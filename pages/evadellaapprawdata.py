import pandas as pd
import numpy as np
import streamlit as st
# import mysql.connector
from evadellaapp import *
from evadella_mysql import *
# from evadellalogin import *
import streamlit_authenticator as stauth


st.set_page_config(
    page_title="EvaDella App",
    page_icon="🧊", 
    layout="wide",  
    initial_sidebar_state="collapsed"
)

# css applied
with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

if not hasattr(state, "authentication_status"):
    state.authentication_status = True

if not state.authentication_status:
    st.error("Please login with username/password")
    
else:
    st.title('Raw Data To Home Page')

    authenticator.logout("logout")

    col15, col16 = st.columns(2)

    with col15:

        st.subheader('Total Orders Details')

        # unShippedOrdersMonthCountDf1
        ordersDf = pd.read_sql(ordersCount, mydb)

        totalOrders = sum(ordersDf['No Of Orders'])

        st.metric("Total No Of Orders", totalOrders)

        st.dataframe(ordersDf)                                                                                                