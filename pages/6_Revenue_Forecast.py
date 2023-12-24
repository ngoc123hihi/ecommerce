import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima.arima import auto_arima
import streamlit as st

# Create a fake sales dataset
np.random.seed(0)

width = st.sidebar.slider("plot width", 0.1, 25., 15.)
height = st.sidebar.slider("plot height", 0.1, 25., 5.)

customer_df = st.session_state.get('df_customer', None)
product_df = st.session_state.get('df_product', None)
transaction_df = st.session_state.get('df_transaction', None)

product_df = product_df.rename(columns = {'id' : 'product_id'})

df_transaction_cus = transaction_df.merge(customer_df , how = 'left' , on = 'customer_id')
df_transaction_cus_prod = df_transaction_cus.merge(product_df , how = 'left' , on = 'product_id')
df_transaction_trend = transaction_df.copy()

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import networkx as nx


# Create multiple tabs using st.submenu
tabs = st.radio("Select a Tab:", ("Overview" , "Revenue Forecast"))

df_transaction_trend['created_at'] = pd.to_datetime(df_transaction_trend['created_at'])
df_transaction_trend.set_index('created_at', inplace=True)

if tabs == "Overview":
    st.write("## Monthly trends in total sales.")

    # Monthly sales trend
    fig = plt.figure(figsize=(width, height))
    monthly_sales = df_transaction_trend['total_amount'].resample('M').sum()
    monthly_sales.plot()
    plt.title('Monthly Sales Trend')
    plt.ylabel('Total Sales')
    st.pyplot(fig)

    fig = plt.figure(figsize=(width, height))
    weekly_sales = df_transaction_trend['total_amount'].resample('W').sum()
    weekly_sales.plot()
    plt.title('Weekly Sales Trend')
    plt.ylabel('Total Sales')
    st.pyplot(fig)

        

elif tabs == "Revenue Forecast":

    weekly_sales = df_transaction_trend['total_amount'].resample('W').sum()

    st.write("We see that the series has a period of 1 year. The demand for shopping on e-commerce platforms increased in the months when the covid-19 epidemic began, when people stayed at home so shopping at home became more popular. In addition, we can use a seasonal decompose to extract the components that make up the series including: trend, season, residual like under:")
    
    result = seasonal_decompose(weekly_sales, model='multiplicative')
    fig = result.plot()
    fig.set_size_inches(15, 5)
    st.pyplot(fig)
    
    train, test = weekly_sales[weekly_sales.index < '2022-01-01'], weekly_sales[weekly_sales.index >= '2022-01-01']

    st.write("## autocorrelation and partial correlation")
    plot_pacf(train);
    plot_acf(train);
    
    st.write("## Summarize Arima")
    model_sarima = auto_arima(train, start_p=0, start_q=0,
                           max_p=2, max_q=5, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
    st.text(model_sarima.summary())
    
    st.write("## Revenue Forecast by Arima")
    n_pred_perious = 30
    fitted, confint = model_sarima.predict(n_periods=n_pred_perious, return_conf_int=True)
    date = pd.date_range(train.index[-1], periods=n_pred_perious, freq='W')

    fitted_seri = pd.Series(fitted, index=date)
    lower = confint[:, 0]
    upper = confint[:, 1]

    fig = plt.figure(figsize=(12, 6))
    plt.plot(weekly_sales[-318:], label='Actual')
    plt.plot(fitted_seri, color='red', linestyle='--', label = 'Forecast')
    plt.fill_between(date,
                    lower,
                    upper,
                    color='grey', alpha=0.2)
    # plt.ylim((0, 130))
    plt.legend()
    plt.title('SARIMA regression model forecast for 12 next months')
    st.pyplot(fig)


