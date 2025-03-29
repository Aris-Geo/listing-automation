# data_cleaner.py
import pandas as pd

def remove_duplicates(current_df, previous_df):
    duplicate_skus = current_df[current_df['ProductID'].isin(previous_df['ProductID'])]['ProductID']
    # Remove duplicates
    return current_df[~current_df['ProductID'].isin(duplicate_skus)]

def validate_required_fields(df):
    missing_data = df[(df['BrandName'].isna()) | 
                      (df['ManufacturerName'].isna()) | 
                      (df['Manufacture SKU'].isna())]
    
    if not missing_data.empty:
        return df[~df.index.isin(missing_data.index)], missing_data
    return df, None

def delete_unnecessary_columns(df):
    columns_to_delete = [
        "Category Specifics",
        "ManufacturerName", 
        "Manufacture SKU",
        "Kit", 
        "StoreCategory1", 
        "CoreEbayCategory",
        "UPC", 
        "AggregateQty", 
        "SpexCategory", 
        "Prop65Type", 
        "Prop65Desc",
        "RequireToBeReturned",
        "ItemCondition"
    ]
    existing_columns = [col for col in columns_to_delete if col in df.columns]
    return df.drop(columns=existing_columns)

def hide_columns_for_bulk_update(df):
    columns_to_hide = [
        "eBayEnabled",
        "eBayPriceUseDefault",
        "eBayUseShippingRateTableID",
        "DescriptionTemplateId",
        "eBayCategory1",
        "MAPPricingTreatment",
        "eBayEnableStrikeThroughPrices",
        "eBaySellingZipCode",
        "eBaySellingCity",
        "eBaySellingState"
    ]
    
    for col in columns_to_hide:
        if col in df.columns:
            df = df.rename(columns={col: f"HIDDEN_{col}"})
    
    return df