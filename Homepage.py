import altair as alt
import streamlit as st
import requests
import pandas as pd
import base64
import datetime
from st_pages import Page, show_pages, add_page_title
import time  # Used for simulating a processing time

st.set_page_config(
    page_title='E-commerce Sales Analysis',
    page_icon="chart_with_upwards_trend",
    layout='wide',
)
# st.title('Explore Sales Data')

show_pages(
    [
        Page("Homepage.py", "Homepage", "🏠"),
        Page("pages/Customer.py", "Customer Analyst", ":customs:"),
        Page("pages/Product.py", "Product Analyst", ":shopping_trolley:"),
        Page("pages/Transaction.py", "Transaction Analyst", ":inbox_tray:"),
        Page("pages/Product_Link.py", "Product Link Algorithm", ":linked_paperclips:"),
        Page("pages/Revenue_Forecast.py", "Revenue Forecast Predict", ":chart_with_upwards_trend:"),
        Page("pages/Cluster_Customers.py", "Cluster Customers", ":customs:"),
    ]
)  

# Sidebar for file upload
uploaded_file1 = st.sidebar.file_uploader("Choose a data Customer file", type="csv" , accept_multiple_files=False)
uploaded_file2 = st.sidebar.file_uploader("Choose a data Product file", type="csv", accept_multiple_files=False)
uploaded_file3 = st.sidebar.file_uploader("Choose a data Transaction file", type="csv", accept_multiple_files=False)

if uploaded_file1 is None:
    with st.spinner('Please import Customer data ...'):
        time.sleep(60)
else:
    df_customer = pd.read_csv(uploaded_file1)
st.session_state['df_customer'] = df_customer

if uploaded_file2 is None:
    with st.spinner('Please import Product data ...'):
        time.sleep(60)
else: 
    df_product = pd.read_csv(uploaded_file2)
st.session_state['df_product'] = df_product

if uploaded_file3 is None:
    with st.spinner('Please import Transaction data ...'):
        time.sleep(60)
else: 
    df_transaction = pd.read_csv(uploaded_file3)

st.session_state['df_transaction'] = df_transaction

def get_image_base64(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


image_base64 = get_image_base64('Devops-ecom.gif')
st.markdown(f"""
    <div style='border-radius: 100px; overflow: hidden;'>
        <img src='data:image/gif;base64,{image_base64}' width='100%' height='60%'/>
    </div>
    """, unsafe_allow_html=True)


st.markdown(
    """
<style>
.css-1aumxhk {
    background-color: #D4AF37;
}
</style>
""",
    unsafe_allow_html=True,
)


# # Specify what pages should be shown in the sidebar, and what their titles 
# # and icons should be

