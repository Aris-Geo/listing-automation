import pandas as pd

def load_unlisted_file(file_path):
    return pd.read_excel(file_path)
    
def load_previous_day_file(file_path):
    return pd.read_excel(file_path)
    
def load_platform_restrictions(file_path):
    return {
        'listing_restrictions': pd.read_excel(file_path, sheet_name='ListingRestrictions'),
        'no_best_offer': pd.read_excel(file_path, sheet_name='NoBestOffer_UPDATEDMASTERLIST'),
        'no_international': pd.read_excel(file_path, sheet_name='New_eBay_NoInternational')
    }
    
def load_subtitles(file_path):
    return pd.read_excel(file_path)