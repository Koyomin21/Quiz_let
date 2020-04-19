import json
import random
def shuffle_questions(questions):
    questions = list(questions)
    random.shuffle(questions)
    questions = dict(questions)
    return questions

def user_exists(user):
    with open ('passed_test.json') as f:
        temp = json.load(f)
    
    qs = dict(temp.items())
    for i in qs:
        if i == user.name:
            return True
    return False

def add_question():
    q = input("Enter the question:")
    a = input("Enter the answer: ")
    with open('questions.json') as f:
        temp = json.load(f)
        
    questions = dict(temp.items())
    num = int(0)
    for i in questions:
        if int(i[-1:]) > num:
            num = int(i[-1:])
    num+=1
    questions['question_{}'.format(num)] = {'question':q,'answer':a,'rating':0,'answered':0,'correct':0}
    with open ('questions.json','w') as f:
        json.dump(questions,f)

def new_user(user):
    with open('passed_test.json')as f:
        temp = json.load(f)

    users = dict(temp.items())

    users[user.name] = {"score" : user.score,"total" : user.total}

    with open('passed_test.json','w') as f:
        json.dump(users,f)
    

def get_questions():
    with open("questions.json")as file:
        templates = json.load(file)

    questions = list(templates.items())
    random.shuffle(questions)
    questions = dict(questions)
    return questions


def send_res(user):
    with open('passed_test.json')as f:
        tmp = json.load(f)

    users = dict(tmp)

    if user_exists(user):
        users[user.name]['prev_result'] = user.score
        if users[user.name]['score']<user.score:
            users[user.name]['score'] = user.score
            users[user.name]['total'] = user.total
            print("You got a new highscore!\n{}".format(user.score))
        else:
            users[user.name] = {'score':user.score,'total':user.total,'prev_result':user.score}

    with open('passed_test.json','w') as f:
        json.dump(users,f)

def answer_questions(user,questions):
    for i in questions:
        print(questions[i]['question'])
        ans = input()
        questions[i]['answered']+=1
        if(ans.lower() == questions[i]['answer'].lower()):
            user.total+=1
            user.score+=20
            questions[i]['correct']+=1
        questions[i]['rating'] = 100*questions[i]['correct']/questions[i]['answered']
    
    with open('questions.json','w')as f:
        json.dump(questions,f)

def get_highscore(user):
    with open ('passed_test.json')as f:
        temp = json.load(f)
    users = dict(temp.items())
    return users[user.name]['score']