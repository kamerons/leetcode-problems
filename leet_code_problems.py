#!/usr/bin/env python3
# from the following gist: https://gist.github.com/akshaykarnawat/6479579a351f6fe52aab4042829ca967
import requests
import json
import os

RED = "\033[0;31m"
GREEN = "\033[0;32m"
NC = "\033[0m"

LOC_TO_STORE = os.getcwd()

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
difficulty_as_string_map = {1: "easy", 2: "medium", 3: "hard"}
for difficulty in problems:
    difficulty_as_string = difficulty_as_string_map[difficulty]

    print("Beginning difficulty: %s%s%s" % (GREEN, difficulty_as_string, NC))
    # create a new folder in local path
    if not os.path.exists('/'.join([LOC_TO_STORE, str(difficulty_as_string)])):
        os.makedirs('/'.join([LOC_TO_STORE, str(difficulty_as_string)]))

    problemItems = problems.get(difficulty).items()
    for idx, (title, pUrl) in enumerate(problemItems):
        print("Problem %d of %d for %s" % (idx + 1, len(problemItems), difficulty_as_string))
        res = requests.get(HEX_LIKE_URL_1 + title + HEX_LIKE_URL_2)
        if res.status_code != 200:
            continue

        d = json.loads(res.text)

        quesData = d.get('data', {}).get('question', {})
        titleSlug = quesData.get('titleSlug', '')
        content = quesData.get('content', '')
        if content is None:
            continue

        # save data to local folder
        with open('{0}/{1}/{2}.html'.format(LOC_TO_STORE, difficulty_as_string, titleSlug), 'w+') as f:
            try:
                f.writelines(content)
                f.close()
            except Exception as e:
                print('%s%s had a problem while saving!%s' % (RED, title, e.args[0], NC))
