import sqlite3

db = sqlite3.connect('inventory.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS logincredentials
               (UserName text, Password text)''')
cursor.execute("INSERT INTO logincredentials Values('Apurva','Shopify')")
cursor.execute('''DROP TABLE inventoryDetails''')
cursor.execute('''CREATE TABLE IF NOT EXISTS inventoryDetails
               (ProductID INTEGER PRIMARY KEY UNIQUE, ProductName text, Price real, Qty integer)''')
cursor.execute("INSERT INTO inventoryDetails Values(1,'Vegetable',5.00,2)")
db.commit()
