# 単語学習

import sys, io
import cgi
from R02_sql import prepare, choose, update
import sqlite3

con = sqlite3.connect('words.sqlite3')
cur = con.cursor()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form = cgi.FieldStorage()

partOfSpeech = form.getvalue('partOfSpeech', 'all')
familiarity = form.getvalue('familiarity', 'all')
mode = form.getvalue('mode', 'meaning')
order = form.getvalue('order', 'normal')
next = form.getvalue('next', '')

#next='dream,2,meaning,normal'
action = ''
if next != '':
    action = next.split(',')
    print(action)
    pre_word = action[0]
    new_f = action[1]
    mode = action[2]
    order = action[3]
    update(cur, con, pre_word, int(new_f))

else:
    prepare(partOfSpeech, familiarity,  cur, con)


cur.execute("""SELECT count(*) FROM studyPlus WHERE state=1 """)
count = cur.fetchone()[0]


template = """
<html>
<head>
    <title>英英辞書-学習モード</title>
    <meta http-equiv="content-type" charset="utf-8">
    <link rel="stylesheet" type="text/css" href="../css/stylesheet.css">
</head>
<body>
<div id="center">
<a href="/cgi-bin/19K1109-R02-searchMode.py?clear=1" class="border_spread_btn">検索モード</a> 
&ensp;&ensp;
<p class="btn-border-bottom" style="font-size:16px">学習モード</p></br>"""

# 未学習の単語がなくなるとき
if count == 0:
    template += """
                <p> 今回の学習が終わりました。よく頑張りました！</p>
                """

else:
    #cur.execute("""UPDATE studyPlus SET state=0""")
    #con.commit
    cur.execute("""SELECT * FROM studyPlus """)
    print(cur.fetchall())

    w_list = choose(order, cur)[0]
    l_word = w_list[0]
    meaning = w_list[1]
    partOfSpeech = w_list[2]
    synonym = w_list[3]
    if synonym == '':
        synonym = l_word

    if mode == 'meaning':
        template += f"""
            <h2>{l_word}</h2>

        <div class="hidden_box">
        <input type="checkbox" id="label1" />
        <label for="label1">意味を見る</label>
        <div class="hidden_show">
          <!--非表示ここから-->     
          <p style="font-weight:bold">{partOfSpeech}.</p>
          <P>{meaning}</p>
          <!--ここまで-->
        </div>
        </div>
        """.format(l_word=l_word, partOfSpeech=partOfSpeech, meaning=meaning)


    elif mode == "synonym":
        template += f"""
        <h2>{synonym}</h2>
        <div class="hidden_box">
        <input type="checkbox" id="label1"/>
        <label for="label1">単語を見る</label>
        <div class="hidden_show">
          <!--非表示ここから-->
        <h2> {l_word} </h2>
        <p style="font-weight:bold">{partOfSpeech}.</p>
        <p> {meaning}</p>
          <!--ここまで-->
        </div>
        </div>
        """.format(synonym=synonym, l_word=l_word, partOfSpeech=partOfSpeech, meaning=meaning)

    value0 = l_word + ',0,' + mode + ',' + order
    value1 = l_word + ',1,' + mode + ',' + order
    value2 = l_word + ',2,' + mode + ',' + order

    template += f"""
        <form method="GET" 
        action="/cgi-bin/19K1109-R02-study.py">
        <label><input name="next" type="radio" value={value0}>覚えられない</label> 
        <label><input name="next" type="radio" value={value1}>うろ覚え</label>
        <label><input name="next" type="radio" value={value2} checked="checked" >覚えた</label> 
        <br/><br/><button type="submit">次へ→</button>
        </form></br>
        """.format(value0=value0, value1=value1, value2=value2)


template += """
    <form method="GET" action="/cgi-bin/19K1109-R02-studyMode.py?clear=1">
    <button type="submit">戻る</button>
    </form>
</div>
</body>
</html>
"""

print("Content-type text/html\n")
print(template)
