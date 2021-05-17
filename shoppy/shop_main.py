#python file which acts as the main file, imports shop.py

import os, pickle, sys, copy
sys.path += ['shoppy']

import shop
os.chdir('shoppy')
file = open(os.getcwd() + '/objectstore.pkl', 'rb')
users = pickle.load(file)
file.close()
if os.name == 'posix':
    systemclear = 'clear'
else:
    systemclear = 'cls'

#function which is used for user creation
def signup():
    os.system(systemclear)
    print('Enter the username: ', end = '')
    u_name = input().strip()
    print('Enter the mailid: ', end = '')
    u_mailid = input().strip()
    print('Enter the password: ', end = '')
    password = input().strip()
    print('Enter the country:  ', end = '')
    country_input = input().strip()
    user = shop.User(u_name, u_mailid, password)
    user.country = country_input
    users[u_name] = user 
    if len(users) % 5 == 0:
        user.discount = True
    print('New user created!\nRedirecting to Login page')
    print('Press enter to continue ', end = '')
    input()

#function to login the user
def login():
    while 1:
        os.system(systemclear)
        print('Enter the username: ', end = '')
        username = input().strip()
        if username in users:
            user = copy.deepcopy(users[username])
            while 1:
                os.system(systemclear)
                print('Enter the password: ', end = '')
                password = input().strip()
                if password != user.password:
                    continue
                else:
                    print('Logged in, Enter to continue ', end = ' ')
                    input()
                    break
            break
    return user
    

#main function which integrates all the other functions
def main():
    while 1:
        os.system(systemclear)
        print('Press\nLogin - l\nSign up - s\nAdmin -a\nExit - e')
        response = input().lower()
        if response == 'e':
            os.system(systemclear)
            break
        elif response == 'l':
            user = login()
        elif response == 's':
            signup()
            user = login()
        elif response == 'a':
            while 1:
                os.system(systemclear)
                print('Enter the admin password: ', end = ' ')
                password = input().strip()
                if password == shop.Admin.password:
                    break
                else:
                    os.system(systemclear)
                    print('Incorrect password')
                    print('\nPress enter to continue')
                    input()
            while 1:
                os.system(systemclear)
                print('Enter the following\n1. Today\'s sales\n2. Sales by Country\n3. Sales by Product\n4. Log out')
                response = int(input())
                if response == 1:
                    shop.Admin.todaysales()
                elif response == 2:
                    shop.Admin().salesbyCountry()
                elif response == 3:
                    shop.Admin().salesbyProduct()
                elif response == 4:
                    os.system(systemclear)
                    break
            continue

        os.system(systemclear)
        while 1:
            os.system(systemclear)
            print('Enter the following\n1. Place order\n2. Cancel order\n3. View orders\n4. Log out')
            response = int(input())
            if response == 1:
                user.order()
                users[user.name] = user
                file = open(os.getcwd() + '/objectstore.pkl', 'wb')
                pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)
                file.close()
            elif response == 2:
                user.cancel()
                users[user.name] = user
                file = open(os.getcwd() + '/objectstore.pkl', 'wb')
                pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)
                file.close()
            elif response == 3:
                user.display()
                users[user.name] = user
                file = open(os.getcwd() + '/objectstore.pkl', 'wb')
                pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)
                file.close()
            elif response == 4:
                users[user.name] = user
                print(users[user.name].cart)
                file = open(os.getcwd() + '/objectstore.pkl', 'wb')
                pickle.dump(users, file, pickle.HIGHEST_PROTOCOL)
                file.close()
                break


