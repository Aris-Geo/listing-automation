import pandas as pd

def generate_subtitles(df, subtitles_df):

    result_df = df.copy()
    
    subtitle_lookup = dict(zip(subtitles_df['SKU'], subtitles_df['SubTitle']))
    
    result_df['SubTitle'] = result_df['ProductID'].map(subtitle_lookup)
    
    result_df['SubTitle'] = result_df['SubTitle'].fillna('Free Shipping! Get It Fast!')
    
    cr_mask = result_df['EBayItemCondition'].isin([2000, 2500])
    
    auth_dealer_mask = result_df['SubTitle'] == 'Authorized Dealer - Full USA Warranty'
    result_df.loc[cr_mask & auth_dealer_mask, 'SubTitle'] = 'Free Shipping! Get It Fast!'
    
    cr_2000_mask = result_df['EBayItemCondition'] == 2000
    result_df.loc[cr_2000_mask, 'SubTitle'] = 'Certified Refurbished -- 2 year warranty'
    
    return result_df