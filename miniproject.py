#main file which integrates all other python files

#code to connect with mysql, create database and tables
try:
    import mysql.connector
    db = mysql.connector.connect(host = 'mydb', user = 'root', password = 'root', port = 3306)
    my_cursor = db.cursor()
    my_cursor.execute('create database shop')
    my_cursor.execute('use shop')
    my_cursor.execute('create table salesreport(Id int not null auto_increment primary key, Username varchar(30), Product varchar(30), Category varchar(30), Quantity int, Country varchar(30), Order_Date date, Order_time time)')
    
except:
    pass


from shoppy import shop_main
shop_main.main()