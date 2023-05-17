import pickle
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from streamlit import session_state as state
import mysql.connector
from evadella_mysql import *
import plotly.express as px
from evadellalogin import * 

st.set_page_config(
    page_title="EvaDella App",
    page_icon="🧊",
    layout="wide",  
    initial_sidebar_state="collapsed"
)

# user authentication
names = ["Giridhar", "Yerra"]
usernames = ["evadellagiri", "evadellayerra"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

    credentials = {
        "usernames":{
            usernames[0]:{
                "name":names[0],
                "password":hashed_passwords[0]
                },
            usernames[1]:{
                "name":names[1],
                "password":hashed_passwords[1]
                }            
            }
        }

authenticator = stauth.Authenticate(credentials,
    "dashborad", "abcdefg", cookie_expiry_days = 30)

name, authentication_status, username = authenticator.login("login", "main")

if authentication_status == False:
    st.error("Username/Password is incorrect")

if authentication_status: 
    state.authentication_status = True

    page = st.sidebar.selectbox("Select a page", ["evadellaapp.py","evadellaapprawdata.py"])

    # Navigation Bar
    if page == "evadellaapp.py":
        st.title(':smile: EvaDella App Dashboard')

        authenticator.logout("logout")

        # Navigation Bar
        selected = option_menu(
            menu_title = None,
            options = ["Operations", "Sales", "Inventory"],
            icons = ["house", "book", ""],
            orientation = "horizontal",
        )

        if selected == "Operations":

            # css applied
            with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

            # columns for partition
            col5, col6 = st.columns(2)

            with col5:

                st.subheader("Order Count By Status")

                orderCountByStatusDf = pd.read_sql_query(orderCountByStatus, mydb)
                filteredOrderCountByStatusDf = orderCountByStatusDf.pivot_table(index='status_cd', columns='Date', values='Date', aggfunc='count')
                byStatusOrderCountDf = ((filteredOrderCountByStatusDf.replace(np.nan, 0)).astype(int)).iloc[:, ::-1]
                sumoforders = byStatusOrderCountDf.iloc[:, 3:].sum(axis=1)
                orderCountByStatusFinalDf = byStatusOrderCountDf.drop(byStatusOrderCountDf.iloc[:, 3:], axis=1)
                orderCountByStatusFinalDf['Prior period'] = sumoforders
                dfOrderCountByStatus = (pd.DataFrame(orderCountByStatusFinalDf)).reset_index()
                dfOrderCountByStatus.columns.values[0] = "Order Submit Date"

                st.table(dfOrderCountByStatus)

            with col6:

                st.subheader("Today Orders/Average Orders - Count/Amount")

                todayOrdersDetailsDf = pd.read_sql_query(todayOrdersDetails, mydb)
                convert_dict = {'Count': int, 'Amount' :int}
                todayOrdersDetailsDf = todayOrdersDetailsDf.astype(convert_dict)
                todayOrdersDetailsDf.iloc[0, 0] = 'Today Orders'
                todayOrdersDetailsDf['Orders'] = todayOrdersDetailsDf['Date'].astype(str)
                todayOrdersDetailsDf = todayOrdersDetailsDf.drop('Date', axis=1)

                averageOrdersBy30DaysDf = pd.read_sql_query(averageOrdersBy30Days, mydb)
                convert_dict = {'Count': int, 'Amount' :int}
                averageOrdersBy30DaysDf = averageOrdersBy30DaysDf.astype(convert_dict)
                averageOrdersBy30DaysDf.iloc[0, 0] = 'Daily Average Orders'
                averageOrdersBy30DaysDf['Orders'] = averageOrdersBy30DaysDf['Date'].astype(str)
                averageOrdersBy30DaysDf = averageOrdersBy30DaysDf.drop('Date', axis=1)

                todayOrdersAverageOrdersDF = (pd.concat([todayOrdersDetailsDf, averageOrdersBy30DaysDf]).reset_index())
                todayOrdersAverageOrdersDF = todayOrdersAverageOrdersDF.drop('index', axis=1)
                firstcolumn = todayOrdersAverageOrdersDF.pop('Orders')
                todayOrdersAverageOrdersDF.insert(0, 'Orders', firstcolumn)

                st.table(todayOrdersAverageOrdersDF)

        if selected == "Sales":

            # css applied
            with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

            # columns for partition
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.subheader("Total No Of Orders")
                ordersDf = pd.read_sql(ordersCount, mydb)
                totalOrders = sum(ordersDf['No Of Orders'])
                st.metric("", "")
                st.markdown('<a href="http://localhost:8501/evadellaapprawdata" target="_self" >' + str(totalOrders) +'</a>',unsafe_allow_html = True)

            with col2:
                st.metric(st.text_input(''),  value='')

            with col3:
                st.subheader("Total Amount")
                ordersTable = pd.read_sql_query(getOrdersDf, mydb)
                totalAmount = sum(ordersTable['total_amount'])

                st.metric("", totalAmount, '0%')

            with col4:
                st.subheader("Number of sales")
                st.metric("", "25%", "-8%")

            # columns for partition
            col10, col11 = st.columns(2)

            with col10:
                st.subheader("Orders Count By Coupon Applied")

                ordersCountByCouponDf = pd.read_sql_query(ordersCountByCoupon, mydb)
                optionSelect = st.multiselect("Coupon Applied", options= ordersCountByCouponDf['coupon_applied'].unique(), 
                                            default = ordersCountByCouponDf['coupon_applied'].unique())
                appliedCoupon = ordersCountByCouponDf.query("coupon_applied == @optionSelect")

                st.table(appliedCoupon)

            # columns for partition
            col7, col8, col9 = st.columns(3)

            with col7:
                st.subheader("Orders By AmountRange")

                ordersCountByTotalAmountDf1 =  pd.read_sql_query(ordersCountByTotalAmount1, mydb)
                ordersCountByTotalAmountDf2 =  pd.read_sql_query(ordersCountByTotalAmount2, mydb)
                ordersCountByTotalAmountDf3 =  pd.read_sql_query(ordersCountByTotalAmount3, mydb)
                ordersCountByTotalAmountDf4 =  pd.read_sql_query(ordersCountByTotalAmount4, mydb)
                ordersCountByTotalAmountDf5 =  pd.read_sql_query(ordersCountByTotalAmount5, mydb)

                filteringData = [list(ordersCountByTotalAmountDf1['No Of Orders']), list(ordersCountByTotalAmountDf2['No Of Orders']), 
                            list(ordersCountByTotalAmountDf3['No Of Orders']), list(ordersCountByTotalAmountDf4['No Of Orders']), list(ordersCountByTotalAmountDf5['No Of Orders'])]
                ordersCountByTotalAmountDf = pd.DataFrame(filteringData)
                ordersCountByTotalAmountDf.columns = ['Orders']
                amountRange = ['<100', '101 - 300', '301 - 500', '501 - 1000', '>1000']
                ordersCountByTotalAmountDf['AmountRange'] = amountRange

                st.table(ordersCountByTotalAmountDf)

            with col8:
                st.subheader('Orders Count By Month, By Year')

                ordersDf = pd.read_sql(ordersCount, mydb)

                totalOrderCount =ordersDf[['Year', 'Month Name', 'No Of Orders']]
                totalOrderCountDf = totalOrderCount.pivot_table(index = 'Month Name', columns = 'Year', values='No Of Orders', aggfunc = 'sum')
                totalOrderCountDf = (((totalOrderCountDf.replace(np.nan, 0)).astype(int)).iloc[:, ::-1]).reset_index()
                totalOrderCountDf.columns.values[0] = "Month Name/Year"

                st.table(totalOrderCountDf)

            with col9:
                st.subheader('No Of Orders By Year')

                ordersDf = pd.read_sql(ordersCount, mydb)

                def noOfOrders():   
                    noOfOrdersDf = (ordersDf.groupby(['Year'])['No Of Orders'].sum()).reset_index()
                    return noOfOrdersDf

                noOfOrdersCountDf = noOfOrders()

                optionSelect = st.multiselect('select year', options=noOfOrdersCountDf['Year'].unique(), 
                                            default = noOfOrdersCountDf['Year'].unique())
                ordersByYearDf = noOfOrdersCountDf.query("Year == @optionSelect")

                st.bar_chart(ordersByYearDf, x='Year', y='No Of Orders')

            # pie chart
            st.subheader("Last 30days Orders Count")

            ordersLastMonthCountDf = pd.read_sql(ordersLastMonthCount, mydb)
            fig = px.pie(ordersLastMonthCountDf, values='No Of Orders', names='Date')

            st.plotly_chart(fig)


    if page == "evadellaapprawdata.py":

        st.title('Raw Data To Home Page')

        # authenticator.logout("logout")

        st.subheader('Total Orders Details')

        # unShippedOrdersMonthCountDf1
        ordersDf = pd.read_sql(ordersCount, mydb)

        totalOrders = sum(ordersDf['No Of Orders'])

        st.metric("Total No Of Orders", totalOrders)

        st.dataframe(ordersDf)