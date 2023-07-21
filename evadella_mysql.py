import mysql.connector
import os
import toml

# config = toml.load("config.toml")
mysql_host = os.environ.get('localhost')
mysql_user = os.environ.get('root')
mysql_password = os.environ.get('swapna2021')
mysql_database = os.environ.get('ecomm')

# @st.cache(hash_funcs={_mysql_connector.MySQL: my_hash_func})

mydb = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "swapna2021",
    database = "ecomm"
)

mydb.close()

getOrderStatusDf = "SELECT * FROM ecomm.order_status"

getOrdersDf = "SELECT * FROM ecomm.orders"

# todayOrdersDetails = "SELECT DATE(order_submit_dt_tm) as 'Date', order_id, total_amount FROM ecomm.orders WHERE DATE(order_submit_dt_tm) = CURDATE()"

todayOrdersDetails = "SELECT DATE(order_submit_dt_tm) as 'Date', ROUND(COUNT(order_id)) as 'Count', ROUND(SUM(IFNULL(total_amount, 0))) as 'Amount' FROM ecomm.orders WHERE DATE(order_submit_dt_tm) = CURDATE()"

averageOrdersBy30Days = "SELECT DATE(order_submit_dt_tm) as 'Date', ROUND(COUNT(order_id)/COUNT(DISTINCT DATE(order_submit_dt_tm))) as 'Count', ROUND(AVG(total_amount)) as 'Amount' FROM ecomm.orders WHERE DATE(order_submit_dt_tm) >= (CURDATE()- INTERVAL 1 MONTH)"

orderCountByStatus = "SELECT DATE(order_track_update_time) as 'Date', status_cd, order_id FROM ecomm.order_status WHERE order_status.order_track_update_time != 0"

filterOrderStatusDf = "SElECT order_id, status_cd, estimated_time FROM ecomm.order_status"

ordersCount = "SELECT COUNT(order_id) as 'No Of Orders', order_id, DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders GROUP BY DATE(order_submit_dt_tm)" 

currentMonthOrders = "SELECT COUNT(order_id) as 'No Of Orders', order_id, coupon_applied, DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' FROM ecomm.orders WHERE MONTH(order_submit_dt_tm) = MONTH(CURDATE() - INTERVAL 1 MONTH) GROUP BY DATE(order_submit_dt_tm)"

unShippedordersWeekCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as Date, DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 1 WEEK)) GROUP BY DATE(order_submit_dt_tm)"

unShippedordersByDaysCount = "select DATE(order_submit_dt_tm) as 'Date', order_id, COUNT(order_id) as 'No Of Orders' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( CURDATE() - INTERVAL 10 DAY ) GROUP BY Date"

ordersLastMonthCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from ecomm.orders where orders.order_submit_dt_tm >= ( CURDATE() - INTERVAL 1 MONTH) GROUP BY DATE(order_submit_dt_tm)"

ordersLastdaysCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', DAYNAME(order_submit_dt_tm) as 'Day Name', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from ecomm.orders where orders.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 10 DAY)) GROUP BY DATE(order_submit_dt_tm)"

ordersCountByCoupon = "select coupon_applied, count(order_id) as 'No Of Orders' from ecomm.orders where orders.coupon_applied <> '0' GROUP BY coupon_applied"

unShippedordersMonthCount = "select order_id, COUNT(order_id) as 'No Of Orders', DATE(order_submit_dt_tm) as 'Date', DAY (order_submit_dt_tm) as 'Day', MONTHNAME(order_submit_dt_tm) as 'Month Name', YEAR(order_submit_dt_tm) as 'Year' from orders o WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') AND o.order_submit_dt_tm >= ( DATE_SUB(NOW(), INTERVAL 1 MONTH)) GROUP BY DATE(order_submit_dt_tm)"

unShippedOrdersMonthCount1 = "select DATE(order_submit_dt_tm) as 'Date', status_cd, customer_id from orders o, order_status os WHERE o.status <> 'OPEN' AND o.order_id NOT IN (select distinct os.order_id from order_status os WHERE os.status_cd = 'Shipped') GROUP BY order_submit_dt_tm"

ordersCountByTotalAmount5 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 1000"

ordersCountByTotalAmount4 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 500 and orders.total_amount >= 1000"

ordersCountByTotalAmount3 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 300 and orders.total_amount >= 500"

ordersCountByTotalAmount2 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount > 100 and orders.total_amount >= 300"

ordersCountByTotalAmount1 = "select COUNT(order_id) as 'No Of Orders' from ecomm.orders where orders.total_amount <= 100"

ordersWithStatusWeek = "SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd FROM ecomm.order_status WHERE  order_track_update_time >= CURDATE() - INTERVAL 1 WEEK"

ordersWithStatusMONTH = "SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd FROM ecomm.order_status WHERE  order_track_update_time >= CURDATE() - INTERVAL 1 MONTH"

ordersWithStatusYear = "SELECT DATE(order_track_update_time) as Ordered_date, order_id, status_cd, DATE(estimated_time) as Estimated_date, staff_cd FROM ecomm.order_status WHERE (order_track_update_time != 0 OR last_update_dt_tm != 0) AND order_track_update_time >= CURDATE() - INTERVAL 1 YEAR"

orderstatusByThreshould = "SELECT os.order_id, os.status_cd, os.last_update_dt_tm, os.staff_cd FROM order_status os JOIN orders o ON os.order_id = o.order_id JOIN thresholds tt ON tt.name = os.status_cd WHERE os.order_track_ref = (SELECT MAX(order_track_ref) FROM order_status WHERE order_id = os.order_id) AND DATEDIFF(CURRENT_DATE, os.last_update_dt_tm) > tt.value"

ordersByStaffAction = "SELECT os.staff_cd, s.staff_name, DATE(os.last_update_dt_tm) as Date, COUNT(os.order_id) as orderscount, opr.staff_role FROM order_status os JOIN op_staff s ON os.staff_cd = s.staff_cd JOIN op_staff_role r ON s.op_staff_id = r.op_staff_id JOIN op_role opr ON r.role_id = opr.role_id GROUP BY os.staff_cd"

ordersOfOneMonth= "SELECT os.order_id, os.status_cd, os.last_update_dt_tm as order_date_time, os.staff_cd FROM order_status os WHERE os.last_update_dt_tm >= CURRENT_DATE - INTERVAL 1 MONTH"










