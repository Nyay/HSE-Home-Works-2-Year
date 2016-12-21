import os
import re
from flask import Flask
from flask import url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/result')
def result():
    file_name = request.args['file_name']
    file_name = file_name + '.txt'
    text_enter = request.args['text_to_prog']
    f_out = open('mystem_base.txt','w', encoding='UTF-8')
    text = text_enter.split()
    text = set(text)
    text = ' '.join(text)
    text_free = text.strip(',.!?-_')
    low_text = text_free.lower()
    f_out.write(low_text)
    f_out.close()
    os.system('/Users/macbook/Downloads/mystem -di ' + '/Users/macbook/Desktop/HSE-Home-Works-2-Year/sql_hw/mystem_base.txt ' + '/Users/macbook/Desktop/HSE-Home-Works-2-Year/sql_hw/text_ms.txt ')
    full = []
    file_enter = open('text_ms.txt', 'r', encoding='UTF-8')
    file_exit = open(file_name, 'w', encoding='UTF-8')
    f = file_enter.read()
    result = re.findall('(.+?)\{(.+?)=.+?\}', f, flags=re.DOTALL)
    for element in result:
        line = 'insert into DBT3 (Форма, Лемма) values ("' + element[0] + '","' + element[1] + '");'
        full.append(line)
    final = '\n'.join(full)
    file_exit.write(final)
    file_enter.close()
    file_exit.close()
    urls = {'Вернуться к введению текста': url_for('main_page'), }
    return render_template('result.html', urls=urls)

if __name__ == '__main__':
    app.run()