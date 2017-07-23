import sys
import re
import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

# first regular expression 'w' and then every time after that do 'a'
@ask.launch
def beginInterview():
    if 'hello' in session.attributes:
        prefix = ''
    else:
        session.attributes['hello'] = 1
    # do I need and sessions?
    session.attributes['state'] = 'Hello' # set state as what you are in
    session.attributes['numberOfQuestions'] = 0
    session.attributes['question']  = None #question number asked
    hello_msg = render_template('hello')
    return question(hello_msg) # makes alexa ask question

@ask.intent("AMAZON.YesIntent")
def instructions():

    sys.stderr.write('\n-----------------------[OLD state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()

    # the user bails immediately; i.e. no games were played. Express regret
    if session.attributes['state'] == 'Hello': # origin state
        
        session.attributes['state'] = 'Instruction' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    instruction_msg = render_template('instruction')
    return question(instruction_msg)
    
    
@ask.intent("GreetingIntent")
def greeting():

    if session.attributes['state'] == 'Instruction': # origin state
        
        session.attributes['state'] = 'Greeting' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    greeting_msg = render_template('greeting')
    return question(greeting_msg)

# I want to have a gretting response that is for when the user does not ask the interviewer how they are doing and alexa will give a tip before moving on 
@ask.intent("GoodGreetingResponseIntent")
def greetingResponse():
    if session.attributes['state'] == 'Greeting': # origin state
        
        session.attributes['state'] = 'GreetingResponse' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    prefix = render_template('greeting_response')
    greeting_response_msg = prefix + render_template('first_question')
    session.attributes['numberOfQuestions'] = 1
    return question(greeting_response_msg)

# the question asking random generating doesn't work yet:(
"""@ask.intent("AnythingIntent")
def generateQuestion():
    if session.attributes['state'] == 'GreetingResponse':
         session.attributes['state'] = 'Question'
         sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
         sys.stderr.flush()
    questionNumber = randint(1, 10)
    question_msg = render_template('questionNumber')
    session.attributes['numberOfQuestions'] += 1
    return question(question_msg)"""
        

@ask.intent("AMAZON.NoIntent")
def all_done():

    sys.stderr.write('\n-----------------------[OLD state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()

    # the user bails immediately; i.e. no games were played. Express regret
    if session.attributes['state'] == 'Hello': # origin state
        # starement() says something then exists immediately
        session.attributes['state'] = 'Goodbye' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    msg = 'Ah well...you could’ve gotten into college! Maybe next time pal! Goodbye'
    
    if session.attributes['state'] != 'Hello':
        session.attributes['state'] = 'Goodbye2'
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    msg = 'Well then, I hope you had a nice interview'

    return statement(msg)



if __name__ == '__main__':
    app.run(debug=True)






