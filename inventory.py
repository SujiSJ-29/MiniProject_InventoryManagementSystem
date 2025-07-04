import sqlite3
from datetime import datetime
try:
    conn = sqlite3.connect('inventory_management_system.db')
    cursor = conn.cursor()
    # Create table admin to store userid and password
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS admin(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username VARCHAR(30) UNIQUE,
               password TEXT
               )
       ''')
    # Create table product for product details
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS product(
            product_id INTEGER PRIMARY KEY UNIQUE,
            product_name VARCHAR(255),
            price DECIMAL(10,2),
            category VARCHAR(100),
            userid VARCHAR(100),
            FOREIGN KEY(userid) REFERENCES admin(username)
            )
    ''')
    # Create table inventorys for inventory deatails
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventorys(
               inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
               product_id INTEGER,
               quantity INTEGER,
               userid VARCHAR(100),
               last_updated Text,               
               FOREIGN KEY(product_id) REFERENCES product(product_id),
               FOREIGN KEY(userid) REFERENCES admin(username)
               )
    ''')
      # Create table transactions for transaction details
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS transactions(
               transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
               product_id INTEGER,
               transaction_type VARCHAR(30),
               userid VARCHAR(100),
               transaction_date Text,
               quantity INTEGER,
               FOREIGN KEY(product_id) REFERENCES product(product_id),
               FOREIGN KEY(userid) REFERENCES admin(username)
            )
    ''')
except sqlite3.Error as e:
     # Handle SQLite-specific errors
    print(f"Error: {e}")
except Exception as e:
    # Handle other general exceptions
    print(f"An unexpected error occurred: {e}")
conn.commit()
conn.close()
# function for registeration
def register():
    username = input("Enter your username : ")
    password = input("Enter your password : ")
    try :
          conn = sqlite3.connect('inventory_management_system.db') 
          cursor =conn.cursor()
          cursor.execute('''                   
             INSERT INTO admin(username,password)
                values(?,?)''',(username,password))
          print("user created ")
          conn.commit()
    except Exception as e :
          print(f"An error occurred: {e}")
    conn.close()
def login():
     username = input("Enter your username : ")
     password = input("Enter your password : ")
     try:
           conn = sqlite3.connect('inventory_management_system.db') 
           cursor =conn.cursor()
           cursor.execute('''
                          SELECT * FROM  admin WHERE username = ? AND password = ?''',
                          (username,password))
           user = cursor.fetchone()
           if user : 
                 print("login successfully")
                 while True:
                       print("1. Add item")
                       print("2. View item")
                       print("3. Updating item")
                       print("4. Searching item")
                       print("5. Exit")
                       choice = input("Enter your choice : ")
                       if choice == '1':
                        add_item(username)
                       elif choice == '2':
                        view_item()
                       elif choice == '3':
                        update_item(username)
                       elif choice == '4':
                        search_item()
                       elif choice =='5':
                        break
           else :
                print("login failed  invalid credential")
     except Exception as e :
          print(f"An error occurred: {e}")
    
def add_item(username):
        conn = sqlite3.connect('inventory_management_system.db')
        cursor = conn.cursor()
        print("Add products ")
        product_id = int(input("Enter product id : "))
        product_name = input("Enter product name : ")
        price = float(input("Enter price : "))
        category = input("Enter category : ")
        quantity = int(input("Enter the quantity : "))
        currentdate = datetime.now()
        try :
              cursor.execute('''
                             SELECT * FROM  product WHERE product_id = ? ''',
                             (product_id,))
              id = cursor.fetchone()
              if id :
                print("Product id already exist ")
              else :
                    print("add item")
                    cursor.execute('''
                                   INSERT INTO product(product_id,product_name,price,category,userid)
                                   VALUES(?,?,?,?,?)''',(product_id,product_name,price,category,username))
                    cursor.execute('''
                                   INSERT INTO inventorys(product_id,quantity,userid,last_updated)
                                   VALUES(?,?,?,?)''',(product_id,quantity,username,currentdate.strftime('%D  %H.%M:%S')))
                    conn.commit() 
        except Exception as e :
          print(f"An error occurred: {e}")                   
        conn.close()

def view_item():
        conn = sqlite3.connect('inventory_management_system.db')
        cursor = conn.cursor()
        try :
              cursor.execute('''
                             SELECT * FROM inventorys
                             ''')
              details = cursor.fetchall()
              for i in details:
                print(f'Product id : {i[1]} Quantity : {i[2]} userid : {i[3]} last update : {i[4]}')
              conn.commit()
        except Exception as e :
          print(f"An error occurred: {e}") 
        conn.close()

def update_item(username):
        product_id = int(input ("Enter product id :"))
        conn = sqlite3.connect('inventory_management_system.db')
        try :
              cursor = conn.cursor()
              cursor.execute('''
                             SELECT * FROM  product WHERE product_id = ? ''',
                             (product_id,))
              id = cursor.fetchone()
              if id :
                transaction_type = input("Enter transaction type 'Sale / Purchase' : ")
                if transaction_type =='Sale' or transaction_type == 'Purchase':
                         cursor.execute('''
                                        SELECT * FROM  inventorys WHERE product_id = ? ''',
                                        (product_id,))
                         inventory_quantity = cursor.fetchone()
                         print("quantity  ",inventory_quantity[2])
                         current_quantity = inventory_quantity[2]
                         update_quantity = int(input("Enter quantity to update : "))
                         date_today = datetime.now()
                         cursor.execute('''
                                INSERT INTO transactions (product_id,transaction_type,userid,transaction_date,quantity)
                                       VALUES(?,?,?,?,?) ''', (product_id,transaction_type,username,date_today.strftime('%D  %H.%M:%S'),update_quantity))
                         if transaction_type =='Sale':
                                if current_quantity < update_quantity :
                                        print("Not enough STOCK ")
                                else :
                                        quantity = current_quantity - update_quantity
                                       
                                        cursor.execute('''
                                                UPDATE inventorys SET quantity = ? ,userid = ? ,last_updated = ? WHERE product_id = ?''' ,
                                                        (quantity,username,date_today.strftime('%D  %H.%M:%S'),product_id,))
                                        print("Update Successfully  ")
                         elif transaction_type == 'Purchase' :
                                 quantity = current_quantity + update_quantity
                                 
                                 cursor.execute('''
                                                UPDATE inventorys SET quantity = ? ,userid = ? ,last_updated = ? WHERE product_id = ?''' ,
                                                        (quantity,username,date_today.strftime('%D  %H.%M:%S'),product_id,))
                                 print("Update Successfully  ")           
                        
                else :
                        print("enter transaction type either 'Sale / Purchase' ")
              else :
                print("Product id not exist ")
              conn.commit()
        except Exception as e :
          print(f"An error occurred: {e}")  
        
        conn.close()

def search_item():
       search_data = input("Search based on category/product name :  ")
       conn = sqlite3.connect('inventory_management_system.db')
       cursor = conn.cursor()
       try : 
            if search_data == 'category':
              category_name = input("Enter the category name : ")
              cursor.execute('''
                      SELECT * FROM  product WHERE category = ? ''',
                      (category_name,))
              data = cursor.fetchall()
              for i in data :
                     print({i[1]})
            elif search_data == 'product name' :
              product_name = input("Enter product name : ")
              cursor.execute('''
                      SELECT * FROM  product WHERE product_name = ? ''',
                      (product_name,))
              data = cursor.fetchall()
              for i in data :
                     print(f'Product id : {i[0]}  Price = {i[2]} Category = {i[3]}')   
              conn.commit()
       except Exception as e :
          print(f"An error occurred: {e}") 
       conn.close()



def inventory_management():
    #  Authentication
       print('           Inventory Management System    ')
       while True :
               print('1 . Register')
               print("2 . Login ")
               print("3 . Exit")
               choice = input("Enter the choice : ")
               if choice == '1':
                      register()
               elif choice == '2':
                      login()
               elif choice == '3' :
                      break
             
inventory_management()