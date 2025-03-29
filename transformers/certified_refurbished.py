def process_certified_refurbished(df, cr_brands_list):
    result_df = df.copy()
    
    cr_mask = result_df['ItemCondition'] == 'Certified Refurbished'
    
    for idx in result_df[cr_mask].index:
        brand = result_df.loc[idx, 'BrandName']
        
        if brand in cr_brands_list:
            result_df.loc[idx, 'EBayItemCondition'] = 2000
            
    return result_df