import json
import random
from functions import *
from User import *

        

gameover = False

while not gameover:
    print('\t\t\t1.Start quiz\n\t\t\t2.Add a question\n\t\t\t3.Exit')
    ch = int(input())
    if ch == 1:
        user = User()
        if user_exists(user):
            print("Your previous highscore:",get_highscore(user))
        else:
            new_user(user)
        questions = get_questions()
        answer_questions(user,questions)
        send_res(user)
        gameover = True

    elif ch == 2:
        add_question()
    elif ch == 3:
        gameover = True







    



