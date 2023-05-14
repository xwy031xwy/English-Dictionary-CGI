# 単語検索＆API

import sys, io
import cgi
import sqlite3

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
form = cgi.FieldStorage()
word = form.getvalue('word', '')
additions = form.getlist('search')
clear = form.getvalue('clear', '')

if clear == '1':
    con = sqlite3.connect('words.sqlite3')
    cur = con.cursor()
    cur.execute("""UPDATE studyPlus SET state=0""")
    con.commit()


template = """
<html>
<head>
    <title>英英辞書-検索モード</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="../css/stylesheet.css ">
</head>
<body>
<div id="center">
<p class="btn-border-bottom" style="font-size:16px">検索モード</p> &ensp;&ensp;
<a href="/cgi-bin/19K1109-R02-studyMode.py" class="border_spread_btn">学習モード</a></br>
    <form method="get" action="/cgi-bin/19K1109-R02-results.py">
    <p>Word:
    <input type="text" name="word"></p>
                                    
        追加検索：<br/>
        <label><input name="search" type="checkbox" value="synonyms" />同意語 </label>
        <label><input name="search" type="checkbox" value="examples" />例文・イディオム </label>
        <label><input name="search" type="checkbox" value="derivation" />語源 </label>
        
        <p> <input type="submit"></p>
</form>

<div>    
</body>
</html>
"""

print("Content-type text/html\n")
print(template)
