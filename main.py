import pandas as pd
import os
from datetime import datetime

# Import custom modules
import data_loader
import data_cleaner
from transformers import (
    certified_refurbished, 
    quantity_handler, 
    subtitle_handler,
    shipping_handler, 
    restriction_handler,
    best_offer_handler,
    global_shipping_handler
)

def main():
    current_file = "EbayNotListed.xlsx"
    previous_file = "EbayNotListed_spec_Done.xlsx"
    platform_restrictions_file = "1_PlatformRestrictions.xlsx"
    subtitles_file = "SubtitleseBay.xlsx"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"EbayNotListed_processed_{timestamp}.xlsx"
    
    cr_brands = ["Sony", "Nikon", "Canon", "DJI", "GoPro", "Logitech"]
    
    report = {
        'missing_fields': [],
        'dimension_updates': [],
        'quantity_updates': [],
        'restricted_skus': []
    }
    
    try:
        print("Loading data files...")
        current_df = data_loader.load_unlisted_file(current_file)
        previous_df = data_loader.load_previous_day_file(previous_file)
        
        restriction_data = data_loader.load_platform_restrictions(platform_restrictions_file)
        subtitles_df = data_loader.load_subtitles(subtitles_file)
        
        print("Removing duplicates and validating fields...")
        df = data_cleaner.remove_duplicates(current_df, previous_df)
        df, missing_fields = data_cleaner.validate_required_fields(df)
        
        if missing_fields is not None:
            report['missing_fields'] = missing_fields['ProductID'].tolist()
        
        print("Copying titles to ProductName column...")
        df['ProductName'] = df['TopTitles']
        
        print("Processing certified refurbished items...")
        df = certified_refurbished.process_certified_refurbished(df, cr_brands)
        
        print("Updating low quantity items...")
        df, qty_updates = quantity_handler.update_low_quantity_items(df)
        report['quantity_updates'] = qty_updates
        
        print("Checking shipping dimensions...")
        df, dim_updates = shipping_handler.check_shipping_dimensions(df)
        report['dimension_updates'] = dim_updates
        
        print("Checking platform restrictions...")
        df, restricted = restriction_handler.check_platform_restrictions(
            df, restriction_data['listing_restrictions']
        )
        report['restricted_skus'] = restricted
        
        print("Generating subtitles...")
        df = subtitle_handler.generate_subtitles(df, subtitles_df)
        
        print("Applying best offer rules...")
        df = best_offer_handler.apply_best_offer_rules(
            df, restriction_data['no_best_offer']
        )
        
        print("Applying global shipping rules...")
        df = global_shipping_handler.apply_global_shipping_rules(
            df, restriction_data['no_international']
        )
        
        print("Performing final cleanup...")
        df = data_cleaner.delete_unnecessary_columns(df)
        
        print(f"Saving processed file to {output_file}...")
        df.to_excel(output_file, index=False)
        
        if any(report.values()):
            print("Generating manual follow-up reports...")
            for key, items in report.items():
                if items:
                    pd.DataFrame(items).to_excel(f"{key}_{timestamp}.xlsx", index=False)
        
        print("Processing complete!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
        
if __name__ == "__main__":
    main()