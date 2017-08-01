session.attributes['rating']=0
neg = len(re.findall(neg_words))
pos = len(re.findall(pos_words))
emp = len(re.findall(emp_words))
neg *= (-0.75)
pos *= 1
emp *= (-0.25)
session.attributes['rating'] = neg + pos + emp
rating = session.attributes['rating']
round_msg = 'Your interview rating based on your responses was a {}.'.session.attributes['rating']
if rating > 0:
    return statement(round_msg + ' You had a pretty positive interview!')
if rating < 0:
    return statement(round_msg + ' You used more negative and empty words than positive words by a wide margin. Try to be a tad bit more positive in your actual interview.')
if rating == 0:
    return statement(round_msg + ' You had an equal mix of positive and negative and empty words in your interview. Try to be more positive in your actual interview.')
