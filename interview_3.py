import sys
import re
import logging
import random
import yaml
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

# print things to the command window
def trace(string):
    sys.stderr.write(string+'\n')
    sys.stderr.flush()
    return

app = Flask(__name__)
ask = Ask(app, "/")

neg = 0
pos = 0
emp = 0



def rating():
    global pos, neg, emp
    session.attributes['rating'] = 0 #rating starts at 0 points
    neg_r = 0.75 * neg
    pos_r = 1 * pos
    emp_r = emp * 0.25
    session.attributes['rating'] = pos_r - neg_r - emp_r
    ratings = session.attributes['rating']
    round_msg = 'You used ' + str(pos) + ' positive words, ' + str(neg) + ' negative words, and ' +str(emp) +' empty words in your interview.'
    if ratings >= 3:
        return round_msg + ' You had a pretty positive interview! Good job! You seem prepared for your interview!'
    if ratings <= -2:
        return round_msg + ' Try to be a tad bit more positive in your actual interview. Think about practicing more before your interview.'
    if -2 < ratings < 3:
        return round_msg + ' Try to be more positive in your actual interview.'

def feedback():
    global pos, neg, emp
    session.attributes['state'] = 'feedback'
    sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()
    msg = rating()+ " " + 'Good luck!'

    return statement(msg)

# first regular expression 'w' and then every time after that do 'a'
@ask.launch
def beginInterview():
    if 'hello' in session.attributes:
        prefix = ''
    else:
        session.attributes['hello'] = 1
    # do I need and sessions?
    with open('questions.yaml') as f:
        questions = yaml.load(f.read())
    with open('tips.yaml') as f:
        tips = yaml.load(f.read())
    session.attributes['state'] = 'Hello' # set state as what you are in
    session.attributes['numberOfQuestions'] = 0
    session.attributes['badWords'] = 0
    session.attributes['goodWords'] = 0
    session.attributes['emptyWords'] = 0
    session.attributes['questionList'] = questions
    session.attributes['tipList'] = tips
    session.attributes['tip'] = None
    session.attributes['question']  = None #question asked
    #hello_msg = render_template('hello')
    hello_msg = "Welcome to College Interview developed at Carnegie Mellon University by the Summer Academy for Math and Science. Ready to practice?"
    return question(hello_msg) # makes alexa ask question

@ask.intent("YesIntent")
def instructions(saidyes):
    
    sys.stderr.write('\n-----------------------[OLD state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()
    if(session.attributes['numberOfQuestions'] == 21):
         sys.stderr.write('-----------------------[Q number]----> '+str('end was called'+'\n'))
         return feedback()
    # the user bails immediately; i.e. no games were played. Express regret
    if session.attributes['state'] == 'Hello': # origin state
        
        session.attributes['state'] = 'Instruction' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    #instruction_msg = render_template('instruction')
        instruction_msg = "Say: Repeat, to hear the question again: skip, to move on. tip, if you're unsure how to answer a question. and: End Interview. to end the interview and receive your feedback. If you are unsure of the instructions, say: help. If you are ready, say start my interview."
        return question(instruction_msg)
        
    
    else:
        session.attributes['state'] = 'Yes Intent Called' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        session.attributes['state'] = 'Question'
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        questionIndex = random.randint(0,len(session.attributes['questionList'])-1)
        question_msg = session.attributes['questionList'][questionIndex]
        tip_msg = session.attributes['tipList'][questionIndex]
        session.attributes['question'] = question_msg
        session.attributes['tip'] = tip_msg
        session.attributes['numberOfQuestions'] += 1
        session.attributes['questionList'].pop(questionIndex)
        session.attributes['tipList'].pop(questionIndex)

        record(saidyes)
        return question(question_msg)
    
@ask.intent("HelpIntent")
def help():
    if session.attributes['state'] != 'Hello': # origin state
        
        session.attributes['state'] = 'Help' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        instruction_msg = "Say: Repeat, to hear the question again: skip, to move on. tip, if you're unsure how to answer a question. and: End Interview. to end the interview and receive your feedback. If you are unsure of the instructions, say: help. If you are ready, say: continue iterview."
        return question(instruction_msg)    
    
@ask.intent("GreetingIntent")
def greeting():

    if session.attributes['state'] == 'Instruction': # origin state
        
        session.attributes['state'] = 'Greeting' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
  #  greeting_msg = render_template('greeting')
    greeting_msg = "Hello, how are you doing today?"
    return question(greeting_msg)

@ask.intent("ContinueIntent")
def cont(next):
    global pos, neg, emp
    session.attributes['state'] = 'Continue' # set current state
    sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()
    if(session.attributes['numberOfQuestions'] == 21):
         sys.stderr.write('-----------------------[Q number]----> '+str('end was called'+'\n'))
         return feedback()
        
    else:
        session.attributes['state'] = 'Question'
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        questionIndex = random.randint(0,len(session.attributes['questionList'])-1)
        question_msg = session.attributes['questionList'][questionIndex]
        tip_msg = session.attributes['tipList'][questionIndex]
        session.attributes['question'] = question_msg
        session.attributes['tip'] = tip_msg
        session.attributes['numberOfQuestions'] += 1
        session.attributes['questionList'].pop(questionIndex)
        session.attributes['tipList'].pop(questionIndex)

        record(next)
        return question(question_msg) 
        

@ask.intent("QuestionIntent")
def generateQuestion(Freeform):
    global pos, neg, emp
    if(session.attributes['numberOfQuestions'] == 21):
         sys.stderr.write('-----------------------[Q number]----> '+str('end was called'+'\n'))
         return feedback()
    else:    
        if (session.attributes['state'] == 'Greeting' and session.attributes['numberOfQuestions'] == 0):
            session.attributes['state'] = 'First Question'
            sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
            sys.stderr.flush()
            greeting_response_msg = "..... Tell me about yourself. "
            session.attributes['numberOfQuestions'] = 1
            return question(greeting_response_msg)
    
        else:
            session.attributes['state'] = 'Question'
            sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
            sys.stderr.flush()
            questionIndex = random.randint(0,len(session.attributes['questionList'])-1)
            question_msg = session.attributes['questionList'][questionIndex]
            tip_msg = session.attributes['tipList'][questionIndex]
            session.attributes['question'] = question_msg
            session.attributes['tip'] = tip_msg
            session.attributes['numberOfQuestions'] += 1
            session.attributes['questionList'].pop(questionIndex)
            session.attributes['tipList'].pop(questionIndex)
            sys.stderr.write('-----------------------[Q number]----> '+str(str(session.attributes['numberOfQuestions']))+'\n')

            record(Freeform)
            return question(question_msg)
   
   
def record(Freeform):
    global pos, neg, emp
    session.attributes['state'] = 'Recording'
    sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()
         
    words = Freeform 
    sys.stderr.write('------------------------------------------------------------')
    sys.stderr.write(words +'\n')
    sys.stderr.flush()


    pos_words = ['focus', 'hard-working',  'dedication', 'thank you', 'appreciate', 'diligent', 'motivation', 'initiative', 'grateful', 'determined', 'dynamic', 'mature', 'independent', 'happy', 'enjoy', 'splendid', 'goal', 'interested', 'opportunity', 'individual', 'fortunate', 'incredible', 'inspire', 'influence', 'achieve', 'honest', 'benefit', 'willing', 'effort', 'fantastic', 'balance', 'interact', 'enlightening', 'culture', 'innovation', 'involved', 'leadership', 'diverse', 'multicultural' ]
    neg_words = ['nigger', 'smarter than', 'hate', 'dumb', 'stupid', 'ugly', 'lame', 'weird', 'nasty', 'terrible', 'horrible', 'awful', 'heck', 'darn', 'poop', 'shit', 'fuck', 'damn', 'hell', 'ass', 'bitch', 'cunt', 'cock', 'pussy', 'dick', 'asshole', 'ass', 'safety school', 'backup school', 'sucks', 'blows', 'obsessed', 'shucks', 'drugs', 'alcohol', 'avoid', 'worst', 'desperate', 'failure', 'you know', 'you guys', 'bad', 'negative', 'dang']
    emp_words = ['sorry', 'kind of', 'sort of', 'amazing', 'basically', 'actually', 'so', 'stuff', 'sure', 'yeah', 'I don’t know', 'well', 'maybe', 'technically', 'I think', 'mostly', 'wait', 'I guess']
    pos_words = "|".join(pos_words)
    neg_words = "|".join(neg_words)
    emp_words = "|".join(emp_words)
    pos += len(re.findall(pos_words, Freeform))
    neg += len(re.findall(neg_words, Freeform))
    emp += len(re.findall(emp_words, Freeform))

    
@ask.intent("RepeatIntent")
def repeatQuestion():
    if(session.attributes['state'] == 'Recording'):
        session.attributes['state'] = 'Repeat'
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    return question(session.attributes['question'])

@ask.intent("TipIntent")
def tip():
    if( session.attributes['numberOfQuestions'] == 1 ):
        session.attributes['state'] = 'Tip'
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        tip_msg = 'Try to portray yourself as someone unique. Describe your personality without making it sound cliche. Try to talk for around a minute..' + '    ' + 'Say: continue, to move to the next question'
        return question(tip_msg)
        
    else:
        session.attributes['state'] = 'Tip'
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        tip_msg = session.attributes["tip"]
        next_msg = "Say: continue, to move to the next question"
        return question(tip_msg + "   " + next_msg)

@ask.intent("AMAZON.NoIntent")
def all_done():
    global pos, neg, emp
    sys.stderr.write('\n-----------------------[OLD state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()

    # the user bails immediately; i.e. no games were played. Express regret
    if session.attributes['state'] == 'Hello': # origin state
        # starement() says something then exists immediately
        session.attributes['state'] = 'Goodbye' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
        msg = 'Ah well...you could’ve gotten into college! Maybe next time pal! Goodbye'
        return statement(msg)

    else:
        return feedback()
    



# get the recognition, speak it back and show on the screen

if __name__ == '__main__':
    app.run(debug=True)






