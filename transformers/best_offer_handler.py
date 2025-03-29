def apply_best_offer_rules(df, no_best_offer_df):
    no_best_offer_dict = dict(zip(no_best_offer_df.iloc[:, 0], no_best_offer_df.iloc[:, 2]))
    
    df['EnableBestOffer'] = df['ProductID'].map(no_best_offer_dict)
    
    price_mask = df['BuyItNow'] < 49.99
    df.loc[price_mask, 'EnableBestOffer'] = 0
    
    cr_mask = df['EBayItemCondition'] == 2000
    df.loc[cr_mask, 'EnableBestOffer'] = 0
    
    df['EnableBestOffer'] = df['EnableBestOffer'].fillna(1)
    
    return df