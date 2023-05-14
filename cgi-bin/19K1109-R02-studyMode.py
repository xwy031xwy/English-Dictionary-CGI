# 学習カスタマイズ＆単語リストチェック


import requests
import sys, io
import cgi
from R02_sql import search_pos, search_f
import sqlite3


con = sqlite3.connect('words.sqlite3')
cur = con.cursor()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form = cgi.FieldStorage()

word = form.getvalue('word', '')
additions = form.getlist('search')

clear = form.getvalue('clear', '')

if clear == '1':
    cur.execute("""UPDATE studyPlus SET state=0""")
    con.commit()



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




try:
    pos_opt = ''
    for i in search_pos(cur):
        pos = i[0]
        print(pos)
        pos_opt += f'<option value={pos}> {pos} </option>'.format(pos=pos)

    f_opt = ''
    for j in search_f(cur):
        if j[0] == 0:
            f = '覚えられない'
            f_opt += f'<option value= "0" > {f} </option>'.format(f=f)
        elif j[0] == 1:
            f = 'うろ覚え'
            f_opt += f'<option value= "1" > {f} </option>'.format(f=f)
        elif j[0] == 2:
            f = '覚えた'
            f_opt += f'<option value= "2" > {f} </option>'.format(f=f)
    cur.execute("""SELECT a.word, a.partOfSpeech, b.familiarity FROM words a LEFT JOIN studyPlus b ON a.word=b.word""")
    table0 = cur.fetchall()
    print(table0)
    table = ''
    table += "<table><tr><th>単語</th><th>品詞</th><th>記憶度</th></tr>"
    for i in table0:
        print('ok')
        print(i)
        word0 = i[0]
        pos0 = i[1]
        if i[2] == 0:
            f0 = '覚えられない'
        elif i[2] == 1:
            f0 = 'うろ覚え'
        elif i[2] == 2:
            f0 = '覚えた'
        table += f"<tr><td>{word0}</td><td>{pos0}</td><td>{f0}</td></tr>".format(word0=word0,
                                                                                    pos0=pos0, f0=f0)

    table += "</table>"
    submit = '<button type="submit">始める</button>'


except:
    pos_opt = ''
    f_opt = ''
    table = '<p>まだ単語が追加されていません。</p>'
    submit = '<p>まだ単語が追加されていません。</p>'


template = """
<!DOCTYPE html>
<html>
<head>
    <title>英英辞書-学習モード</title>
    <meta http-equiv="content-type" charset="utf-8">
    <link rel="stylesheet" type="text/css" href="../css/stylesheet.css">

<body>
<div id="center">
<a href="/cgi-bin/19K1109-R02-searchMode.py" class="border_spread_btn">検索モード</a> &ensp;&ensp;
<p class="btn-border-bottom" style="font-size:16px">学習モード</p></br>
    <h3>出題タイプを選んでください:</h3>
    <form method="GET" action="19K1109-R02-study.py">
    <p>品詞:
    <select name='partOfSpeech'>
    <option value='all'>全て</option>
    <pre>{pos_opt}</pre> 
    </select>
    </p>
    <p>記憶度:
    <select name='familiarity'>
    <option value='all'>全て</option>
    <pre>{f_opt}</pre>
    </select></p>
    <p>モード:
    <select name='mode'>
    <option value='meaning'>意味から</option>
    <option value='synonym'>同意語から</option>
    </select></p>
    <p>順番:
    <label><input name="order" type="radio" value="random" >ランダム順 </label> 
    <label><input name="order" type="radio" value="initial">頭文字順 </label> 
    </p>    
    <pre>{submit}</pre>
 
    </form></br>
        <div class="hidden_box">
        <input type="checkbox" id="label1"/>
        <label for="label1">単語リスト</label>
        <div class="hidden_show">
          <!--非表示ここから-->
            <pre>{table}</pre>
          <!--ここまで-->
        </div>
    </div>
</div>
</body>
</html>
"""

result = template.format(pos_opt=pos_opt, f_opt=f_opt, submit=submit, table=table)

print("Content-type text/html\n")
print(result)
