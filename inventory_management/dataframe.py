import requests
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder

try:
    print("Fetching product data...")
    product_api = requests.get("http://localhost:8000/product/json")
    product_api.raise_for_status() 
    product_api_data = product_api.json()
    print("Product data fetched successfully.")

    print("Fetching order data...")
    order_api = requests.get("http://localhost:8000/orders/json")
    order_api.raise_for_status() 
    order_api_data = order_api.json()
    print("Order data fetched successfully.")

    print("\nFlattening product data...")
    product_df = pd.DataFrame(product_api_data['products'])  
    print(f"Product DataFrame shape: {product_df.shape}")
    print(product_df.tail())  

    print("\nFlattening order data...")
    order_data = []
    for order in order_api_data['orders']:
        order_data.append({
            'order_id': order.get('order_id'),
            'user_id': order.get('user_id'),
            'user_username': order.get('user_username'),
            'product_id': order.get('product_id'),
            'product_name': order.get('product_name'),
            'quantity': order.get('quantity'),
            'created_at': order.get('created_at'),
            'updated_at': order.get('updated_at'),
            'is_approved': order.get('is_approved'),
        })
    order_df = pd.DataFrame(order_data)  
    print(f"Order DataFrame shape: {order_df.shape}")
    print(order_df.head())  

    print("\nMerging product and order data...")
    merged_df = pd.merge(order_df, product_df, left_on='product_id', right_on='id', how='inner')
    merged_df = merged_df.rename(columns={'id': 'product_id', 'name': 'product'}) 
    print(f"Merged DataFrame shape: {merged_df.shape}")
    print(merged_df.head()) 

    print("\nChecking for missing values...")
    print(merged_df.isnull().sum()) 
    print("\nChecking for product missing values")
    print(product_df.isnull().sum())  

    print("\nImputing missing values in product dataframe...")
    product_df['stock_level'] = product_df['stock_level'].fillna(product_df['stock_level'].mean()) 
    product_df['reorder_level'] = product_df['reorder_level'].fillna(product_df['reorder_level'].median())  
    product_df['price'] = product_df['price'].fillna(product_df['price'].mode()[0])
    product_df['description'] = product_df['description'].fillna('No description')  
    print(product_df[['name', 'stock_level', 'reorder_level', 'price', 'description']].tail())  

    duplicate_count = product_df.duplicated().sum()
    print(f"Number of duplicate rows in product_df: {duplicate_count}")

    duplicates_columns = merged_df.columns[merged_df.columns.duplicated()]
    print("Duplicated columns in merged_df:", duplicates_columns)

    print("\nDropping duplicate and unnecessary columns...")
    merged_df = merged_df.drop(columns=['product_id', 'product']) 
    print(merged_df.columns) 

    print("\nEncoding 'is_approved' as binary (0/1)...")
    merged_df['is_approved'] = merged_df['is_approved'].astype(int)  
    print(f"Sample data after encoding 'is_approved':\n{merged_df[['order_id', 'is_approved']].head()}\n")

    print("\nEncoding 'product_name' using LabelEncoder...")
    label_encoder = LabelEncoder()
    merged_df['product_encoded'] = label_encoder.fit_transform(merged_df['product_name'])
    print(f"Sample data after encoding 'product_name':\n{merged_df[['order_id', 'product_name', 'product_encoded']].tail()}")

    print("\nCreating new 'stock_status' column based on 'quantity'...")
    merged_df['stock_status'] = merged_df['quantity'].apply(lambda x: 'Low' if x < 10 else 'Sufficient')  
    print(f"Sample data after adding 'stock_status':\n{merged_df[['order_id', 'quantity', 'stock_status']].head()}")

    print("\nStandardizing 'quantity' column using StandardScaler...")
    scaler = StandardScaler()
    merged_df['quantity_std'] = scaler.fit_transform(merged_df[['quantity']])  
    print(f"Sample data after standardizing 'quantity':\n{merged_df[['order_id', 'quantity', 'quantity_std']].head()}")

    print("\nNormalizing 'quantity' column using MinMaxScaler...")
    min_max_scaler = MinMaxScaler()
    merged_df['quantity_norm'] = min_max_scaler.fit_transform(merged_df[['quantity']])  
    print(f"Sample data after normalizing 'quantity':\n{merged_df[['order_id', 'quantity', 'quantity_norm']].head()}")

    print("\nPerforming One-Hot Encoding on 'stock_status'...")
    merged_df = pd.get_dummies(merged_df, columns=['stock_status'], drop_first=False) 
    print(f"Sample data after One-Hot Encoding:\n{merged_df[['order_id', 'stock_status_Low', 'stock_status_Sufficient']].head()}")

    print("\nProcessed data sample:")
    print(merged_df.head())

    processed_data = merged_df.to_dict(orient='records')

except requests.exceptions.RequestException as e:
    print(f"HTTP Request error: {e}")
except Exception as e:
    print(f"Error: {e}")
