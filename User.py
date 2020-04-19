class User:
    def __init__(self):
        self.name = input("Enter your username: ")
        self.score = 0
        self.total = 0
    def show(self):
        print("Name: {}\nScore: {}\nTotal: {}".format(self.name,self.score,self.total))
    