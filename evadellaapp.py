import pickle
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from streamlit import session_state as state
from datetime import datetime, timedelta
import mysql.connector
import os
# from evadella_mysql import *
import toml
import plotly.express as px

# sql = open('task.sql', mode='r', encoding='utf-8-sig').read()

st.set_page_config(
    page_title="EvaDella App",
    page_icon=":ring:",
    layout="wide",  
    initial_sidebar_state="collapsed",
    # background_color = "green"
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
    # st.balloons()
    # st.snow()

    page = st.sidebar.selectbox("Select a page", ["evadellaapp.py","evadellaapprawdata.py"])

    # Navigation Bar
    if page == "evadellaapp.py":
        st.title('📊 EvaDella App Dashboard')

        authenticator.logout("logout")

        # Navigation Bar
        selected = option_menu(
            menu_title = None,
            options = ["Operations", "Sales", "Inventory", "Staff Metrics"],
            icons = ["house", "book", "", ""],
            orientation = "horizontal",
        )

        # config = toml.load("config.toml")
        mysql_host = os.environ.get('localhost')
        mysql_user = os.environ.get('root')
        mysql_password = os.environ.get('swapna2021')
        mysql_database = os.environ.get('ecomm')

        mydb = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "swapna2021",
            database = "ecomm"
        )

        getOrderStatusDf = "SELECT * FROM ecomm.order_status"

        # todayOrdersDetails = "SELECT DATE(order_submit_dt_tm) as 'Date', order_id, total_amount FROM ecomm.orders WHERE DATE(order_submit_dt_tm) = CURDATE()"

        filterOrderStatusDf = "SElECT order_id, status_cd, estimated_time FROM ecomm.order_status"

        currentMonthOrders = "SELECT COUNT(order_id) as 'No Of Orders', order_id, coupon_applied, DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders WHERE MONTH(order_submit_dt_tm) = MONTH(CURDATE() - INTERVAL 1 MONTH) GROUP BY DATE(order_submit_dt_tm)"

        unShippedordersWeekCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as Date, DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 1 WEEK)) GROUP BY DATE(order_submit_dt_tm)"

        unShippedordersByDaysCount = "select DATE(order_submit_dt_tm) as 'Date', order_id, COUNT(order_id) as 'No Of Orders' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( CURDATE() - INTERVAL 10 DAY ) GROUP BY Date"

        ordersLastdaysCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from ecomm.orders where orders.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 10 DAY)) GROUP BY DATE(order_submit_dt_tm)"

        unShippedordersMonthCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 1 MONTH)) GROUP BY DATE(order_submit_dt_tm)"

        unShippedOrdersMonthCount1 = "select DATE(order_submit_dt_tm) as 'Date', status_cd, customer_id from orders o, order_status os WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') GROUP BY order_submit_dt_tm"

        ordersOfOneMonth= "SELECT os.order_id, os.status_cd, os.last_update_dt_tm as order_date_time, os.staff_cd FROM order_status os WHERE os.last_update_dt_tm >= CURRENT_DATE - INTERVAL 1 MONTH"


        if selected == "Operations":

            # css applied
            with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

            # columns for partition
            col5, col6 = st.columns(2)

            with col5:

                st.subheader("Order Count By Status")

                orderCountByStatus = "SELECT DATE(order_track_update_time) as 'Date', status_cd, order_id FROM ecomm.order_status WHERE order_status.order_track_update_time != 0"

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

                todayOrdersDetails = "SELECT DATE(order_submit_dt_tm) as 'Date', ROUND(COUNT(order_id)) as 'Count', ROUND(SUM(IFNULL(total_amount, 0))) as 'Amount' FROM ecomm.orders WHERE DATE(order_submit_dt_tm) = CURDATE()"

                todayOrdersDetailsDf = pd.read_sql_query(todayOrdersDetails, mydb)
                # convert_dict = {'Count': int, 'Amount' :int}
                # todayOrdersDetailsDf = todayOrdersDetailsDf.astype(convert_dict)
                todayOrdersDetailsDf.iloc[0, 0] = 'Today Orders'
                todayOrdersDetailsDf['Orders'] = todayOrdersDetailsDf['Date'].astype(str)
                todayOrdersDetailsDf = todayOrdersDetailsDf.drop('Date', axis=1)


                averageOrdersBy30Days = "SELECT DATE(order_submit_dt_tm) as 'Date', ROUND(COUNT(order_id)/COUNT(DISTINCT DATE(order_submit_dt_tm))) as 'Count', ROUND(AVG(total_amount)) as 'Amount' FROM ecomm.orders WHERE DATE(order_submit_dt_tm) >= (CURDATE()- INTERVAL 1 MONTH)"

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

            col10, col11 = st.columns(2)

            with col10:
                st.subheader("Orders By OrderStatus By Week, Month, Year")

                option = st.selectbox(
                '',
                ('', 'Week', 'Month', 'Year'))

                def week():

                    ordersWithStatusWeek = "SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd FROM ecomm.order_status WHERE  order_track_update_time >= CURDATE() - INTERVAL 1 WEEK"
                    
                    orderStatusWeekData = pd.read_sql_query(ordersWithStatusWeek, mydb)
                    def highlight_cell(val, column):
                        if column == column == 'status_cd' and val == 'PAID':
                            return 'color: blue'
                        elif column == 'status_cd' and val == 'Delivered':
                            return 'color: green'
                        elif column == 'status_cd' and val == 'Shipped':
                            return 'color: yellow'
                        elif column =='status_cd' and val != 'Delivered':
                            return 'color: red'
                        else:
                            return ''
                    orderStatusWeekDataDF = orderStatusWeekData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)

                    st.dataframe(orderStatusWeekDataDF)
                    # st.write('You selected:', option)

                def month():

                    ordersWithStatusMONTH = "SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd FROM ecomm.order_status WHERE  order_track_update_time >= CURDATE() - INTERVAL 1 MONTH"

                    orderStatusMonthData = pd.read_sql_query(ordersWithStatusMONTH, mydb)
                    def highlight_cell(val, column):
                        if column == column == 'status_cd' and val == 'PAID':
                            return 'color: blue'
                        elif column == 'status_cd' and val == 'Delivered':
                            return 'color: green'
                        elif column == 'status_cd' and val == 'SHIPPED':
                            return 'color: yellow'
                        elif column =='status_cd' and val != 'Delivered':
                            return 'color: red'
                        else:
                            return ''

                    orderStatusMonthDataDF = orderStatusMonthData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)
                    st.dataframe(orderStatusMonthDataDF)

                # def year():
                #     orderStatusYearData = pd.read_sql_query(ordersWithStatusYear, mydb)
                #     def highlight_cell(val, column):
                #         if column == 'status_cd' and val == 'PAID':
                #             return 'color: blue'
                #         elif column == 'status_cd' and val == 'Delivered':
                #             return 'color: green'
                #         elif column == 'status_cd' and val == 'Shipped':
                #             return 'color: yellow'
                #         elif column =='status_cd' and val != 'Delivered':
                #             return 'color: red'
                #         else:   
                #             return ''
                #     orderStatusYearDataDF = orderStatusYearData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)

                def year():
                    # Load the threshold data from Excel
                    thresholdData = pd.read_excel('Task/threshold_data.xlsx')
                    
                    ordersWithStatusYear = "SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd FROM ecomm.order_status WHERE (order_track_update_time != 0 OR last_update_dt_tm != 0) AND order_track_update_time >= CURDATE() - INTERVAL 1 YEAR"

                    # Read the orders data from SQL query
                    orderStatusYearData = pd.read_sql_query(ordersWithStatusYear, mydb)
                    
                    def highlight_cell(val, column):
                        if column == 'status_cd' and val == 'PAID':
                            return 'color: ' + thresholdData.loc[(thresholdData['Name'] == "status_cd") & (thresholdData['Threshold Value'] == "blue"), 'Threshold Value'].values[0]
                        elif column == 'status_cd' and val == 'Delivered':
                            return 'color: ' + thresholdData.loc[(thresholdData['Name'] == "status_cd") & (thresholdData['Threshold Value'] == "green"), 'Threshold Value'].values[0]
                        elif column == 'status_cd' and val == 'SHIPPED':
                            return 'color: ' + thresholdData.loc[(thresholdData['Name'] == "status_cd") & (thresholdData['Threshold Value'] == "yellow"), 'Threshold Value'].values[0]
                        elif column == 'status_cd' and val != 'Delivered':
                            return 'color:red'
                        
                        # elif column in thresholdData.columns:
                        #     threshold = thresholdData.loc[(thresholdData['Column'] == column), 'Threshold'].values[0]
                        #     if val >= threshold:
                        #         return 'color: ' + threshold
                        #     else:
                        #         return ''
                        else:
                            return ''
                    
                    orderStatusYearDataDF = orderStatusYearData.style.apply(lambda x: [highlight_cell(val, column) for val, column in zip(x, x.index)], axis=1)

                    st.dataframe(orderStatusYearDataDF)

                option_function_map = {
                    'Week' : week,
                    'Month' : month,
                    'Year' : year,

                }

                selected_function = option_function_map.get(option)
                if selected_function:
                    selected_function()
            
            with col11:

                st.subheader("Orders Delay")

                orderstatusByThreshould = "SELECT os.order_id, os.status_cd, os.last_update_dt_tm, os.staff_cd FROM order_status os JOIN orders o ON os.order_id = o.order_id JOIN thresholds tt ON tt.name = os.status_cd WHERE os.order_track_ref = (SELECT MAX(order_track_ref) FROM order_status WHERE order_id = os.order_id) AND DATEDIFF(CURRENT_DATE, os.last_update_dt_tm) > tt.value"

                delayOrders = pd.read_sql(orderstatusByThreshould, mydb)

                delayOrdersDf = pd.read_sql(ordersOfOneMonth, mydb)

                def highlight_red(row):
                    if row['order_date_time'] + timedelta(minutes=15) == delayOrdersDf.iloc[row.name]['order_date_time'] and row['status_cd'] == delayOrdersDf.iloc[row.name]['status_cd']:
                        return ['background-color: red'] * len(row)
                    return [''] * len(row)


                styled_data = delayOrdersDf.style.apply(highlight_red, axis=1)

                st.dataframe(styled_data)



        if selected == "Sales":

            # css applied
            with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

            # columns for partition
            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.subheader("Total No Of Orders")

                ordersCount = "SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" 

                ordersDf = pd.read_sql(ordersCount, mydb)
                totalOrders = sum(ordersDf['No Of Orders'])
                st.metric("", "")
                st.markdown('<a href="http://localhost:8501/evadellaapprawdata" target="_self" >' + str(totalOrders) +'</a>',unsafe_allow_html = True)

            with col2:
                st.metric(st.text_input(''),  value='')

            with col3:
                st.subheader("Total Amount")

                getOrdersDf = "SELECT * FROM ecomm.orders"

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

                ordersCountByCoupon = "select coupon_applied, count(order_id) as 'No Of Orders' from ecomm.orders where orders.coupon_applied <> '0' GROUP BY coupon_applied"

                ordersCountByCouponDf = pd.read_sql_query(ordersCountByCoupon, mydb)
                optionSelect = st.multiselect("Coupon Applied", options= ordersCountByCouponDf['coupon_applied'].unique(), 
                                            default = ordersCountByCouponDf['coupon_applied'].unique())
                appliedCoupon = ordersCountByCouponDf.query("coupon_applied == @optionSelect")

                st.table(appliedCoupon)

            # columns for partition
            col7, col8, col9 = st.columns(3)

            with col7:
                st.subheader("Orders By AmountRange")

                ordersCountByTotalAmount5 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 1000"

                ordersCountByTotalAmount4 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 500 and orders.total_amount >= 1000"

                ordersCountByTotalAmount3 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 300 and orders.total_amount >= 500"

                ordersCountByTotalAmount2 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 100 and orders.total_amount >= 300"

                ordersCountByTotalAmount1 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount <= 100"

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

                ordersCount = "SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" 

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

            ordersLastMonthCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from ecomm.orders where orders.order_submit_dt_tm >= ( CURDATE() - INTERVAL 1 MONTH) GROUP BY DATE(order_submit_dt_tm)"

            ordersLastMonthCountDf = pd.read_sql(ordersLastMonthCount, mydb)
            fig = px.pie(ordersLastMonthCountDf, values='No Of Orders', names='Date')

            st.plotly_chart(fig)


        if selected == "Staff Metrics":

             # css applied
            with open('C:/Users/ADMIN_2/Python_Giridhar/App Analytics/Analytics/databasestreamlit/Task/static/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

            # columns for partition
            col1, col2 = st.columns(2)

            with col2:

                st.subheader("Target Orders Given To Staff")

                ordersByStaffAction = "SELECT os.staff_cd, s.staff_name, DATE(os.last_update_dt_tm) as Date, COUNT(os.order_id) as orderscount, opr.staff_role FROM order_status os JOIN op_staff s ON os.staff_cd = s.staff_cd JOIN op_staff_role r ON s.op_staff_id = r.op_staff_id JOIN op_role opr ON r.role_id = opr.role_id GROUP BY os.staff_cd"

                ordersByStaffActionDf = pd.read_sql(ordersByStaffAction, mydb)

                thresholdData = pd.read_excel('Task/sample_data.xlsx')

                # Create a dictionary from the threshold table
                threshold_dict = dict(zip(thresholdData['Name'], thresholdData['Threshold Value']))

                # Function to apply color to cells based on threshold values
                def color_status_cd(row):

                    staff_cd = row['staff_cd'] 
                    print(staff_cd)
                    orderscount = row['orderscount']

                    if staff_cd in threshold_dict and orderscount >= threshold_dict[staff_cd]:
                        return ['color: green'] * len(row)
                    else:
                        return ['color: red'] * len(row)

                # Apply the style to the entire DataFrame
                styleed_table = ordersByStaffActionDf.style.applymap(lambda row: color_status_cd(row), subset=['orderscount', 'staff_cd'])

                # Display the updated table in Streamlit
                st.dataframe(ordersByStaffActionDf)



    if page == "evadellaapprawdata.py":

        st.title('Raw Data To Home Page')

        # authenticator.logout("logout")

        st.subheader('Total Orders Details')

        # unShippedOrdersMonthCountDf1
        ordersDf = pd.read_sql(ordersCount, mydb)

        totalOrders = sum(ordersDf['No Of Orders'])

        st.metric("Total No Of Orders", totalOrders)

        st.dataframe(ordersDf)
