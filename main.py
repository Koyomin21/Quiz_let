import json
import random
from functions import *
from User import *

        


name = input("Enter your username: ")
user = User(name)

questions = get_questions()
random.shuffle(questions)

for i in questions:
    print(i[1]['question'])
    ans = input()
    if(ans.lower() == i[1]['answer'].lower()):
        user.total+=1
        user.score+=20

send_res(user)


    



