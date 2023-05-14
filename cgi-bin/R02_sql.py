# SQL関数まとめ

import sqlite3

"""
con = sqlite3.connect('../words.sqlite3')
cur = con.cursor()
cur.execute("SELECT * FROM studyPlus ")
print(cur.fetchall())
"""

def addToList(addword, meaning, partOfSpeech, synonym, cur, con):
    try:
        cur.execute("""CREATE TABLE words
                     (word text, meaning text, partOfSpeech int, synonym text)""")
        cur.execute("""CREATE TABLE studyPlus (word text, familiarity int, state int)""")
    except:
        pass
    # 単語がすでに存在するかと確認する
    cur.execute("""SELECT count(*) FROM words WHERE word=(?)""", (addword,))
    if cur.fetchone()[0] == 0:
        print("none")
        cur.execute("""INSERT INTO words VALUES (?, ?, ?, ?)""", (addword, meaning, partOfSpeech, synonym,))
        cur.execute("""INSERT INTO studyPlus (word, familiarity, state) VALUES (?, ?, ?)""", (addword, 0, 0,))
        message = "追加されました。"
    else:
        message = addword + "はすでに単語リストにあります。"
    con.commit()
    cur.execute("""SELECT * FROM words """)
    print(cur.fetchall())
    return message


def search_pos(cur):
    cur.execute("""SELECT partOfSpeech FROM words GROUP BY partOfSpeech""")
    return cur.fetchall()


def search_f(cur):
    cur.execute("""SELECT familiarity FROM studyPlus GROUP BY familiarity""")
    return cur.fetchall()


def prepare(partOfSpeech, familiarity, cur, con):

    if partOfSpeech == 'all' and familiarity == 'all':
        cur.execute("""UPDATE studyPlus SET state = 1 """)
    elif partOfSpeech == 'all' and familiarity != 'all':
        cur.execute("""UPDATE studyPlus SET state = 1 WHERE word IN 
                   (SELECT word FROM words WHERE familiarity=?)""",
                    (familiarity,))
    elif partOfSpeech != 'all' and familiarity == 'all':
        cur.execute("""UPDATE studyPlus SET state = 1 WHERE word IN 
                   (SELECT word FROM words WHERE partOfSpeech=?)""",
                    (partOfSpeech,))
    else:
        cur.execute("""UPDATE studyPlus SET state = 1 WHERE word IN 
        (SELECT word FROM words WHERE partOfSpeech=?, familiarity=?)""",
                    (partOfSpeech, int(familiarity)))  # state = 1 学習予定
    con.commit()


def choose(order, cur):
    if order == "normal":
        cur.execute("""SELECT * FROM words WHERE word IN 
        (SELECT word FROM studyPlus WHERE state = 1) LIMIT 1""")
    elif order == "random":
        cur.execute("""SELECT * FROM words WHERE word IN 
        (SELECT word FROM studyPlus WHERE state = 1) ORDER BY RANDOM() LIMIT 1""")
    elif order == "initial":
        cur.execute("""SELECT * FROM words WHERE word IN 
        (SELECT word FROM studyPlus WHERE state = 1) ORDER BY word LIMIT 1""")
    word_all = cur.fetchall()
    return word_all

# 学習した後に状態更新
def update(cur, con, word, f):
    cur.execute("""UPDATE studyPlus SET familiarity = ?, state=0 WHERE word = ? """,
                (f, word,))
    con.commit()

#update(cur,con,'dream', 2)

#cur.execute("SELECT * FROM studyPlus ")
#print(cur.fetchall())
#search_pos(cur)
# [('adjective',), ('adverb',), ('noun',)]

#cur.execute("""SELECT a.word, a.partOfSpeech, b.familiarity FROM words a LEFT JOIN studyPlus b ON a.word=b.word""")
#print(cur.fetchall())

#con.close()