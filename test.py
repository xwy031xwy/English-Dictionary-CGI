import requests

word = 'summer'
detail = 'synonym'

url = "https://wordsapiv1.p.rapidapi.com/words/" + word

headers = {
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
    'x-rapidapi-key': "dccbc5c110msh1de7cf0489a9b50p147a10jsn175e72c00f4b"
}

response = requests.request("GET", url, headers=headers)
response.enconding = "utf-8"
response = response.json()  # jsonの形に変える


print(response['word'])
# number of meanings
print(len(response['results']))
print(response['results'])
print(response['syllables']['list'])
# print(response)
# 音節
syllables = ''

for i in range(len(response['syllables']['list'])):
  syllables += response['syllables']['list'][i]
  if i != len(response['syllables']['list']) - 1:
    syllables += '・'
print(syllables)

# 発音
pronunciation = ''
for i in response['pronunciation']:
  pronunciation += i + ':/' + response['pronunciation'][i] + '/ '
print(pronunciation)

# 意味
additions = ['examples', 'synonyms']
trans = {'synonyms': '同意語', 'examples': '例文・イディオム', 'derivation': '語源'}

results = ''
for i in range(len(response['results'])):
    type = response['results'][i]['partOfSpeech']
    results += str(i+1) + '.' + type + ' ' + response['results'][i]['definition'] + '\n'
    for j in additions:
        if j in response['results'][i]:
            results += '<h4>' + trans[j] + '</h4>'
            for n in response['results'][i][j]:
                results += '<p>' + n + '</p>'
        else:
            results += '<h4>'+ trans[j] +'</h4>' + '<p> なし </p>'

print(results)






"""
1.express the need or desire for
2.the verbal act of requesting
3.a formal message requesting something that is submitted to an authority
4.ask (a person) to do something
5.inquire for (information)
"""


"""
{  
         "definition":"speech you make to yourself",
         "partOfSpeech":"noun",
         "synonyms":[  
            "monologue"
         ],
         "typeOf":[  
            "speech",
            "voice communication",
            "speech communication",
            "spoken communication",
            "spoken language",
            "language",
            "oral communication"
         ],
         "derivation":[  
            "soliloquize"
         ]
      },

"""