import sqlite3
import os
import csv
import pwinput
import pandas as pd
from sqlite3 import Error
from tkinter import *
from tkcalendar import Calendar
# sqlite3 is a python module that is used to create and manage the sqlite database and its tables
# os is a python module that is used to interact with the operating system
# csv is a python module that is used to read and write the data into the csv file (comma separated values)
# pwinput is a python module that is used to hide the password entered by the user while logging in
# pandas is a python module that is used to read the data from the csv file
# import error from sqlite3 module is used to handle the errors that are generated while executing the code
# tkinter is a python module that is used to create the graphical user interface
# tkcalendar is a python module that is used to create the calender widget
txt = "Welcome to smart farm management system"
print(txt.center(140, " "))
print(" ")
print("1. Farmer side")
print("2. Customer side")
choice = int(input("Enter your choice: "))
print(" ")
if choice == 1:
    # entering into farmer section of the code
    print("1. To create farmer account")
    print("2. To login as a farmer")
    choice = int(input("Enter your choice: "))
    print(" ")
    conn = sqlite3.connect('farmer_database.db')
# making connection with the farmers database
    cursor = conn.cursor()
    conn.commit()
    conn.close()
    if choice == 1:
        if os.path.exists('farmers_database.db'):
            conn = sqlite3.connect('farmers_database.db')
            c = conn.cursor()
        else:
            conn = sqlite3.connect('farmers_database.db')
            c = conn.cursor()
# c.execute is used to execute the sql queries and create a table with the given columns
# conn.commit() is used to save the changes made to the database
            c.execute(
                '''CREATE TABLE farmers (username text, password text, state text, contact text,area text,trust_score text)''')
        print("Enter details to create an account")
        username = input("Enter your username: ")
        password = pwinput.pwinput("Enter your password: ", "*")
        state = input("Enter your state: ")
        contact = input("Enter your contact number: ")
        area = input("Enter your area of farm: ")
        trust_score = 0
# c.execute is used to execute the sql queries and insert the values into the table
        c.execute("INSERT INTO farmers VALUES (?, ?, ?, ?, ?,?)",
                  (username, password, state, contact, area, trust_score))
        conn.commit()
        txt = "Account created"
        print(txt.center(140, " "))
        # print("Exporting data into CSV............")
# cursor is used to execute the sql queries and fetch the data from the database
        cursor = conn.cursor()
        cursor.execute("select * from farmers")
# csv.writer is used to write the data into the csv file
        with open('farmers_database.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
# os.getcwd() is used to get the current working directory
        dirpath = os.getcwd() + "/farmers_database.csv"
        print("Data has been stored in our database")
        # print csv data
        # with open(dirpath, 'r') as file:
        #     reader = csv.reader(file)
        #     for row in reader:
        #         print(row)
# conn.close() is used to close the connection with the database after the execution of the code is completed
        conn.close()
    elif choice == 2:
        # entering into the farmer login section of the code
        data = pd.read_csv("farmers_database.csv")
        user = input("Enter your username: ")
        password = pwinput.pwinput("Enter your password: ", "*")
# checking if the username and password entered by the user is present in the database or not
        if user in data['username'].values and password in data['password'].values:
            print("You are logged in")
            txt = "Welcome to the farmer's dashboard"
            print(txt.center(140, " "))
            print("1. Is there any previous crop that you have grown?")
# asking the farmer if there is any previous crop that he has grown on the land and whose details are present in the database
            choice = int(input("Enter your choice: 1 for yes and 2 for no: "))
            if choice == 1:
                # yes then delete previous crop details from database
                conn = sqlite3.connect('details_database.db')
                c = conn.cursor()
                c.execute("DELETE FROM details WHERE username = ?", (user,))
                conn.commit()
                conn.close()
                print("Previous crop details have been removed from the database")
# also delete previous crop details from csv
                df = pd.read_csv("details_database.csv")
                df = df[df.username != user]
                df.to_csv("details_database.csv", index=False)
# once the previous details are deleted then add the details of the current crop that is being grown
# make connection with the details database and create a table with the given columns
                print("Add details of the current crop that you are growing")
                if os.path.exists('details_database.db'):
                    conn = sqlite3.connect('details_database.db')
                    c = conn.cursor()
                else:
                    conn = sqlite3.connect('details_database.db')
                    c = conn.cursor()
                    c.execute(
                        '''CREATE TABLE details (username text,crop text, sowing_date text, expected_harvest_date text, expected_yield text, alerts text)''')
                username = user
                crop = input("Enter the crop variety that you are growing: ")
# accept date from calender and store it in a variable
# Import Required Library
# Create Object
                root = Tk()
# Set geometry
                root.geometry("400x400")
# Add Calendar
                cal = Calendar(root, selectmode='day',
                               year=2023, month=4, day=14)
                cal.pack(pady=20)

                def grad_date():
                    date.config(text="Selected Date is: " + cal.get_date())
# Add Button and Label
                Button(root, text="Get Date", command=grad_date).pack(pady=20)
                date = Label(root, text="")
                date.pack(pady=20)
# Execute Tkinter
                root.mainloop()
                sowing_date = cal.get_date()
                print("Enter the sowing date of the crop:", sowing_date)
# again creating calender object to accept the expected harvest date of the crop from the farmer
                root = Tk()
                root.geometry("400x400")
                cal = Calendar(root, selectmode='day',
                               year=2023, month=4, day=14)
                cal.pack(pady=20)

                def grad_date():
                    date.config(text="Selected Date is: " + cal.get_date())
                Button(root, text="Get Date", command=grad_date).pack(pady=20)
                date = Label(root, text="")
                date.pack(pady=20)
                root.mainloop()
                expected_harvest_date = cal.get_date()
                print("Enter the sowing date of the crop:",
                      expected_harvest_date)
                # expected_harvest_date = input("Enter the Expected harvest date of the crop: ")
                expected_yield = input(
                    "Enter the Expected yield of the crop: ")
                alerts = input(
                    "Enter the Alerts related to pests and diseases: ")
                c.execute("INSERT INTO details VALUES (?, ?, ?, ?, ?, ?)", (user,
                          crop, sowing_date, expected_harvest_date, expected_yield, alerts))
                conn.commit()
                # print("Exporting data into CSV............")
                cursor = conn.cursor()
                cursor.execute("select * from details")
                with open('details_database.csv', 'w') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in cursor.description])
                    csv_writer.writerows(cursor)
                dirpath = os.getcwd() + "/details_database.csv"
                print("Data has been stored in our database")
                # print csv data
                # with open(dirpath, 'r') as file:
                #     reader = csv.reader(file)
                #     for row in reader:
                #         print(row)
                conn.close()
# if there is no previous crop that is grown on the land then directly add the details of the current crop that is being grown
            else:
                if os.path.exists('details_database.db'):
                    conn = sqlite3.connect('details_database.db')
                    c = conn.cursor()
                else:
                    conn = sqlite3.connect('details_database.db')
                    c = conn.cursor()
                    c.execute(
                        '''CREATE TABLE details (username text,crop text, sowing_date text, expected_harvest_date text, expected_yield text, alerts text)''')
                username = user
                crop = input("Enter the crop variety that you are growing: ")
                # sowing_date = input("Enter the sowing date of the crop: ")
                # expected_harvest_date = input("Enter the Expected harvest date of the crop: ")
# accept date from calender and store it in a variable
                root = Tk()
                root.geometry("400x400")
                cal = Calendar(root, selectmode='day',
                               year=2023, month=4, day=14)
                cal.pack(pady=20)

                def grad_date():
                    date.config(text="Selected Date is: " + cal.get_date())
                Button(root, text="Get Date", command=grad_date).pack(pady=20)
                date = Label(root, text="")
                date.pack(pady=20)
                root.mainloop()
                sowing_date = cal.get_date()
                print("Enter the sowing date of the crop:", sowing_date)
# again creating calender object to accept the expected harvest date of the crop from the farmer
                root = Tk()
                root.geometry("400x400")
                cal = Calendar(root, selectmode='day',
                               year=2023, month=4, day=14)
                cal.pack(pady=20)

                def grad_date():
                    date.config(text="Selected Date is: " + cal.get_date())
                Button(root, text="Get Date", command=grad_date).pack(pady=20)
                date = Label(root, text="")
                date.pack(pady=20)
                root.mainloop()
                expected_harvest_date = cal.get_date()
                print("Enter the sowing date of the crop:",
                      expected_harvest_date)
                expected_yield = input(
                    "Enter the Expected yield of the crop: ")
                alerts = input(
                    "Enter the Alerts related to pests and diseases: ")
                c.execute("INSERT INTO details VALUES (?, ?, ?, ?, ?, ?)", (user,
                          crop, sowing_date, expected_harvest_date, expected_yield, alerts))
                conn.commit()
                # print("Exporting data into CSV............")
                cursor = conn.cursor()
                cursor.execute("select * from details")
                with open('details_database.csv', 'w') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in cursor.description])
                    csv_writer.writerows(cursor)
                dirpath = os.getcwd() + "/details_database.csv"
                print("Data has been stored in our database")
                # print csv data
                # with open(dirpath, 'r') as file:
                #     reader = csv.reader(file)
                #     for row in reader:
                #         print(row)
                conn.close()
# entering into the customer login section of the code
else:
    print("1. To create customer account")
    print("2. To login as a customer")
    choice = int(input("Enter your choice: "))
# when choice is 1 then create a customer account
    if choice == 1:
        # make connection with the customers database and create a table with the given columns
        if os.path.exists('customers_database.db'):
            conn = sqlite3.connect('customers_database.db')
            c = conn.cursor()
        else:
            conn = sqlite3.connect('customers_database.db')
            c = conn.cursor()
            c.execute(
                '''CREATE TABLE customers (username text, password text, contact text)''')
        print(" ")
        print("Enter details to create an account")
        username = input("Enter your username: ")
        password = pwinput.pwinput("Enter your password: ", "*")
        contact = input("Enter your contact number: ")
        c.execute("INSERT INTO customers VALUES (?, ?, ?)",
                  (username, password, contact))
        conn.commit()
        txt = "Account created"
        print(txt.center(140, " "))
# once the account is created then export the data into a csv file
        # print("Exporting data into CSV............")
        cursor = conn.cursor()
        cursor.execute("select * from customers")
        with open('customers_database.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
        dirpath = os.getcwd() + "/customers_database.csv"
        # print("Data exported to CSV file")
        # print csv data
        # with open(dirpath, 'r') as file:
        #     reader = csv.reader(file)
        #     for row in reader:
        #         print(row)
        conn.close()
# when choice is 2 then login as a customer
    elif choice == 2:
        data = pd.read_csv("customers_database.csv")
        user = input("Enter your username: ")
        password = pwinput.pwinput("Enter your password: ", "*")
        if user in data['username'].values and password in data['password'].values:
            print("You are logged in")
            txt = "Welcome to the customer's dashboard"
            print(txt.center(140, " "))
            print("1. filter by crop")
            print("2. filter by state")
            n = int(input("Enter your choice: "))
# customer can select the farmer based on the crop that is available or the state where the farmer is located
# if the customer selects 1 then filter by crop
            if n == 1:
                crop_demand = input("Enter the crop variety that you need: ")
                data = pd.read_csv("details_database.csv")
                data1 = pd.read_csv("farmers_database.csv")
# read crop details from the details database and farmer details from the farmers database
# then filter the data based on the crop that is demanded by the customer
                if crop_demand in data['crop'].values:
                    print("Crop available")
                    print(data.loc[data['crop'] == crop_demand])
                    print("Details of the farmer")
                    n = int(input("Enter the index of the farmer: "))
                    name = data.loc[data['crop'] ==
                                    crop_demand, 'username'].values[n-1]
                    if name in data1['username'].values:
                        print(data1.loc[data1['username'] == name, [
                              'username', 'contact', 'state', 'trust_score']])
                else:
                    print("Crop not available")
# if the customer selects 2 then filter by state
            elif n == 2:
                state_demand = input(
                    "Enter the state where you need the crop: ")
                data = pd.read_csv("details_database.csv")
                data1 = pd.read_csv("farmers_database.csv")
                if state_demand in data1['state'].values:
                    print("Crop available")
                    print(data.loc[data1['state'] == state_demand])
                    print("Details of the farmer")
                    n = int(input("Enter the index of the farmer: "))
                    name = data.loc[data1['state'] ==
                                    state_demand, 'username'].values[n-1]
                    if name in data1['username'].values:
                        print(data1.loc[data1['username'] == name, [
                              'username', 'contact', 'state', 'trust_score']])
                else:
                    print("Crop not available")
        txt = "Hope you were able to contact the farmer"
        print(txt.center(140, " "))
# once you were able to contact the farmer then you can rate the farmer
        print("Please rate the farmer")
        print("Rate the farmer on a scale of 1 to 5 on the following parameters")
        print("1. To rate the farmer")
        print("2. To exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            crop_quality = int(input("Enter the rating for crop quality: "))
            service_provided = int(
                input("Enter the rating for service provided: "))
            trust_score = (crop_quality + service_provided)/2
            if os.path.exists('farmers_database.db'):
                conn = sqlite3.connect('farmers_database.db')
                c = conn.cursor()
            else:
                conn = sqlite3.connect('farmers_database.db')
                c = conn.cursor()
                c.execute(
                    '''CREATE TABLE farmers (username text, password text, contact text, area text, state text, trust_score text)''')
            data = pd.read_csv("farmers_database.csv")
            trust = data.loc[data['username'] == name, 'trust_score'].values[0]
            trust_score = (trust_score + trust)/2
            c.execute(
                "UPDATE farmers SET trust_score = ? WHERE username = ?", (trust_score, name))
            conn.commit()
            print("Trust score updated")
            # print("Exporting data into CSV............")
            cursor = conn.cursor()
            cursor.execute("select * from farmers")
            with open('farmers_database.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(cursor)
            dirpath = os.getcwd() + "/farmers_database.csv"
            # print("Data exported to CSV file")
            conn.close()
        elif choice == 2:
            txt = "Thank you for using our service"
            print(txt.center(140, " "))
            txt = "Hope to see you again"
            print(txt.center(140, " "))
            exit()
        else:
            print("Invalid choice")
            exit()
    else:
        print("Invalid choice")
        exit()
txt = "Thank you for using our service"
print(txt.center(140, " "))
