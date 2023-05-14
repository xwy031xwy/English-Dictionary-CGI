
# 検索結果＆単語リスト＆SQL

import requests
import sys, io
import cgi
from sql import addToList
import sqlite3

con = sqlite3.connect('words.sqlite3')
cur = con.cursor()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form = cgi.FieldStorage()

word = form.getvalue('word', '')
additions = form.getlist('search')
addWord = form.getvalue('addToList', '')
#word = 'dream'
#addWord = 'dream'

def search(word):
    global response
    url = "https://wordsapiv1.p.rapidapi.com/words/" + word

    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': "dccbc5c110msh1de7cf0489a9b50p147a10jsn175e72c00f4b"
    }

    response = requests.request("GET", url, headers=headers)
    response.enconding = "utf-8"
    response = response.json()  # jsonの形に変える


if addWord != '':
    search(addWord)
    partOfSpeech = response['results'][0]['partOfSpeech']
    print(partOfSpeech)
    meaning = response['results'][0]['definition']
    print(meaning)
    if response['results'][0]['synonyms']:
        synonym = response['results'][0]['synonyms'][0]
    else:
        synonym = ''
    print(synonym)
    word = addToList(addWord, meaning, partOfSpeech, synonym, cur, con)
    print(word)
    syllables = ''
    pronunciation = ''
    results = ''
    add = ''

elif word != '':
    try:
        search(word)
        # 音節
        syllables = '<p id="small">'
        for i in range(len(response['syllables']['list'])):
            syllables += response['syllables']['list'][i]
            if i != len(response['syllables']['list']) - 1:
                syllables += '・'
        print(syllables)
        # 発音
        pronunciation = ''
        for i in response['pronunciation']:
            pronunciation += i + ':/' + response['pronunciation'][i] + '/ '

        pronunciation += '</p>'
        print(pronunciation)
        # 意味
        #additions = ['examples', 'synonyms']
        trans = {'synonyms': '同意語', 'examples': '例文・イディオム', 'derivation': '語源'}

        results = '<div id="content">'
        for i in range(len(response['results'])):
            type = response['results'][i]['partOfSpeech']
            results += '<p><h4>' + str(i + 1) + '. ' + \
                       type + ' </h4>' + response['results'][i]['definition'] + '</p>'
            for j in additions:
                if j in response['results'][i]:
                    results += '<h4>' + trans[j] + '</h4>'
                    for n in response['results'][i][j]:
                        results += '<p>' + n + '</p>'
                else:
                    results += '<h4>' + trans[j] + '</h4>' + '<h4> なし </h4>'
        results += '</div>'
        add = '<form method="GET" action="/cgi-bin/results.py">'
        add += f'<button name="addToList" type="submit" value={word}>＋単語リスト</button></form>'.format(word=word)

    except:
        word = '一致する単語は見つかりませんでした。'
        syllables = ''
        pronunciation = ''
        results = ''
        add = ''

elif addWord == '' and word == '':
    word = 'もう一度入力してください。'
    syllables = ''
    pronunciation = ''
    results = ''
    add = ''



template = """

<html>
<head>
    <title>英英辞書-検索モード</title>
    <meta http-equiv="content-type" charset="utf-8">
    <link rel="stylesheet" type="text/css" href="../css/stylesheet.css ">
</head>
<body>
<div id="center">
<p class="btn-border-bottom" style="font-size:16px">検索モード</p> &ensp;&ensp;
<a href="/cgi-bin/studyMode.py" class="border_spread_btn">学習モード</a></br>
    <h1 style="font-size:24px">{word} </h1>
    <pre>{syllables}  {pronunciation}</pre></p>
    <pre> {add}{results} </pre>
    <form method="GET" action="/cgi-bin/searchMode.py">
    <button type="submit">戻る</button>
    </form>

</div>
</body>
</html>
"""

result = template.format(word=word, syllables=syllables,
                         pronunciation=pronunciation,
                         results=results, add=add)

print("Content-type text/html\n")
print(result)
