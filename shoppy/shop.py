#file which contains classes for printing data, user creation and admin functions

import pickle, os, json
import random, copy
import smtplib
from datetime import date
import time
import pandas as pd
import mysql.connector

if os.name == 'posix':
    systemclear = 'clear'
else:
    systemclear = 'cls'

#class which contains static methods responsible for printing data
class PrintProducts:

    #method which prints all the categories avaiable for purchase and allows user to choose the category
    @staticmethod
    def categories():
        items_available = json.load(open(os.getcwd() + '/items.json', 'r'))
        os.system(systemclear)
        print('Categories')
        for itr, key in zip(range(len(items_available)), list(items_available.keys())):
            print(str(itr+1) + '.', key.title())
        print()
        print('Enter the corresponding number to look into the categories: ', end = '')
        response = int(input())
        return list(items_available.keys())[response-1]

    #method which prints all the items which are available in the selected category and allows user to choose the items
    @staticmethod
    def products(category):
        items_available = json.load(open(os.getcwd() + '/items.json', 'r'))
        os.system(systemclear)
          
        print('Products available in', category)
        for itr, key in zip(list(range(len(items_available.get(category)))), list(items_available.get(category).keys())):
            print(str(itr+1) + '.', key.title())
        print()
        print('Enter the corresponding number to look into the product: ', end = '')
        response = int(input())
        return (list(items_available.get(category).keys())[response-1])

    #method which prints all the item description and allows the user to choose the quantity
    @staticmethod
    def item_desc(category, item):
        items_available = json.load(open(os.getcwd() + '/items.json', 'r'))
        os.system(systemclear)
          
        print('Product:', item.title())
        print('Description:', items_available.get(category).get(item).get('description'))
        print('Price:', items_available.get(category).get(item).get('price'))
        if items_available.get(category).get(item).get('quantity') == 0:
            print('No stocks available')
            print('Press enter to return to home ', end = '')
            input()
            
        else:
            print('In stock:', items_available.get(category).get(item).get('quantity'))
            print('\nEnter the required quantity: ', end = '')
            quantity = int(input())

            print()
            return quantity


#class which is responsible for user creation, ordering, cancelling and displaying cart items
#User class inherits PrintProducts class
class User(PrintProducts):
    def __init__(self, name, mailid, password):
        self.name = name
        self.mailid = mailid 
        self.password = password
        self.cart = {}
        self.discount = False
        self.country = ''

    #method for ordering the items
    def order(self):
        while 1:
            items_available = json.load(open(os.getcwd() + '/items.json', 'r'))
            category = super().categories()
            item = super().products(category)
            quantity = super().item_desc(category, item)
            if quantity != None and quantity != 0: 
                self.cart[category] = self.cart.get(category, {})
                self.cart[category][item] = self.cart[category].get(item, 0) + quantity
                items_available[category][item]['quantity'] -= self.cart[category][item]
                json.dump(items_available, open(os.getcwd() + '/items.json', 'w'), indent=4)

                try:
                    db = mysql.connector.connect(host = 'mydb', user = 'root', password = 'root', port = 3306)
                    my_cursor = db.cursor()
                    my_cursor.execute('use shop')
                    my_cursor.execute('select * from salesreport')
                    df = my_cursor.fetchall()
                    if not df:
                        query = 'insert into salesreport(id, Username, Product, Category, Quantity, Country, Order_date, Order_time) values(%s, %s, %s, %s, %s, %s, %s, %s)'
                        values = (1, self.name, item, category, quantity, self.country, date.today(), time.strftime("%H:%M:%S", time.localtime()))
                    else:
                        query = 'insert into salesreport(Username, Product, Category, Quantity, Country, Order_date, Order_time) values(%s, %s, %s, %s, %s, %s, %s)'
                        values = (self.name, item, category, quantity, self.country, date.today(), time.strftime("%H:%M:%S", time.localtime()))
                    my_cursor.execute(query, values)
                    db.commit()
                except:
                    pass

            os.system(systemclear)
          
            print('Enter y to continue ordering: ', end = '')
            response = input().lower()
            if response != 'y':
                break       
            
    #method to cancel the ordered items
    def cancel(self):
        os.system(systemclear)
          
        items_available = json.load(open(os.getcwd() + '/items.json', 'r'))
        gotp = str(random.randint(1000, 9999))
        if False:
            sen_email = 'eshopproject2021@gmail.com'
            emailpass = 'eshopproject20211!#'
            rec_email = self.mailid
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sen_email, emailpass)
            server.sendmail(sen_email, rec_email, 'Your OTP is ' +  gotp)
            pass
        while 1:
            os.system(systemclear)
          
            if False:
                print('The OTP has been sent to your email id!')
            else:
                print('The OTP is ', gotp)
            print('Enter the OTP: ', end = '')
            uotp = input()
            if uotp == gotp:
                for category in self.cart.keys():
                    for item in self.cart[category]:
                        items_available[category][item]['quantity'] += self.cart[category][item]
                self.cart = {}
                try:
                    db = mysql.connector.connect(host = 'mydb', user = 'root', password = 'root', port = 3306)
                    my_cursor = db.cursor()
                    my_cursor.execute('use shop')
                    my_cursor.execute("delete from salesreport where username = '%s'"%(self.name))
                    db.commit()
                except:
                    pass

                json.dump(items_available, open(os.getcwd() + '/items.json', 'w'), indent=4)
                print('Your order has been cancelled!')
                print('Press enter to continue..')
                input()
                break
            else:
                os.system(systemclear)
                print('Invalid OTP\nPress enter to continue..')
                input()
        
    #method to display the ordered items
    def display(self):
        os.system(systemclear)
          
        items_available = json.load(open(os.getcwd() + '/items.json', 'r'))
        if self.cart != {}:
            print('Your Cart')
            total_price = 0
            for category in self.cart.keys():
                for product in self.cart[category]:
                    print(('Product: ' + product).ljust(20),  (' | Category: ' + category).ljust(30), (' | Quantity: '+ str(self.cart[category][product])).ljust(20), (' | Price: ' + str(items_available[category][product]['price'])).ljust(15))
                    total_price += self.cart[category][product] * items_available[category][product]['price']
            if self.discount:
                print('For every fifth customer, we provide ₹ 500 discount!!')
                print('Total cost: ', total_price, '-500')
                print('Final cost: ', total_price - 500 if total_price - 500 >= 0 else 0)
            else:
                print('Total cost: ', total_price)
            print('Press enter to continue..')
            input()
        else:
            print('Your cart is empty!')
            print('Press enter to continue..')
            input()


#class which is responsible for admin functions
class Admin:
    password = '123'

    #method which prints the sales done in current day
    @staticmethod
    def todaysales():
        os.system(systemclear)
          
        try:
            db = mysql.connector.connect(host = 'mydb', user = 'root', password = 'root', port = 3306)
            my_cursor = db.cursor()
            my_cursor.execute('use shop')
            df = my_cursor.execute("select * from salesreport where order_date = '%s' "%(date.today()))
            df = my_cursor.fetchall()
            df = pd.DataFrame(df, columns = [i[0] for i in my_cursor.description])
        except:
            pass
        
        if df.empty:
            print('No sales today')
        else:
            print('Today\'s sales\n')
            df = df.to_string(index = False)
            print(df)
        print('\nPress enter to continue')
        input()

    #method to print the sales grouped by country
    @staticmethod
    def salesbyCountry():
        os.system(systemclear)
          
        try:
            db = mysql.connector.connect(host = 'mydb', user = 'root', password = 'root', port = 3306)
            my_cursor = db.cursor()
            my_cursor.execute('use shop')
            df = my_cursor.execute("select * from salesreport")
            df = my_cursor.fetchall()
            df = pd.DataFrame(df, columns = [i[0] for i in my_cursor.description])
        except:
            pass
        
        if df.empty:
            print('No sales')
        else:
            print('Sales by Country\n')
            print('Country'.ljust(15) + 'No. of products sold')
            for i, j in zip(df.groupby('Country').count()['Product'].index, df.groupby('Country').count()['Product']):
                print(i.ljust(15) + str(j).rjust(20))
        print('\nPress enter to continue')
        input()

    #method to print the sales grouped by product
    @staticmethod 
    def salesbyProduct():
        os.system(systemclear)
        try:
            db = mysql.connector.connect(host = 'mydb', user = 'root', password = 'root', port = 3306)
            my_cursor = db.cursor()
            my_cursor.execute('use shop')
            df = my_cursor.execute("select * from salesreport")
            df = my_cursor.fetchall()
            df = pd.DataFrame(df, columns = [i[0] for i in my_cursor.description])
        except:
            pass

        if df.empty:
            print('No sales')
        else:
            df = df.groupby('Product')
            print('Sales by Product\n')
            for i, j in df:
                print('Product:', i, '\n')
                print(j.to_string(index = False))
                print('\n')
        print('\nPress enter to continue')
        input()





