import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

maxUploadSize = 1000

# Max size, in megabytes, of messages that can be sent via the WebSocket
# connection.
# Default: 200
maxMessageSize = 1000

# Create a fake sales dataset
np.random.seed(0)

customer_df = st.session_state.get('df_customer', None)
product_df = st.session_state.get('df_product', None)
transaction_df = st.session_state.get('df_transaction', None)

product_df = product_df.rename(columns = {'id' : 'product_id'})

df_trans_prod = transaction_df.merge(product_df , how = 'left' , on = 'product_id')
transaction_df['created_at'] = pd.to_datetime(transaction_df['created_at'])

# Add tabs to the Streamlit app
st.title("E-commerce Transaction Analysis")
st.subheader("Explore Transaction Data")

# Create multiple tabs using st.submenu
tabs = st.radio("Select a Tab:", ("Overview" , "Transaction Visualization", "Transaction Analysis"))

width = st.sidebar.slider("plot width", 0.1, 25., 14.)
height = st.sidebar.slider("plot height", 0.1, 25., 5.)

if tabs == "Overview":
    st.write("## Transaction Overview")
    st.dataframe(transaction_df)

elif tabs == "Transaction Analysis":
    st.write("## Distribution of payment methods used by customers")
    fig = plt.figure(figsize=(width, height))
    sns.countplot(data=transaction_df, x='payment_method', order=transaction_df['payment_method'].value_counts().index , palette='husl')
    plt.title('Distribution of Payment Methods Used by Customers')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("## Average purchase amount by payment method")
    fig = plt.figure(figsize=(width, height))
    sns.barplot(data=transaction_df, x='payment_method', y='total_amount', ci=None , palette='husl')
    plt.title('Average Purchase Amount by Payment Method')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("## Correlation between payment method and product category or price")

    fig = plt.figure(figsize=(width, height))
    sns.boxplot(data=df_trans_prod, x='payment_method', y='item_price', hue='masterCategory')
    plt.title('Distribution of Product Prices by Payment Method and Product Category')
    plt.xticks(rotation=45)
    plt.legend(loc='upper right')
    st.pyplot(fig)

    st.write("## Total number of unsuccessful payments of the e-commerce platform")
    payStatus = transaction_df.groupby(['payment_status'])['payment_status'].count()
    
    fig = plt.figure(figsize=(width, height))
    explodeSize = [0.1, 0.1]
    plt.pie(payStatus, labels = ['Failed', 'Success'], shadow = True, autopct='%1.1f%%', explode = explodeSize)
    st.pyplot(fig)


elif tabs == "Transaction Visualization":

    st.write("## Transaction Visualization")
    selected_product = st.selectbox("Select a Transaction:", df_trans_prod['masterCategory'].unique())

    product_df_ = df_trans_prod[df_trans_prod['masterCategory'] == selected_product]

    # Add filters and radio buttons
    st.write("### Filter Data")
    min_quantity = st.slider("Minimum Quantity Sold", min_value=1, max_value=100, value=1)
    filtered_product_df = product_df_[product_df_['quantity'] >= min_quantity]
    st.dataframe(filtered_product_df)

    # # Interactive Scatter Plot
    # st.write("### Interactive Scatter Plot")
    # selected_metric = st.selectbox("Select a Metric:", ('quantity', 'total_amount'))
    # c = alt.Chart(df_trans_prod).mark_circle().encode(
    #     x='created_at',
    #     y=selected_metric,
    #     color='masterCategory',
    #     size='quantity'
    # ).interactive()
    # st.altair_chart(c, use_container_width=True)

    # # Distribution Plot
    # st.write("### Distribution Plot")
    # selected_feature = st.selectbox("Select a Feature:", ('quantity', 'total_amount'))
    # hist_values = np.histogram(df_trans_prod[selected_feature], bins=20)[0]
    # st.bar_chart(hist_values)

    # # Advanced filters
    # st.write("### Advanced Filters")
    # min_revenue = st.number_input("Minimum total_amount", value=0, min_value=0, max_value=int(df_trans_prod['total_amount'].max()))
    # filtered_data = df_trans_prod[df_trans_prod['total_amount'] >= min_revenue]
    # st.dataframe(filtered_data)


