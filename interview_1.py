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
    #hello_msg = render_template('hello')
    hello_msg = "Welcome to College Interview. Ready to practice?"
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
    #instruction_msg = render_template('instruction')
    instruction_msg = "Say Repeat Question to hear the question again, say Next Question  to move on, and say End Interview to end the interview and receive your feedback. If you are ready to start your interview say. start my interview."
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


@ask.intent("QuestionIntent")
def generateQuestion(Freeform):
    #words = str(scooby)
    if (session.attributes['state'] == 'Greeting' and session.attributes['numberOfQuestions'] == 0):
         session.attributes['state'] = 'Question'
         sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
         sys.stderr.flush()
      #   prefix = render_template('greeting_response')
         greeting_response_msg = "I am good, thank you, Tell me about yourself. "
         session.attributes['numberOfQuestions'] == 1
         return question(greeting_response_msg)
    
    else: 
         session.attributes['state'] = 'Question'
         sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
         sys.stderr.flush()
         with open('questions.yaml') as f:
            questions = yaml.load(f.read())
         question_msg = random.choice(questions)
         session.attributes['numberOfQuestions'] += 1
         session.attributes['state'] = 'Recording'
         sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
         sys.stderr.flush()
   #words isn't a thing right now - FIXXXXXX
    words = Freeform 
    sys.stderr.write('------------------------------------------------------------')
    sys.stderr.write(words +'\n')
    sys.stderr.flush()
    
    with open('user_responses.txt', 'a') as fout:
        fout.write(words+'\n')

    msg = 'i heard: . {}... '.format(words)

    with open('user_response.txt') as speech_text:
        stxt =   speech_text.read()
    
        statement = str((len(re.findall(r'\w*ing',stxt))))

    return question(question_msg)
         



# write the input to a text file

#    return question(statement+' do you want to try again?')
        

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


# get the recognition, speak it back and show on the screen
@ask.intent("AnswerIntent")
def answer(wa):
    if session.attributes['state'] == 'Question':
         session.attributes['state'] = 'Recording'
         sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
         sys.stderr.flush()
   #words isn't a thing right now - FIXXXXXX
    words = wa
    sys.stderr.write('------------------------------------------------------------')
    sys.stderr.write(words+'\n')
    sys.stderr.flush()


# write the input to a text file
    with open('user_responses.txt', 'w') as fout:
        fout.write(words+'\n')

    msg = 'i heard: . {}... '.format(words)

    with open('user_response.txt') as speech_text:
        stxt =   speech_text.read()
    
        statement = str((len(re.findall(r'\w*ing',stxt))))

    return question(statement+' do you want to try again?')




if __name__ == '__main__':
    app.run(debug=True)






