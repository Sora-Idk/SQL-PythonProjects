import mysql.connector as sql
from mysql.connector import Error


def create_server_connection(user_password, host_name="localhost", user_name="root"):
    con = None
    try:
        con = sql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print("MySQL Database connection successful")

    except Error as err:
        print(f"Error:'{err}'")
    return con


def execute_query(query, fetch=False):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        # print(f"Successfully executed "{query}"")
    except Error as err:
        print(f"Error:'{err}'")

    if fetch:
        return cursor.fetchall()


#Create Database
def create_database():
    try:
        #execute_query(f"DROP DATABASE {db_name}")
        #uncomment this ^ to delete the current database
        execute_query(f"CREATE DATABASE {db_name}")
        print("database created")
    except Error as err:
        print(f"Error:'{err}'")


#Create Table
def create_table():
    try:
        execute_query(f"USE {db_name}")
        for each_table in tables:
            execute_query(f"CREATE TABLE {each_table}")

    except Error as err:
        print("table could not be created")
        print(f"Error:'{err}'")


#register,login users
users = {"admin":"abc123"}


def login_user():
    us_name = input("enter username: ")
    pw = input("enter password")  # getpass lib should be used.
    if users[us_name] == pw:
        return True
    elif users[us_name] != pw:
        return False


def register_user():
    us_name = input("enter username: ")
    pw = input("set password: ")
    if pw == input("repeat password: "):
        users[us_name] = pw
        print(f"Successfully registered user {us_name}")


#add, remove, getinfo doctors
def register_staff():
    name = input("Employee Name: ")
    speciality = input("Enter Speciality")
    age = int(input("Age(integer) "))
    address = input("Address: ")
    contact = input("Contact: ")
    monthly_salary = round(float(input("Enter Monthly Salary: ")),2)
    query = f"INSERT INTO {table_names[0]} VALUES ('{name}','{speciality}',{age},'{address}','{contact}',{monthly_salary})"
    execute_query(query)


def get_info_staff():
    id_ = input('Enter ID of Employee(enter "nil" if not known): ')
    if id_ == 'nil':
        name = input('Enter name of Employee: ')
        query = f"SELECT * FROM {table_names[0]} WHERE Name = '{name}';"
        print(execute_query(query,fetch=True))
    else:
        query = f"SELECT * FROM {table_names[0]} WHERE ID = {id_};"
        print(execute_query(query, fetch=True))


def remove_staff():
    id_ = input('enter patient ID: ')
    query = f"SELECT * FROM {table_names[0]} WHERE ID = {id_};"
    print(execute_query(query, fetch=True))
    if input('delete this y/n? ') == 'y':
        query = f"DELETE FROM {table_names[0]} WHERE ID = {id_}"
    execute_query(query)


#add, remove, getinfo patients
def register_patient():
    name = input("Patient Name: ")
    age = int(input("Patient Age(integer) "))
    gender = input("Gender: ")
    address = input("Address: ")
    contact = input("Contact: ")
    query = f"INSERT INTO {table_names[1]} (Name, Age, Gender, Address, Contact) VALUES ('{name}',{age},'{gender}','{address}','{contact}')"
    execute_query(query)
    print(execute_query(f"SELECT * FROM {table_names[1]} WHERE Name = '{name}' AND Age = {age} AND Address = '{address}'", fetch=True))


def get_info_patient():
    id_ = input('Enter ID of Patient(enter "nil" if not known): ')
    if id_ == 'nil':
        name = input('Enter name of Patient: ')
        query = f"SELECT * FROM {table_names[1]} WHERE Name = '{name}';"
        print(execute_query(query,fetch=True))
    else:
        query = f"SELECT * FROM {table_names[1]} WHERE ID = {id_};"
        print(execute_query(query, fetch=True))


def remove_patient():
    id_ = input('enter patient ID: ')
    query = f"SELECT * FROM {table_names[1]} WHERE ID = {id_};"
    print(execute_query(query, fetch=True))
    if input('delete this y/n? ') == 'y':
        query = f"DELETE FROM {table_names[1]} WHERE ID = {id_}"
    execute_query(query)


def main():
    create_database()
    create_table()
    print("""
    Choose Action(Enter the seriel no. of the action you want to perform):
    1)Login
    2)Register""")

    check = None

    inp = int(input())
    if inp == 1:
        check = login_user()
    elif inp == 2:
        register_user()
        check = login_user()

    while check:
        print("""
                Choose Action:
                1)edit/check patient data
                2)edit/check staff data""")
        inp = int(input())
        if inp == 1:
            print("""
                            Choose Action:
                            1)Register Patient
                            2)Get Patient Info
                            3)Remove Patient Info""")
            inp = int(input())
            if inp == 1:
                register_patient()
            elif inp == 2:
                get_info_patient()
            elif inp == 3:
                remove_patient()
        elif inp == 2:
            print("""
                            Choose Action:
                            1)Register Employee
                            2)Get Employee Info
                            3)Remove Employee Info""")
            if inp == 1:
                register_staff()
            elif inp == 2:
                get_info_staff()
            elif inp == 3:
                remove_staff()
    else:
        print("Invalid Login Info")


db_name = "HMS"

table_names = ['HospitalStaff',"Patients"]

#CREATE TABLE PART OF SYNTAX IS IN create_table()
tables = [f" {table_names[0]} (ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,"
          f"Name VARCHAR(255) NOT NULL,"
          f"Speciality VARCHAR(100),"
          f"Age INT,Address VARCHAR(255),"
          f"Contact VARCHAR(20),"
          f"MonthlySalary DECIMAL(10, 2));""",

          f"""{table_names[1]} (ID INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
          Name VARCHAR(255) NOT NULL,
          Age INT,
          Gender VARCHAR(10),
          Address VARCHAR(255),
          Contact VARCHAR(20)
);"""]

connection = create_server_connection(user_password='Aku@1234')  # sql password
main()
