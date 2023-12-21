import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

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

# Load the fake sales dataset

customer_df = st.session_state.get('df_customer', None)
product_df = st.session_state.get('df_product', None)
transaction_df = st.session_state.get('df_transaction', None)

# Add tabs to the Streamlit app
st.title("E-commerce Sales Analysis")
st.subheader("Explore Sales Data")

width = st.sidebar.slider("plot width", 0.1, 25., 14.)
height = st.sidebar.slider("plot height", 0.1, 25., 5.)

# Create multiple tabs using st.submenu
tabs = st.radio("Select a Tab:", ("Overview" , "Product Analysis"))

if tabs == "Overview":
    st.write("## Product Overview")
    st.dataframe(product_df)

elif tabs == "Product Analysis":
    st.write("## Product Analysis")
    column_to_plot = st.selectbox('Select the column to plot:', ['masterCategory' , 'gender' , 'subCategory' , 'baseColour' , 'season'])

    st.write("## Count Plot")
    # Count Plot
    fig_count, ax_count = plt.subplots(figsize=(width, height))
    sns.countplot(x=product_df[column_to_plot], palette='tab10', ax=ax_count)
    plt.xticks(rotation=45)
    st.pyplot(fig_count)

    st.write("## Pie Plot")
    # Pie Plot
    fig_pie, ax_pie = plt.subplots(figsize=(width, height))
    explodeSize = [0.06] * len(product_df[column_to_plot].value_counts())

    season = product_df.groupby([column_to_plot])[column_to_plot].count()

    plt.pie(season, labels = season.index, shadow = True, autopct='%1.1f%%', explode = explodeSize)
    st.pyplot(fig_pie)


    # selected_product = st.selectbox("Select a Product:", product_df['Product'].unique())

    # product_df = product_df[product_df['masterCategory'] == selected_product]

    # # Add filters and radio buttons
    # st.write("### Filter Data")
    # min_quantity = st.slider("Minimum Quantity Sold", min_value=1, max_value=100, value=1)
    # filtered_product_df = product_df[product_df['Quantity Sold'] >= min_quantity]
    # st.dataframe(filtered_product_df)

# elif tabs == "Date Analysis":
#     st.write("## Date Analysis")
#     st.line_chart(product_df.groupby('Date')['Revenue'].sum())

# elif tabs == "Data Visualization":
#     st.write("## Data Visualization")

#     # Interactive Scatter Plot
#     st.write("### Interactive Scatter Plot")
#     selected_metric = st.selectbox("Select a Metric:", ('Quantity Sold', 'Revenue'))
#     c = alt.Chart(product_df).mark_circle().encode(
#         x='Date',
#         y=selected_metric,
#         color='Product',
#         size='Quantity Sold'
#     ).interactive()
#     st.altair_chart(c, use_container_width=True)

#     # Distribution Plot
#     st.write("### Distribution Plot")
#     selected_feature = st.selectbox("Select a Feature:", ('Quantity Sold', 'Revenue'))
#     hist_values = np.histogram(product_df[selected_feature], bins=20)[0]
#     st.bar_chart(hist_values)

#     # Advanced filters
#     st.write("### Advanced Filters")
#     min_revenue = st.number_input("Minimum Revenue", value=0, min_value=0, max_value=int(product_df['Revenue'].max()))
#     filtered_data = product_df[product_df['Revenue'] >= min_revenue]
#     st.dataframe(filtered_data)


