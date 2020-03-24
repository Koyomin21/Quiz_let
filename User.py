from Delivery import*
from Carts import*
class User:
    username = ""
    first_name = ""
    last_name = ""
    role_id = int() 
    Id = int()
    balance = int()
    delivery = []


    def register(self):
        print("Enter your username")
        self.username = input()
        print("Enter your password")
        self.password = input()
        print("Enter your first name")
        self.first_name = input()
        print("Enter your last name")
        self.last_name = input()
    def show_data(self):
        print("Id: ",self.Id)
        print("Username: ",self.username)
        print("First name: ",self.first_name)
        print("Last name: ",self.last_name)
        print("Balance: ",self.balance)