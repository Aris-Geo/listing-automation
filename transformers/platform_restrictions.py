import pandas as pd

def check_platform_restrictions(df, restrictions_df):

    restrictions_dict = dict(zip(restrictions_df.iloc[:, 0], restrictions_df.iloc[:, 1]))
    
    df['TempRestriction'] = df['BrandName'].map(restrictions_dict)
    
    restricted_skus = []
    
    dnl_mask = df['TempRestriction'] == 'Do Not List'
    restricted_skus.extend([
        {'sku': row['ProductID'], 'reason': 'Do Not List'} 
        for _, row in df[dnl_mask].iterrows()
    ])
    
    hk_mask = df['TempRestriction'] == 'Do Not List - Hello Kitty'
    for idx, row in df[hk_mask].iterrows():
        if 'hello kitty' in row['ProductName'].lower():
            restricted_skus.append({
                'sku': row['ProductID'], 
                'reason': 'Do Not List - Hello Kitty'
            })
    
    kit_mask = df['TempRestriction'] == 'Do Not List -- Kits'
    for idx, row in df[kit_mask].iterrows():
        if 'kit' in row['ProductName'].lower():
            restricted_skus.append({
                'sku': row['ProductID'], 
                'reason': 'Do Not List -- Kits'
            })
    
    img_mask = df['TempRestriction'] == 'In House Images Only'
    restricted_skus.extend([
        {'sku': row['ProductID'], 'reason': 'In House Images Only'} 
        for _, row in df[img_mask].iterrows()
    ])
    
    restricted_sku_list = [item['sku'] for item in restricted_skus]
    filtered_df = df[~df['ProductID'].isin(restricted_sku_list)]
    
    filtered_df = filtered_df.drop(columns=['TempRestriction'])
    
    return filtered_df, restricted_skus