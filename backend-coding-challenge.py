# pylint: disable=C0326
# pylint: disable=C0303

from flask import Flask
import requests
import os
from datetime import date, timedelta
import json

app = Flask(__name__)

class Language:
    def __init__(self, lang_name, num_repos, list_repos):
        self.language_name = lang_name
        self.num_repos = num_repos
        self.list_repos = list_repos

@app.route("/languages", methods=['GET'])
def languages_list():
    date_month_ago = (date.today()-timedelta(days=30)).isoformat()
    
    query_url = f'https://api.github.com/search/repositories?q=created:>{date_month_ago}&sort=stars&order=desc&per_page=100'
    r = requests.get(query_url)
    r = r.json()

    lang_name_list = []
    
    for item in r['items']:
        lang_name_list.append(item['language'])

    lang_name_list = list(set(lang_name_list))

    lang_object_list = []

    for x in lang_name_list:
        repos_num = 0
        repos_list = []
        for item in r['items']:
            if x == item['language']:
                repos_num += 1
                repos_list.append(item['html_url'])
        lang_object_list.append( Language(x, repos_num, repos_list))

    result = json.dumps([ob.__dict__ for ob in lang_object_list])
    return result


if __name__ == '__main__':
    app.run(debug=True)