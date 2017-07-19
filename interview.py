import sys
import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

@ask.launch
def beginInterview():
    if 'hello' in session.attributes:
        prefix = ''
    else:
        session.attributes['hello'] = 1
        prefix = 'Welcome to College Interview Prep...'
    # do I need and sessions?
    session.attributes['state'] = 'Hello' # set state as what you are in
    session.attributes['numberOfQuestions'] = 0
    task_msg = prefix+render_template('task')
    return question(task_msg) # makes alexa ask question

@ask.intent("NoIntent")
def all_done():

    sys.stderr.write('\n-----------------------[OLD state]----> '+str(session.attributes['state'])+'\n')
    sys.stderr.flush()

    # the user bails immediately; i.e. no games were played. Express regret
    if session.attributes['state'] == 'Hello': # origin state
        # starement() says something then exists immediately
        session.attributes['state'] = 'Goodbye' # set current state
        sys.stderr.write('-----------------------[NEW state]----> '+str(session.attributes['state'])+'\n')
        sys.stderr.flush()
    msg = 'Good luck on your interview.. I guess... Goodbye.'
    return statement(msg)



if __name__ == '__main__':
    app.run(debug=True)






