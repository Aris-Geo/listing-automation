def update_low_quantity_items(df):

    low_qty_mask = df['FixedPriceQuantity'] < 50
    
    skus_to_update = df.loc[low_qty_mask, 'ProductID'].tolist()
    
    df = df.drop(columns=['FixedPriceQuantity'])
    
    return df, skus_to_update