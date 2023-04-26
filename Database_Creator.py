import sqlite3
connection = sqlite3.connect('retro.db')
cursor = connection.cursor()
#cursor.execute('CREATE TABLE account(accountID INTEGER PRIMARY KEY, email TEXT, password TEXT, credit REAL)')
#cursor.execute('INSERT INTO account(email, password, credit) VALUES(?,?,?)', ("test@gmail.com", "password", 0.00))
#cursor.execute('INSERT INTO account(email, password, credit) VALUES(?,?,?)', ("test1@gmail.com", "password", 0.00))
#cursor.execute('CREATE TABLE product(productID INTEGER PRIMARY KEY, title TEXT, publisher TEXT, desc TEXT, console TEXT, release TEXT)')
#cursor.execute('DROP TABLE account')
#cursor.execute('DROP TABLE condition')
#cursor.execute('CREATE TABLE condition(conditionID INTEGER PRIMARY KEY, productID INTEGER, condition TEXT, stock INTEGER, price REAL)')
"""
cursor.execute('INSERT INTO product(title, publisher, desc, console, release) VALUES(?,?,?,?,?)', ("Super Nintendo Entertainment System", "Nintendo", "The Super Nintendo Entertainment System (SNES) is a 16 bit console made by Nintendo", "SNES", "11/21/1990"))

cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"OK",4,89.99))
cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"GOOD",7,99.99))
cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"LIKE NEW",1,149.99))
cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"CIB OK",0,399.99))
cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"CIB GOOD",1,599.99))
cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"CIB LIKE NEW",0,999.99))
cursor.execute('INSERT INTO condition(productID, condition, stock, price) VALUES(?,?,?,?)', (2,"NEW",1,2499.99))

for i in range(8,15):
    cursor.execute('UPDATE condition SET productID = 2 WHERE conditionID = ?',[i])
connection.commit()

cursor.execute('UPDATE account SET credit = 44.99 WHERE accountID = ?',[2])
connection.commit()

cursor.execute('CREATE TABLE purchasedItem(purchasedItemID INTEGER PRIMARY KEY, purchaseID INTEGER, conditionID INTEGER, price REAL)')
"""
cursor.execute('CREATE TABLE purchase(purchaseID INTEGER PRIMARY KEY, accountID INTEGER, shipping REAL, delivery TEXT, status TEXT, date TEXT, time TEXT, fname TEXT, lname TEXT, phone TEXT, address TEXT, zip TEXT, state TEXT, creditcard TEXT, security TEXT, month TEXT, year TEXT, credit REAL)')