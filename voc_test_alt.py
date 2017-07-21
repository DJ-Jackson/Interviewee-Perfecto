#
# recognition tester
#

import sys
import logging
import re
import nltk #for keyword search
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session



# print things to the command window
def trace(string):
    sys.stderr.write(string+'\n')
    sys.stderr.flush()
    return

app = Flask(__name__)
ask = Ask(app, "/")
# uncomment to see the .json traffic between your skill and alexa
# logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# skill starts here
@ask.launch
def new_game():
    welcome_msg = render_template('voctest')
    return question(welcome_msg+' speak something...')


# to try a different input
@ask.intent("YesIntent")
def next_round():
    trace('  ===> YES')
    round_msg = 'ok, say a sentence...'
    return question(round_msg)

# to quit
@ask.intent("NoIntent")
def all_done():
    trace('  ===>  NO')
    return statement('ok, see you next time...')

# get the recognition, speak it back and show on the screen
@ask.intent("AnswerIntent")
def answer(wa):
    words = wa
    trace('------------------------------------------------------------')
    trace(words+'\n')

# write the input to a text file
    with open('voc_strings.txt', 'w') as fout:
        fout.write(words+'\n')


    msg = 'i heard: . {}... '.format(words)

    with open('voc_strings.txt') as speech_text:
        stxt =   speech_text.read()
    
        statement = str((len(re.findall(r'\w*ing',stxt))))

    return question(statement+' do you want to try again?')

# search for keywords





##########################

""" To do:
 add in state for appending instead of writing file
 create a keywords search function with regular expressions
"""


##########################
if __name__ == '__main__':
    app.run(debug=True)
    
# re.findall('|'.join(neg_words),s) -- for finding negative words in a string
# add on len( at the beginning to count occurrences
