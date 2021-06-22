import pandas as pd
import random
from faker import Faker
from collections import defaultdict
from sqlalchemy import create_engine
import pymysql
import mysql.connector
# db_connection = mysql.connector.connect( host = 'localhost', user = 'root', passwd = 'ubuntumysql', database = 'DBMSProjectdb', auth_plugin = 'mysql_native_password')
# db_connection.close()
pymysql.install_as_MySQLdb()
fake_data = Faker()
dummy_data = defaultdict(list)
# ! COnnecting to the mysql server
connection = create_engine('mysql+pymysql://root:ubuntumysql@localhost:3306/DBMSProjectdb',echo = False)
# ids = [1022, 1090, 1107, 1101, 1197, 1105, 1006, 1077, 1017, 1165, 1108, 1167, 1015, 1156, 1003, 1086, 1118, 1191, 1047, 1185, 1062, 1194, 1200, 1097, 1046, 1192, 1082, 1134, 1005, 1151, 1163, 1071, 1188, 1037, 1140, 1135, 1137, 1174, 1133, 1055, 1016, 1155, 1012, 1067, 1007, 1144, 1026, 1175, 1019, 1060, 1193, 1085, 1145, 1132, 1113, 1089, 1123, 1160, 1196, 1106, 1054, 1110, 1142, 1036, 1187, 1035, 1028, 1183, 1138, 1184, 1025, 1117, 1040, 1068, 1161, 1143, 1159, 1094, 1104, 1080, 1168, 1136, 1162, 1103, 1084, 1031, 1180, 1111, 1122, 1109, 1139, 1098, 1114, 1087, 1128, 1199, 1176, 1169, 1152, 1172]
# ! Customers table

# * Structure
# * 1. First Name
# * 2. Last Name
# * 3. Date Of Birth
# * 4. Customer ID
# * 5. Email ID
ids = []
num = random.randint(1000, 1200)
for i in range(100):
    while num in ids:
        num = random.randint(1000, 1200)
    ids.append(num)
for i in range(100):
    dummy_data['first_name'].append(fake_data.first_name())
    dummy_data['last_name'].append(fake_data.last_name())
    dummy_data['Address'].append(fake_data.street_address())
    dummy_data['Date_of_Birth'].append(fake_data.date_between('-50y','-20y'))
    dummy_data['Customer_ID'].append(ids[i])
    dummy_data['Email_ID'].append(dummy_data['first_name'][i] + dummy_data['last_name'][i] + '@' + ''.join(random.sample(['gmail.com','outlook.com','yahoo.com'], 1)))
dummy_data_df = pd.DataFrame(dummy_data)
# print(dummy_data_df)
dummy_data_df.to_sql('Customers', con = connection)
# dummy_data_df['Customer_ID'].is_unique()
# print(dummy_data_df['Customer_ID'])

'''
SELECT Customer_ID, count(Customer_ID) FROM customers GROUP BY Customer_ID HAVING COUNT(Customer_ID) > 1;
'''
# print(ids)
# ! Products table
products_df = pd.read_csv('amaz.csv')
products_df.drop(['Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16'], axis = 1, inplace = True)
products_df.to_sql('Products', con = connection)
# ! Orders table
# * Structure
# * 1. Customer ID
# * 2. Product ID
# * 3. Quantity
# * 4. Price
# * 5. Tax
# * 6. Total Bill
# * 7. Payment Method
orders_dummy_data = defaultdict(list)
order_id = []
payment_methods = ['UPI','Debit Card','Credit Card','Net Banking', 'Cash on Delivery','EMI']
order_num = random.randint(5439,6782)
for i in range(100):
    while order_num in order_id:
        order_num = random.randint(5439,6782)
    order_id.append(order_num)
for i in range(100):
    orders_dummy_data['Order_ID'].append(order_id[i])
    orders_dummy_data['Customer_ID'].append(random.sample(dummy_data['Customer_ID'],1)[0])
    orders_dummy_data['Product_ID'].append(random.sample(products_df['ProductID'].tolist(),1)[0])
    orders_dummy_data['Quantity'].append(random.randint(1,10))
    orders_dummy_data['Price'].append(products_df['SellingPrice'][products_df['ProductID'] == orders_dummy_data['Product_ID'][i]].iloc[0])
    orders_dummy_data['Tax'].append((orders_dummy_data['Quantity'][i] * orders_dummy_data['Price'][i]) * 0.18)
    orders_dummy_data['Total_Bill'].append((orders_dummy_data['Quantity'][i] * orders_dummy_data['Price'][i]) + orders_dummy_data['Tax'][i])
    orders_dummy_data['Payment_Method'].append(random.sample(payment_methods,1)[0])
orders_dummy_data_df = pd.DataFrame(orders_dummy_data)
orders_dummy_data_df.to_sql('Orders', con = connection)
# ! Sellers Table
# * Seller_Name
# * Seller_ID
# * Seller_ContactNo
# * Email_ID
seller_dummy_data = defaultdict(list)
a = []
ii = fake_data.company()
for i in range(100):
    while ii in a:
        ii = fake_data.company()
    a.append(ii)
seller_ids = []
num = random.randint(1000, 1200)
for i in range(100):
    while num in seller_ids:
        num = random.randint(1000, 1200)
    seller_ids.append(num)
contact_no = []
number = fake_data.phone_number()
for i in range(100):
    while number in contact_no:
        number = fake_data.phone_number()
    contact_no.append(number)
for i in range(10):
    seller_dummy_data['Seller_Name'].append(random.sample(a,1))
    seller_dummy_data['Seller_ID'].append(seller_ids[i])
    seller_dummy_data['Seller_ContactNo'].append(random.sample(contact_no,1))
    seller_dummy_data['Email_ID'].append('customer.care@' + ''.join(seller_dummy_data['Seller_Name'][i]).replace(',','').replace(' ',''))
seller_dummy_data_df = pd.DataFrame(seller_dummy_data)
seller_dummy_data_df.to_sql('Sellers',con = connection)

# ! Logistics
# * Shipper_ID
# * Shipper_Name
# * Date
shipper_list = defaultdict(list)
shipper_ids = []
id = random.randint(5000,6000)
for i in range(100):
    while id in shipper_ids:
        id = random.randint(5000,6000)
    shipper_ids.append(id)
shipper_names = []
suffix = ["Shipping Company","Transport Corporation","Merchants","Shipping Services","Logistics Corporation","Shipping lines","Transport Company"]
name = fake_data.company() + ''.join(random.sample(suffix,1)[0])
for i in range(100):
    while name in shipper_names:
        name = fake_data.company() + " " + ''.join(random.sample(suffix,1)[0])
    shipper_names.append(name)
shipping_methods = []
methods = ['Airways','WaterWays','Roads','Railways']
method = ''.join(random.sample(methods,1))
for i in range(100):
    method = ''.join(random.sample(methods,1))
    shipping_methods.append(method)
for i in range(5):
    shipper_list['Shipper_ID'].append(shipper_ids[i])
    shipper_list['Shippment_Company_Name'].append(shipper_names[i])
    shipper_list['Mode_of_Shipment'].append(shipping_methods[i])
shipper_dummy_data_df = pd.DataFrame(shipper_list)
shipper_dummy_data_df.to_sql('Logistics',con = connection)
# ! Payment methods table
# * Payment_Method
# * Method_ID
payment_methods = {'UPI':1,'Debit Card':2,'Credit Card':3,'Net Banking':4,'Cash on Delivery':5,'EMI':6}
payment_method_list = defaultdict(list)
for i in range(6):
    payment_method_list['Payment_Method'].append(''.join(random.sample(payment_methods.keys(),1)))
    payment_method_list['Method_ID'].append(payment_methods[payment_method_list['Payment_Method'][i]])
payment_method_df = pd.DataFrame(payment_method_list)
payment_method_df.to_sql('Payment_Methods',con = connection)

# ! Invoices Tables
# * Invoice_ID
# * Order_ID
# * Customer_ID
# * Product_ID
# * Seller_ID
# * Price
# * Discount
# * Tax
# * Total
# * Payment method
# * Date
order_ids_ = []
o_ids = random.sample(orders_dummy_data['Order_ID'],1)[0]
for i in range(100):
    while o_ids in order_ids_:
        o_ids = random.sample(orders_dummy_data['Order_ID'],1)[0]
    order_ids_.append(o_ids)
invoices_list = defaultdict(list)
invoice_ids = []
ids = random.randint(100,500)
for i in range(100):
    while ids in invoice_ids:
        ids = random.randint(100,500)
    invoice_ids.append(ids)
seller_ids_ = []
ids_ = random.sample(seller_ids,1)
for i in range(100):
    while ids_ in seller_ids_:
        ids_ = random.sample(seller_ids,1)
    seller_ids_.append(ids_)
payment_methods = {'UPI':1,'Debit Card':2,'Credit Card':3,'Net Banking':4,'Cash on Delivery':5,'EMI':6}
shipping_dates = []
date = fake_data.date_between('-4M','today')
for i in range(100):
    while date in shipping_dates:
        date = fake_data.date_between('-6M','today')
    shipping_dates.append(date)
for i in range(100):
    invoices_list['Invoice_ID'].append(invoice_ids[i])
    invoices_list['Order_ID'].append(order_ids_[i])
    invoices_list['Customer_ID'].append(orders_dummy_data_df['Customer_ID'][orders_dummy_data_df['Order_ID'] == invoices_list['Order_ID'][i]].iloc[0])
    invoices_list['Product_ID'].append(orders_dummy_data_df['Product_ID'][orders_dummy_data_df['Order_ID'] == invoices_list['Order_ID'][i]].iloc[0])
    invoices_list['Seller_ID'].append(seller_ids_[i])
    invoices_list['Price'].append(orders_dummy_data_df['Price'][orders_dummy_data_df['Order_ID'] == invoices_list['Order_ID'][i]].iloc[0])
    invoices_list['Quantity'].append(orders_dummy_data_df['Quantity'][orders_dummy_data_df['Order_ID'] == invoices_list['Order_ID'][i]].iloc[0])
    invoices_list['Tax'].append((invoices_list['Price'][i] * invoices_list['Quantity'][i]) * 0.18)
    invoices_list['Discount'].append(((invoices_list['Price'][i] * invoices_list['Quantity'][i]) + invoices_list['Tax'][i]) * 0.1)
    invoices_list['Bill_Amount'].append(((invoices_list['Price'][i] * invoices_list['Quantity'][i]) + invoices_list['Tax'][i]) - invoices_list['Discount'][i])
    invoices_list['Payment_Method'].append(''.join(random.sample(payment_methods.keys(),1)))
    invoices_list['Method_ID'].append(payment_methods[invoices_list['Payment_Method'][i]])
    invoices_list['Date'].append(shipping_dates[i])
invoices_df = pd.DataFrame(invoices_list)
invoices_df.to_sql('Invoices',con = connection)