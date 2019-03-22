import requests
import json
import time
import os

LOC_TO_STORE = '/Volumes/ExPac/dev/python/leet_code_problems'

LEET_CODE_URL = 'https://leetcode.com'
LEET_CODE_GRAPHQL_URL = 'https://leetcode.com/graphql' 

# get all the problems and take only the needed information
request = requests.get('/'.join([LEET_CODE_URL, 'api/problems/all/']))
data = json.loads(request.text)
problems = {}
_ = [problems.setdefault(p.get('difficulty', {}).get('level', ''), {}).setdefault(p.get('stat', {}).get('question__title_slug'), 
        '/'.join([LEET_CODE_URL, 'problems', p.get('stat', {}).get('question__title_slug')]))
        for p in data.get('stat_status_pairs')]

# create a payload to send to graph ql to get the questions data
payload = {
    "operationName" : "questionData",
    "variables" : {"titleSlug":"two-sum"},
    "query"  : '''\
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            title
            titleSlug
            content
        }
    }
    ''',
}

HEX_LIKE_URL_1 = '''https://leetcode.com/graphql?operationName=questionData&variables={%22titleSlug%22:%22''' 
HEX_LIKE_URL_2 = '''%22}&query=query%20questionData($titleSlug:%20String!)%20{%20%20%20%20%20question(titleSlug:%20$titleSlug)%20{%20%20%20%20%20%20%20%20%20titleSlug%20%20%20%20%20%20%20%20%20content%20%20%20%20%20}%20}'''


# get to the problem one by one and start downloading based on difficulty
# 1 = EASY; 2 = MEDIUM; 3 = HARD
for difficulty in problems:
    
    # create a new folder in local path
    if not os.path.exists('/'.join([LOC_TO_STORE, str(difficulty)])):
        os.makedirs('/'.join([LOC_TO_STORE, str(difficulty)]))

    for title, pUrl in problems.get(difficulty).items():
        res = requests.get(HEX_LIKE_URL_1 + title + HEX_LIKE_URL_2)
        if res.status_code != 200:
            continue

        d = json.loads(res.text)

        quesData = d.get('data', {}).get('question', {})
        titleSlug = quesData.get('titleSlug', '')
        content = quesData.get('content', '')

        # save data to local folder
        with open('{0}/{1}/{2}.html'.format(LOC_TO_STORE, str(difficulty), titleSlug), 'w+') as f:
            try:
                f.writelines(content)
                f.close()
            except Exception as e:
                print(title, 'had a problem while saving!', e.args[0])

        # maybe wait a little so that server does seem like there is something fishy with all the pulls
        # although I doubt this even matters since 30 sec is not enough of a wait; they will know regardless
        # since we are pulling everything all
        # time.sleep(30)