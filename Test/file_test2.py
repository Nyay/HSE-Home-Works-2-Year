import re
import json
from flask import Flask
from flask import url_for, render_template, request

app = Flask(__name__)

def num1():
    global dic_web
    dic_main = {}
    dic_json = {}
    dic_web = {}
    f1 = open('udm_lexemes_ADJ.txt', 'r', encoding='UTF-8')
    base1 = f1.read()
    f2 = open('udm_lexemes_IMIT.txt', 'r', encoding='UTF-8')
    base2 = f2.read()
    f3 = open('udm_lexemes_N.txt', 'r', encoding='UTF-8')
    base3 = f3.read()
    result1 = re.findall('lex: (.+?)\\n.+?gramm: (.+?)\\n.+?trans_ru: (.+?)\\n.+?', base1, flags=re.DOTALL)
    result2 = re.findall('lex: (.+?)\\n.+?gramm: (.+?)\\n.+?trans_ru: (.+?)\\n.+?', base2, flags=re.DOTALL)
    result3 = re.findall('lex: (.+?)\\n.+?gramm: (.+?)\\n.+?trans_ru: (.+?)\\n.+?', base3, flags=re.DOTALL)
    for element in result1:
        dic_main[element[0]] = (element[1], element[2])
        dic_json[element[2]] = (element[1], element[0])
        dic_web[element[0]] = (element[2])
    for element in result2:
        dic_main[element[0]] = (element[1], element[2])
        dic_json[element[2]] = (element[1], element[0])
        dic_web[element[0]] = (element[2])
    for element in result3:
        dic_main[element[0]] = (element[1], element[2])
        dic_json[element[2]] = (element[1], element[0])
        dic_web[element[0]] = (element[2])
    data = json.dumps(dic_main, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    data2 = json.dumps(dic_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    file_json = open('file_json.json', 'w', encoding='UTF-8')
    file_json.write(data)
    file_json.close()
    file_json_RUS = open('file_json_RUS.json', 'w', encoding='UTF-8')
    file_json_RUS.write(data2)
    file_json_RUS.close()

num1()

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/result')
def stats():
    if request.args:
        find_word = request.args['find_this']
        find_word = str(find_word)
        find_word.lower()
        result = str(dic_web[find_word])
        result.strip('()')
    return render_template('result.html', result = result)

if __name__ == '__main__':
    app.run()