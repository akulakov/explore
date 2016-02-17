# format: question, y/n, difficulty level
question_list = """
del statement accepts an object as an arg and removes that object from a list n 2
del statement accepts an object as an arg and removes that object from a dictionary n 2 
del statement deletes a name from current namespace y 2
del statement removes given object from a list or a dictionary y 2
one of the functions in logging module is `loginfo` n 4
one of the functions in logging module is `exception` n 4
one of the functions in logging module is `error` y 4
one of the functions in logging module is `info` y 4
one of the functions in logging module is `information` n 4
"""

from collections import defaultdict
questions = defaultdict(list)
lst = [q for q in question_list.split('\n') if q.strip()]
for q in lst:
    q = q.rsplit(maxsplit=2)
    n = int(q[2])
    questions[n].append(q[:2])
