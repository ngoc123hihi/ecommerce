import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

maxUploadSize = 1000

# Max size, in megabytes, of messages that can be sent via the WebSocket
# connection.
# Default: 200
maxMessageSize = 1000

# Create a fake sales dataset
np.random.seed(0)

# Save the DataFrame to a CSV file

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# from Homepage import df_customer, df_product, df_transaction


customer_df = st.session_state.get('df_customer', None)
product_df = st.session_state.get('df_product', None)
transaction_df = st.session_state.get('df_transaction', None)

product_df = product_df.rename(columns = {'id' : 'product_id'})

# Add tabs to the Streamlit app
st.title("E-commerce Customer Analysis")
st.subheader("Explore Customer Data")

# Create multiple tabs using st.submenu
tabs = st.radio("Select a Tab:", ("Overview" , "Customer Analysis"))

if tabs == "Overview":
    st.write("## Customer Overview")
    st.dataframe(customer_df)

elif tabs == "Customer Analysis":

    customer_df['birthdate'] = pd.to_datetime(customer_df['birthdate'],format= '%Y-%m-%d' )
    customer_df['Age'] = ((datetime.now() - customer_df['birthdate']).dt.days / 365.25).round().astype(np.int64)
    st.write("## Customer distribution by age and gender")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.histplot(data=customer_df[customer_df['gender'] == 'F'], x="Age",color = 'navy', kde=True , ax = axes[0] , bins=30).set(title='Gender F')
    sns.histplot(data=customer_df[customer_df['gender'] == 'M'], x="Age",color = 'navy', kde=True , ax = axes[1] , bins=30).set(title='Gender M')

    st.pyplot(fig)

    st.write("## Revenue by each age group")

    df_amount_cus = transaction_df.groupby('customer_id', as_index =False)['total_amount'].sum()
    df_amount_cus = df_amount_cus.groupby(['customer_id'])['total_amount'].sum().reset_index()

    df_amount_cus_trans = customer_df[['customer_id' , 'gender' , 'Age']].merge(df_amount_cus , how = 'left' , on = 'customer_id')
    
    fig = plt.figure(figsize=(24, 10))
    age_bins = [0,10,20, 30, 40, 50, 60, 70, 80]
    df_amount_cus_trans['Age Group'] = pd.cut(df_amount_cus_trans['Age'], bins=age_bins)
    avg_purchase_by_age = df_amount_cus_trans.groupby(['Age Group'])['total_amount'].mean().reset_index()
    sns.barplot(avg_purchase_by_age, x="Age Group", y="total_amount" , hue="Age Group")
    plt.ylabel('Average Purchase Amount')
    st.pyplot(fig)

    fig = plt.figure(figsize=(24, 10))
    age_labels = ['(0, 10]', '(10, 20]', '(20, 30]', '(30, 40]', '(40, 50]', '(50, 60]', '(60, 70]' , '(70, 80]']

    sns.countplot(data=df_amount_cus_trans, x='Age Group', order=age_labels , palette='husl')
    plt.title('Customer Age Distribution')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    st.pyplot(fig)


    st.write("## Compare the most popular products across age groups")
    df_trans_prod = transaction_df[['created_at','customer_id' , 'product_id']].merge(product_df[['product_id' , 'masterCategory' , 'gender']])
    df_trans_prod_cate = df_trans_prod.groupby(['customer_id', 'masterCategory']).size().unstack().reset_index()
    df_amount_cus_trans_cate = df_amount_cus_trans.merge(df_trans_prod , how = 'right' , on = 'customer_id')
    df_amount_cus_trans_cate_age = df_amount_cus_trans_cate.groupby(['Age Group', 'masterCategory']).size().unstack()
    
    fig = plt.figure(figsize=(24, 10))
    plot = df_amount_cus_trans_cate_age.plot(kind='bar', stacked=True)
    plt.title('Most Popular Product Categories by Age Group')
    plt.ylabel('Number of Purchases')
    st.pyplot(plot.figure)

    df_amount_cus_trans_cate_gender = df_amount_cus_trans_cate.groupby(['gender_x', 'masterCategory']).size().unstack()
    plot = df_amount_cus_trans_cate_gender.plot(kind='bar', stacked=True, figsize=(12, 7))
    plt.title('Most Popular Product Categories by Gender')
    plt.ylabel('Number of Purchases')
    st.pyplot(plot.figure)






#     selected_product = st.selectbox("Select a Product:", customer_df['Product'].unique())

#     product_df = customer_df[customer_df['Product'] == selected_product]

#     # Add filters and radio buttons
#     st.write("### Filter Data")
#     min_quantity = st.slider("Minimum Quantity Sold", min_value=1, max_value=100, value=1)
#     filtered_product_df = product_df[product_df['Quantity Sold'] >= min_quantity]
#     st.dataframe(filtered_product_df)

# elif tabs == "Date Analysis":
#     st.write("## Date Analysis")
#     st.line_chart(customer_df.groupby('Date')['Revenue'].sum())

# elif tabs == "Data Visualization":
#     st.write("## Data Visualization")

#     # Interactive Scatter Plot
#     st.write("### Interactive Scatter Plot")
#     selected_metric = st.selectbox("Select a Metric:", ('Quantity Sold', 'Revenue'))
#     c = alt.Chart(customer_df).mark_circle().encode(
#         x='Date',
#         y=selected_metric,
#         color='Product',
#         size='Quantity Sold'
#     ).interactive()
#     st.altair_chart(c, use_container_width=True)

#     # Distribution Plot
#     st.write("### Distribution Plot")
#     selected_feature = st.selectbox("Select a Feature:", ('Quantity Sold', 'Revenue'))
#     hist_values = np.histogram(customer_df[selected_feature], bins=20)[0]
#     st.bar_chart(hist_values)

#     # Advanced filters
#     st.write("### Advanced Filters")
#     min_revenue = st.number_input("Minimum Revenue", value=0, min_value=0, max_value=int(customer_df['Revenue'].max()))
#     filtered_data = customer_df[customer_df['Revenue'] >= min_revenue]
#     st.dataframe(filtered_data)


