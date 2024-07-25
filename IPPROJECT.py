
import mysql.connector as sql
from mysql.connector import Error


#Password
user_name,pw = 'aakash','abc_123'
#database name
db = "ShoeBill"
#table
tbl = "Bills(shoe_code varchar(5) Primary key, brand_name varchar(15), customer_name varchar(40), customer_num varchar(10), customer_address varchar(60), amount float)"
#queries
DEF_queries = ['drop database '+db,
               'create database '+db,
               'use '+db,
               'CREATE TABLE '+tbl,
              ]


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = sql.connect(
            host = host_name,
            user = user_name,
            passwd = 'abc_1234',
        )
        print("MySQL Database connection successful")

    except Error as err:
        print(f"Error:'{err}'")
    return connection


#Create Database
def create_database(connection):
    try:
        #execute_query(connection, DEF_queries[0])
        #uncomment this ^ to delete the current database
        execute_query(connection, DEF_queries[1])
    except Error as err:
        print(f"Error:'{err}")


#Create Table
def create_table(connection):
    try:
        execute_query(connection, DEF_queries[2])
        execute_query(connection, DEF_queries[3])
    except Error as err:
        print(f"Error:'{err}")


#This is where queries go for execution
def execute_query(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print(f"Successfully executed '{query}'")
    except Error as err:
        print(f"Error:'{err}'")

def login(connection):
    name = input('Enter Username:')
    passwd = input('Enter Password:')

    if name == user_name and passwd == pw:
        print('access Granted...')
        print('')
        print('')
        print(' 1 == shoe billing')
        print(' 2 == look up past sales')
        cur_action = input('Choose: ')
        if cur_action == '1':
            shoe_billing(connection)
        if cur_action == '2':
            lookup(connection)
    else:
        print('either username or password is incorrect')


def shoe_billing(connection):
    print("               shoe Billing          ")
    shoe_cd = input('Enter shoe code:')
    brand = input('Enter brand name:')
    name = input('Enter customer name:')
    num = input('Enter customer phone no.:')
    address = input('Enter customer address:')
    amount = input('Enter amount:')
    query = f"insert into Bills values ('{shoe_cd}','{brand}','{name}','{num}','{address}','{amount}')"
    execute_query(connection,query)


def lookup(connection):
    cursor = connection.cursor()
    bill_no = input('enter the code no.')
    cursor.execute(f"select * from bills where shoe_code = '{bill_no}'")
    data = cursor.fetchall()
    print("Shoe code:", data[0][0])
    print("brand name:", data[0][1])
    print("customer name:", data[0][2])
    print("customer number:", data[0][3])
    print("customer detail:", data[0][4])
    print("amount:", data[0][5])


#Starts execution here
connection = create_server_connection("localhost","root",pw)
create_database(connection)
create_table(connection)
login(connection)


