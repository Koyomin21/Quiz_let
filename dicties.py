class User:
    id = 1


a = User()
print(a.id)

def change_id(a):
    a.id = 12

change_id(a)


print(a.id)