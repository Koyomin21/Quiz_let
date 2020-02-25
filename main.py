from add import User


users = []

def change_data(login,password):
    isActive = 1;
    while isActive > 0:
        print("\t\t1.Change login\n\t\t2.Change password\n\t\t3.Exit")
        ch = input()
        if ch == 1:
            print("Enter new username:")
            username = input()
            users[username] = users.pop(login)
        


def sign_up():
        print("Enter your username: ")
        login = input()
        print("Enter your password: ")
        password = input()
        user = User(login,password) 
        
        
def sign_in():
    print("Enter your username: ")
    login = input()
    print("Enter your password: ")
    password = input()
    for i in users:
        if login == i and password == users[i]:
            change_data(login,password)

isActive = 1



while isActive > 0:
    print("\t\t1.Register\n\t\t2.Log-in\n\t\t3.Exit")
    ch = int(input())
    if ch == 1:
        sign_up()
    elif ch == 2:
        sign_in()
    elif ch == 3:
        isActive = 0;
    elif ch == 4:
        print(users)
    else: print("Incorrect input!\n{}".format(input()))
    