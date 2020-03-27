from os import system
from User import *
from DBService import *


def clear():
     _ = system('cls') 



class MenuService:
    
    def __init__(self):
        self.db = DBService()

    def menu(self,user):#determine which menu should be opened cust,admin or moderator
        if user.role_id == 1:
            self.admin_menu(user)
        elif user.role_id == 2:
            self.cust_menu(user)
        elif user.role_id == 3:
            self.moder_menu(user)

    def moder_menu(self,user):
        isActive = True
        while isActive:
            clear()
            user.show_data()
            print("\t\t\t1.Edit profile\n\t\t\t2.Edit Catalog\n\t\t\t3.Exit")
            ch = int(input())
            if ch == 1:
                self.change_data(user)
            elif ch ==2:
                self.edit_catalog()
            elif ch == 3:
                isActive = False

    def admin_menu(self,user):##dodelat'
        isActive = True
        while isActive:
            clear()
            user.show_data()
            print("\t\t\t1.Edit profile\n\t\t\t2.Appoint merchant\n\t\t\t3.Approve the delivery\n\t\t\t4.Exit")
            ch = int(input())
            if ch == 1:
                self.change_data(user)
            elif ch == 2:
                clear()
                self.appoint_merchant()
            elif ch == 3:
                self.show_deliveries()
                print("Enter the id of delivery you want to approve")
                del_id = int(input())
                self.approve_del(del_id)
            elif ch == 4:
                isActive = False
    
    def approve_del(self,del_id):
        self.db.approve_del(del_id)

    def show_deliveries(self):
        
        for i in self.db.show_deliveries():
            print(i)


    def appoint_merchant(self):
        print("List of users")
        for i in self.db.get_all_users():
            print(i)
        print("Enter the id of user to change the role")
        a = int(input())#id
        clear()
        print("\n\t\t\t1.Change to Customer\n\t\t\t2.Change to Merchant")
        ch = int(input())
        for i in self.db.get_all_users():
            if i['ID'] == a:
                if ch == 2 and i['ROLE_ID'] == 3:
                    print("This user is already a moderator!\nEnter any key to continue")
                    k = input()
                elif  ch == 1 and i["ROLE_ID"] == 2:
                    print("This user is already a moderator!\nEnter any key to continue")
                    k = input()
                elif i["ROLE_ID"] == 1:
                    print("You cannot change the role of this use!\nEnter any key to continue")
                    k = input()
                elif ch == 1:
                    self.db.change_role(a,2)
                elif ch == 2:
                    self.db.change_role(a,3)

    def edit_catalog(self):
        isActive = True
        while isActive:
            clear()
            self.show_items()
            print("\t\t\t1.Add new Item\n\t\t\t2.Edit Item\n\t\t\t3.Delete Item\n\t\t\t4.Exit")
            ch = int(input())
            if ch == 1:
                clear()
                print("Enter the name of Item")
                name = input()
                print("Enter the price of Item")
                price = int(input())
                self.db.add_item(name,price)
            elif ch == 2:
                clear()
                self.item_edit()
            elif ch == 3:
                clear()
                print("Enter the id of Item you would like to delete")
                Id = int(input())
                self.db.delete_item(Id)
            elif ch == 4:
                isActive = False
            
    def item_edit(self):
        isActive = True
        while isActive:
            print("Enter the id of Item you would like to change")
            item_id = int(input())
            print("\t\t\t1.Change the name of Item\n\t\t\t2.Change the price of Item\n\t\t\t3.Exit")
            ch = int(input())
            if ch == 1:
                param = "NAME"
                print("Enter the new name for Item")
                name = input()
                name = "\'{}\'".format(name)
                self.db.edit_item(param,item_id,name)
            elif ch == 2:
                param = "PRICE"
                print("Enter the new price for Item")
                price = input()
                self.db.edit_item(param,item_id,price)

            elif ch == 3:
                isActive = False


    def change_data(self,user):
        isActive = True
        while isActive:
            clear()
            user.show_data()
            print("\n\t\t\t1.Change username\n\t\t\t2.Change first name\n\t\t\t3.Change last name\n\t\t\t4.Change password\n\t\t\t5.Exit")
            ch = int(input())
            change = ""
            if ch == 1:
                change = "\'USERNAME\'"
                print("Enter new username")
                user.username = input()
                self.db.change_data(user,change,user.username)
            elif ch == 2:
                change = "\'FIRST_NAME\'"
                print("Enter new first name")
                user.first_name = input()
                self.db.change_data(user,change,user.first_name)
            elif ch == 3:
                change = "\'LAST_NAME\'"
                print("Enter new last name")
                user.last_name = input()
                self.db.change_data(user,change,user.last_name)
            elif ch == 4:
                change = "\'PASSWORD\'"
                print("Enter new password")
                user.password = input()
                self.db.change_data(user,change,user.password)
            elif ch == 5:
                isActive = False


    def edit_cart(self,user):
        isActive = True
        while isActive:
            clear()
            self.check_cart(user)
            if self.db.cart_filled(user):
                print("Your cart contains:\n")
                self.show_cart(user)
            else:
                print("You have nothing in cart")
            print("\t\t\t1.Add item to cart\n\t\t\t2.Delete item from cart\n\t\t\t3.Buy an Item\n\t\t\t4.Exit")
            ch = int(input())

            if ch == 4:
                isActive = False
            elif ch == 1:
                self.add_item_to_cart(user)
            elif ch == 2:
                self.delete_item_from_cart(user)
            elif ch == 3:
                self.make_delivery(user)

    def make_delivery(self,user):
        print("Your cart contains:\n")
        self.show_cart(user)
        print("Enter the id of Item you want to order")
        item_id = int(input())
        if self.db.can_pay(user,item_id):
            self.change_balance(user)
            self.db.create_del(user,item_id)
        else:
            print("Sorry, you don't have enough money on balance to buy this Item")

    def change_balance(self,user):
        self.db.change_balance(user)

    def add_item_to_cart(self,user):
        print("Enter the id of Item you want to add to cart")
        item_id = int(input())
        cart_id = self.db.get_cart_id(user.Id)
        if self.db.check_item_in_cart(item_id,cart_id):
            self.db.add_amount(item_id,cart_id)
            
        else:
            self.db.add_item_to_cart(cart_id,item_id)

    def delete_item_from_cart(self,user):
        print("Enter the if of Item you want to delete from your cart")
        item_id = int(input())
        cart_id = self.db.get_cart_id(user.Id)
        self.db.delete_item_from_cart_am(cart_id,item_id)
    

    def cust_menu(self,user):##produmat vot eto
        isActive = True
        while isActive:
            clear()
            user.show_data()
            print("\t\t\t1.Edit profile\n\t\t\t2.Edit a cart\n\t\t\t3.Watch the catalog\n\t\t\t4.Exit")
            ch = int(input())
            if ch == 1:
                self.change_data(user)
            elif ch == 2:
                self.edit_cart(user)
            elif ch == 3:
                self.show_items()
                print("\nEnter any symbol to continue")
                k = input()
            elif ch == 4:
                isActive = False
                

    def register(self):
        isActive = True
        while isActive:
            clear()
            user = User()
            user.register()
            if self.db.is_user(user):   
                clear()
                print("Sorry, but this username is already taken\nPress x to exit")
                x = input()
                if x == 'x':
                    isActive = False
            else:
                self.db.add_user(user,2);
                isActive = False
                self.cust_menu(user)
        
    def login(self):
        isActive = True
        while isActive:
            user = User()
            print("Enter your username")
            user.username = input()
            print("Enter your password")
            user.password = input()

            if self.db.check_user(user):
                self.menu(user)
                isActive = False
            else:
                print("Invalid login or password!")
                print("Enter x to exit")
                x = input()
                if x == 'x':
                    isActive = False
        

    def start_menu(self):
        isActive = True
        while isActive:
            clear()
            print("\t\t\t1.Register\n\t\t\t2.Log-in\n\t\t\t3.Exit")
            ch = int(input())
            if ch == 1:
                self.register()
            elif ch == 2:
                self.login()
            elif ch == 3:
                isActive = False
            elif ch == 4:
                for i in self.db.get_all_users():
                    print(i)
                print(self.db.get_cart_nId())
                k = input()
    
    def close_db(self):
        self.db.close()
        
    def show_cart(self,user):#fix it
        cart = tuple(self.db.show_cart(user))
        for i in cart:
            self.show_item(i['ITEM_ID'])
            print('Amount: {}'.format(i['AMOUNT']))

    def show_items(self):
        for i in self.db.get_all_items():
            print(i)

    def show_item(self,item_id):
        for i in self.db.show_item(item_id):
            print(i)

    def check_cart(self,user):
        for i in self.db.show_cart(user):
            if i['AMOUNT'] < 1:
                self.db.delete_item_from_cart(i['CART_ID'],i['ITEM_ID'])