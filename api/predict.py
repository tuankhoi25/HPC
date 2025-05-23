import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def get_dataframes():
    df_orders_item = pd.read_csv("data/raw/order_items.csv")
    df_users = pd.read_csv("data/raw/users.csv")

    filtered_df_oi = df_orders_item[df_orders_item['status'] == 'Complete'].copy()

    filtered_df_oi['created_at'] = filtered_df_oi['created_at'].apply(
        lambda x: pd.to_datetime(str(x).strip(), errors='coerce')
    )

    frequency = filtered_df_oi.groupby('user_id')['order_id'].count()
    frequency = frequency.rename('frequency')


    current_time = max(filtered_df_oi['created_at'])  
    filtered_df_oi['diff'] = current_time - filtered_df_oi['created_at']  
    recency = filtered_df_oi.groupby('user_id')['diff'].min() 
    recency = recency.dt.days

    monetary = filtered_df_oi.groupby('user_id')['sale_price'].sum()

    rfm = pd.merge(frequency, recency, on='user_id', how = 'inner')
    rfm = pd.merge(rfm, monetary, on='user_id', how = 'inner')

    rfm = rfm.rename(columns={'diff': 'recency', 'sale_price': 'monetary'})
    rfm = rfm[['recency', 'frequency', 'monetary']]

    scaler = StandardScaler()
    rfm_scaler = rfm[['recency', 'frequency', 'monetary']]
    rfm_scaler = scaler.fit_transform(rfm_scaler)
    rfm_scaler = pd.DataFrame(rfm_scaler, columns=['recency', 'frequency', 'monetary'])

    kmeans = KMeans(n_clusters=4,init='k-means++',random_state=42)
    kmeans.fit(rfm_scaler)
    rfm['Segmentation'] = kmeans.labels_

    return rfm.reset_index(), df_users

def get_user_info(user_id, rfm, df_users):
    merged = pd.merge(
        rfm.reset_index(),
        df_users[['id', 'first_name', 'last_name', 'email', 'age', 'gender', 'country']],
        left_on='user_id',
        right_on='id',
        how='left'
    ).drop(columns=['id'])

    result = merged[merged['user_id'] == user_id]
    if result.empty:
        return f"Không tìm thấy user_id: {user_id}"
    
    # Convert to dict and reorder keys
    user_info = result.iloc[0].to_dict()
    desired_order = [
        'user_id', 'first_name', 'last_name', 'email', 'age', 'gender', 'country',
        'recency', 'frequency', 'monetary', 'Segmentation'
    ]
    return {key: user_info[key] for key in desired_order if key in user_info}