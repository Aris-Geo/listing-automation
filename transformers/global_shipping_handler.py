def apply_global_shipping_rules(df, no_international_df):

    no_international_dict = dict(zip(no_international_df.iloc[:, 0], no_international_df.iloc[:, 4]))
    
    df['eBayEnableGlobalShippingProgram'] = df['ProductID'].map(no_international_dict)
    
    weight_mask = df['PackageWeightLbs'] >= 44
    df.loc[weight_mask, 'eBayEnableGlobalShippingProgram'] = 0
    
    email_mask = df['PurchaserEmail'] == 'fkantor@focuscamera.com'
    df.loc[email_mask, 'eBayEnableGlobalShippingProgram'] = 0
    
    restricted_keywords = [
        'knife', 'knives', 'multi tool', 'weapon', 'sight', 'night vision', 
        'smartwatch', 'fragrance', 'pepper spray', 'stun gun'
    ]
    
    for keyword in restricted_keywords:
        keyword_mask = df['ProductName'].str.contains(keyword, case=False, na=False)
        df.loc[keyword_mask, 'eBayEnableGlobalShippingProgram'] = 0
    
    df['eBayEnableGlobalShippingProgram'] = df['eBayEnableGlobalShippingProgram'].fillna(1)
    
    df['ShippingTemplateID'] = 'Global'
    df.loc[df['eBayEnableGlobalShippingProgram'] == 0, 'ShippingTemplateID'] = 'Domestic'
    
    large_item_mask = (df['PackageWeightLbs'] > 70) | (
        (df['ShippingLength'] + df['ShippingWidth']) > 130
    )
    df.loc[large_item_mask & (df['eBayEnableGlobalShippingProgram'] == 0), 'ShippingTemplateID'] = 'Domestic No PO Box'
    df.loc[large_item_mask & (df['eBayEnableGlobalShippingProgram'] == 1), 'ShippingTemplateID'] = 'Global No PO Box'
    
    return df