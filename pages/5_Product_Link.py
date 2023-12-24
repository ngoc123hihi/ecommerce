import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import networkx as nx

# Create a fake sales dataset
np.random.seed(0)

maxUploadSize = 400

# Max size, in megabytes, of messages that can be sent via the WebSocket
# connection.
# Default: 200
maxMessageSize = 400

# Load the fake sales dataset

# Add tabs to the Streamlit app
st.title("E-commerce Sales Analysis")
st.subheader("Explore Sales Data")

width = st.sidebar.slider("plot width", 0.1, 25., 20.)
height = st.sidebar.slider("plot height", 0.1, 25., 10.)

customer_df = st.session_state.get('df_customer', None)
product_df = st.session_state.get('df_product', None)
transaction_df = st.session_state.get('df_transaction', None)

product_df = product_df.rename(columns = {'id' : 'product_id'})

df_transaction_cus = transaction_df.merge(customer_df , how = 'left' , on = 'customer_id')
df_transaction_cus_prod = df_transaction_cus.merge(product_df , how = 'left' , on = 'product_id')

st.write("## Encrypt master categories")
basket = df_transaction_cus_prod.groupby(['customer_id', 'masterCategory'])['quantity'].sum().unstack().fillna(0)
basket[basket > 0] = 1
st.dataframe(basket)

# Chuyển đổi dữ liệu thành định dạng được mã hóa one-hot
basket = df_transaction_cus_prod.groupby(['customer_id', 'masterCategory'])['quantity'].sum().unstack().fillna(0)

# Chuyển đổi giá trị số lượng sang nhị phân (1 nếu đã mua, 0 nếu không)
basket[basket > 0] = 1

# Thực hiện thuật toán Apriori để tìm tập mục thường xuyên
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)

# Tạo quy tắc kết hợp
association_rules_transaction_cus = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# Lọc và sắp xếp các quy tắc cho đề xuất
recommended_rules = association_rules_transaction_cus[association_rules_transaction_cus['lift'] > 1.0].sort_values(by='lift', ascending=False)

# Hiển thị các quy tắc được đề xuất
print(recommended_rules[['antecedents', 'consequents', 'support', 'lift']])

st.write("## Recommended Rules by Apriori")
st.dataframe(recommended_rules)

# Network Graph Visualization
st.write("## Network Graph Visualization")
G = nx.DiGraph()
fig = plt.figure(figsize=(width, height))
for _, row in recommended_rules.iterrows():
    G.add_edge(str(row['antecedents']), str(row['consequents']), weight=row['lift'])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, edge_color='gray', width=[G[u][v]['weight'] for u,v in G.edges()])
plt.title("Association Rules")
st.pyplot(fig)