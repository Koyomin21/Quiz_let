from contextlib import closing
import pymysql
from pymysql.cursors import DictCursor
from User import *


class DBService:
    def __init__ (self):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',      
            db = 'shop',
            charset = 'utf8mb4',
            cursorclass = DictCursor
        )
        self.cursor = self.connection.cursor()

    def confirm_changes(self,query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def get_all_users(self):
        query = """
            SELECT * FROM user
        """
        self.confirm_changes(query)
        return self.cursor

    def create_cart(self,user):
        query = """
             INSERT INTO carts(USER_ID,ID) VALUES({},{})
         """.format(user.Id,self.get_cart_nId())

        self.confirm_changes(query)

    def create_del(self,user,item_id):
        cart_id = self.get_cart_id(user.Id)
        self.delete_item_from_cart_am(cart_id,item_id)
        query = """
            INSERT INTO delivery(STATUS,USER_ID,CART_ID)
            VALUES({},{},{})
         """.format(0,user.Id,self.get_cart_id(user.Id))
        self.confirm_changes(query)

    def create_items(self,user):
        query = """
            INSERT INTO items_in_cart(CART_ID)
            VALUES({})
        """.format(self.get_cart_id(user.Id))
        self.confirm_changes(query)

    def add_user (self,user,role_id):
        
        query = """
            INSERT INTO user (USERNAME, PASSWORD, ROLE_ID,balance) VALUES(%s, %s, %s,%s)
        """
        data = (user.username, user.password, str(role_id),str(5000))

        self.cursor.execute(query, data)
        self.connection.commit()

        user.Id = self.new_id()-1
        print(user.Id)

        self.create_cart(user)
        
        #get rid of it

        self.create_items(user)


    def close (self):
        self.cursor.close()
        self.connection.close()

    def delete_user(self):
        print("Enter the id of user that you want to delete")
        id = int(input())
        query = """ 
            DELETE FROM user WHERE ID = {}
            """.format(id)
        self.confirm_changes(query)
    
    def show_info(self):
        print("Enter the id of user that you are looking for")
        id = int(input())
        query = """
            SELECT * FROM user
            WHERE ID = {}
        """.format(id)
        self.confirm_changes(query)

    def is_user(self,user):
        query = """
            SELECT USERNAME,PASSWORD FROM user
         """
        self.cursor.execute(query)
        for i in self.cursor:
            if i["USERNAME"] == user.username and i["PASSWORD"] == user.password:
                return True
        
        return False

    def cart_filled(self,user):
        cart_id = self.get_cart_id(user.Id)
        query = """
            SELECT * FROM items_in_cart WHERE CART_ID = {}
        """.format(cart_id)
        self.confirm_changes(query)
        for i in self.cursor:
            return i

    def show_cart(self,user):
        Id = self.get_cart_id(user.Id)
        query = """
            SELECT * FROM items_in_cart WHERE CART_ID = {}
        """.format(Id)
        self.confirm_changes(query)
        return self.cursor

    def change_data(self,user,change,user_info):
        user_info = "{}".format(user_info)
        query = """
            UPDATE user
            SET {} = {}
            WHERE ID = {}
        """.format(change,user_info,user.Id)
        self.confirm_changes(query)

    def edit_item(self,param,Id,new_info):
        query = """
            UPDATE item
            SET {} = {}
            WHERE ID = {}
        """.format(param,new_info,Id)
        self.confirm_changes(query)
    
    def delete_item(self,id):
        query = """
            DELETE FROM item WHERE ID = {}
        """.format(id)

        self.confirm_changes(query)
    
    def get_all_items(self):
        query = """
            SELECT * FROM item
        """
        self.confirm_changes(query)
        return self.cursor

    def check_user(self,user):
        query = """
            SELECT * FROM user
         """
        self.cursor.execute(query)
        for i in self.cursor:
            if i["USERNAME"] == user.username and i["PASSWORD"] == user.password:
                user.first_name = i['FIRST_NAME']
                user.last_name = i['LAST_NAME']
                user.Id = i['ID']
                user.role_id = i['ROLE_ID']
                user.balance = i['balance']
                return True
        return False
        
    def get_cart_nId(self):
        query = """
            SELECT MAX(ID) FROM carts
        """
        self.confirm_changes(query)
        for i in self.cursor:
            return i['MAX(ID)']+1
    
    def get_role(self,user):
        for i in self.cursor:
            if i['USERNAME'] == user.username:
                return i['ROLE_NAME']

    def add_item(self,name,price):
        
        query = """
            INSERT INTO item(NAME,PRICE)
            VALUES ("{}",{})
        """.format(name,price)

        self.confirm_changes(query)

    def new_id(self):
        query = """
            SELECT MAX(ID) FROM user
        """
        self.confirm_changes(query)
        for i in self.cursor:
            return i['MAX(ID)']+1           

    def get_cart_id(self,id):
        query = """
            SELECT * FROM carts WHERE USER_ID = {}
        """.format(id)
        self.confirm_changes(query)
        for i in self.cursor:
            return i['ID']

    def change_role(self,id,role):
        query = """
                UPDATE user
                SET ROLE_ID = {}
                WHERE ID = {}
            """.format(role,id)
        self.confirm_changes(query)
    
    def check_item_in_cart(self,item_id,cart_id):
        query = """
            SELECT * FROM items_in_cart WHERE CART_ID = {} and ITEM_ID = {}
        """.format(cart_id,item_id)
        self.confirm_changes(query)
        for i in self.cursor:
            return i;

    def add_amount(self,item_id,cart_id):
        query = """
            UPDATE items_in_cart
            SET AMOUNT = AMOUNT+1
            WHERE CART_ID = {} and ITEM_ID = {}
        """.format(cart_id,item_id)
        self.confirm_changes(query)

    def add_item_to_cart(self,cart_id,item_id):
        query = """
            INSERT INTO items_in_cart(CART_ID,ITEM_ID,AMOUNT)
            VALUES ({},{},{})
        """.format(cart_id,item_id,1)
        self.confirm_changes(query)

    def delete_item_from_cart_am(self,cart_id,item_id):
        query = """
            UPDATE items_in_cart SET AMOUNT = AMOUNT-1 
            WHERE CART_ID = {} and ITEM_ID = {}
        """.format(cart_id,item_id)
        self.confirm_changes(query)
        
    def delete_item_from_cart(self,cart_id,item_id):
        query = """
            DELETE FROM items_in_cart WHERE CART_ID = {} and ITEM_ID = {}
        """.format(cart_id,item_id)
        self.confirm_changes(query)

    def show_item(self,item_id):
        query = """
            SELECT * FROM item WHERE ID = {}
        """.format(item_id)
        self.confirm_changes(query)
        return self.cursor

    def show_deliveries(self):
        query = """
            SELECT * FROM delivery WHERE STATUS = 0
        """
        self.confirm_changes(query)
        return self.cursor
    
    def get_item_price(self,item_id):
        query = """
            SELECT PRICE FROM item WHERE ID = {}
        """.format(item_id)
        self.confirm_changes(query)
        for i in self.cursor:
            return i
        
    def can_pay(self,user,item_id):
        
        price = self.get_item_price(item_id)
        if user.balance - price['PRICE'] >= 0:
            user.balance = user.balance - price['PRICE']
            return True
        else:
            return False
    def change_balance(self,user):
        query = """
            UPDATE user
            SET balance = {}
            WHERE ID = {}
        """.format(user.balance,user.Id)
        self.confirm_changes(query)

    def approve_del(self,del_id):
        query = """
            UPDATE delivery
            SET STATUS = 1
            WHERE ID = {}
        """.format(del_id)
        self.confirm_changes(query)