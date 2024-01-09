import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# Create a fake sales dataset
np.random.seed(0)

# Save the DataFrame to a CSV file

maxUploadSize = 400

# Max size, in megabytes, of messages that can be sent via the WebSocket
# connection.
# Default: 200
maxMessageSize = 400

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import networkx as nx


# Load the fake sales dataset

# Add tabs to the Streamlit app
st.title("E-commerce Sales Analysis")
st.subheader("Explore Sales Data")

width = st.sidebar.slider("plot width", 0.1, 25., 20.)
height = st.sidebar.slider("plot height", 0.1, 25., 10.)

customer_df = st.session_state.get('df_customer', None)
product_df = st.session_state.get('df_product', None)
transaction_df = st.session_state.get('df_transaction', None)

customer_df['first_join_date'] = pd.to_datetime(customer_df['first_join_date'])
customer_df['birthdate'] = pd.to_datetime(customer_df['birthdate'])
customer_df["full_name"] = customer_df['first_name'].astype(str) +" "+ customer_df["last_name"]

df_transaction_cus = transaction_df.merge(customer_df , how = 'left' , on = 'customer_id')

total_purchase_per_customer = df_transaction_cus.groupby('full_name')['total_amount'].sum()

st.write("## Visualize Cluster Customer by KMeans")

# Tạo tập dữ liệu cấp độ khách hàng với các số liệu liên quan để phân khúc
customer_data = df_transaction_cus.groupby('full_name').agg({
    'total_amount': ['sum', 'mean'],
    'join_time' : 'max'
}).reset_index()

customer_data.columns = ['full_name', 'Total Purchases', 'Average Purchase Amount' , 'Join Time Customer']

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
scaled_data = scaler.fit_transform(customer_data[['Total Purchases', 'Average Purchase Amount' , 'Join Time Customer']])

# Gán các giá trị bị thiếu bằng giá trị trung bình
imputer = SimpleImputer(strategy='mean')
scaled_data_imputed = imputer.fit_transform(scaled_data)

# Áp dụng phân cụm KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(scaled_data_imputed)

# Trực quan hóa và giải thích các cụm
plt.figure(figsize=(10, 6))
sns.scatterplot(data=customer_data, x='Total Purchases', y='Average Purchase Amount', hue='Cluster', palette='viridis')
plt.title('Customer Segmentation based on Total Purchases and Average Purchase Amount')
plt.show()

# Analyze other metrics by cluster
cluster_summary = customer_data.groupby('Cluster').agg({
    'Total Purchases': 'mean',
    'Average Purchase Amount': 'mean',
    'Join Time Customer': 'mean'
}).reset_index()

cluster_summary = cluster_summary.sort_values(by='Total Purchases', ascending=True).reset_index(drop = True)
cluster_summary['rank'] = ['bronze' , 'silver', 'gold' , 'platinum' , 'diamond']
# rank = pd.DataFrame(data = {'Cluster' : [0,1,2,3,4] , 'rank' : ['bronze' , 'silver', 'gold' , 'platinum' , 'diamond']})
# cluster_summary = cluster_summary.merge(rank , how = 'left' , on = 'Cluster')

st.write("## DataFrame Cluster Customer")

rank = pd.DataFrame(data = {'Cluster' : [0,1,2,3 , 4] , 'rank' : ['bronze' , 'silver', 'gold' , 'platinum' , 'diamond']})
cluster_summary = cluster_summary.merge(rank , how = 'left' , on = 'Cluster')
st.dataframe(cluster_summary)

