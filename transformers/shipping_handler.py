def check_shipping_dimensions(df):

    skus_to_update = []
    
    dim_cols = ['ShippingLength', 'ShippingWidth', 'ShippingHeight']
    for idx, row in df.iterrows():
        if any(row[col] == 0 for col in dim_cols):
            skus_to_update.append({
                'sku': row['ProductID'],
                'issue': 'dimensions',
                'update_value': 9.1
            })
    
    weight_cols = ['PackageWeightLbs', 'PackageWeightOz']
    for idx, row in df.iterrows():
        if all(row[col] == 0 for col in weight_cols):
            skus_to_update.append({
                'sku': row['ProductID'],
                'issue': 'weight',
                'update_value': 1  # 1oz as placeholder
            })
            
    return df, skus_to_update