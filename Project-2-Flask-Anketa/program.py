
import json
from flask import Flask
from flask import url_for, render_template, request

app = Flask(__name__)

def file_creator():
    file = open('/Users/macbook/Desktop/HSE void/Flask prog/project_AGAIN/stats.txt', 'w', encoding='UTF-8')
    title = 'Namae' + '\t' + 'Machi' + '\t' + 'Shitsumon_1' + '\t' + 'Shitsumon_2' + '\t' + 'Shitsumon_3' + '\t' + 'Shitsumon_4' + '\t' + 'Shitsumon_5' + '\t' + 'Shitsumon_6' + '\t' + 'Shitsumon_7' + '\n'
    file.write(title)
    file.close()

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/stats')
def stats():
    i = 0
    if request.args:
        namae = request.args['namae']
        machi = request.args['machi']
        old = request.args['old']
        gend = request.args['gend']
        q1 = request.args['q1']
        q2 = request.args['q2']
        q3 = request.args['q3']
        q4 = request.args['q4']
        q5 = request.args['q5']
        q6 = request.args['q6']
        q7 = request.args['q7']
        file = open ('/Users/macbook/Desktop/HSE void/Flask prog/project_AGAIN/stats.txt', 'a', encoding='UTF-8')
        file.write( namae + '\t' + machi + '\t' + old + '\t' + gend + '\t' + q1 + '\t' + q2 + '\t' + q3 + '\t' + q4 + '\t' + q5 + '\t' + q6 + '\t' + q7 + '\n')
        if q1 != 'ГЕнезис':
            i += 1
        if q2 != 'МАркетинг':
            i += 1
        if q3 != 'ягодИцы':
            i += 1
        if q5 != 'сОгнутый':
            i += 1
        if q6 != 'судЕй':
            i += 1
        if q7 != 'квартАл':
            i += 1
        file.close()
        urls = {'Пройти опрос еще раз': url_for('main_page'),
                'Вернуть Json файл': url_for('come_back_json'),
                'Начать поиск по пройденым анкетам': url_for('search'), }

        return render_template('stats.html', namae=namae, machi=machi, old=old, gend = gend, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, i=i, urls=urls)

@app.route('/json')
def come_back_json():
    d = dict(Namae = [], Machi = [], old=[], gend = [], Shitsumon_1 = [], Shitsumon_2 = [], Shitsumon_3 = [], Shitsumon_4 = [], Shitsumon_5 = [], Shitsumon_6 = [], Shitsumon_7 = [])
    file_for_json = open('/Users/macbook/Desktop/HSE void/Flask prog/project_AGAIN/stats.txt', 'r', encoding='UTF-8')
    for line in file_for_json:
        if 'Namae' in line:
            continue
        arr = line.split('\t')
        d['Namae'].append(arr[0])
        d['Machi'].append(arr[1])
        d['old'].append(arr[2])
        d['gend'].append(arr[3])
        d['Shitsumon_1'].append(arr[4])
        d['Shitsumon_2'].append(arr[5])
        d['Shitsumon_3'].append(arr[6])
        d['Shitsumon_4'].append(arr[7])
        d['Shitsumon_5'].append(arr[8])
        d['Shitsumon_6'].append(arr[9])
        d['Shitsumon_7'].append(arr[10])
    data = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    urls = {'Пройти опрос еще раз': url_for('main_page'),}
    return render_template('json.html', urls=urls, data=data)

@app.route('/search')
def search():
    urls = {'Вернуться к стартовой анкетеме': url_for('main_page'),}
    return render_template('search.html', urls=urls)

@app.route('/result')
def result():
    block = []
    argg = request.args['argg']
    argg_name = request.args['argg_name']
    if argg != 'find_name':
        search_file = open('stats.txt', 'r', encoding='UTF-8')
        for line in search_file:
            if 'Namae' in line:
                continue
            arr = line.split('\t')
            if arr[3] == argg:
                block.append(arr)
        search_file.close()

    elif argg == 'find_name':
        search_file = open('stats.txt', 'r', encoding='UTF-8')
        for line in search_file:
            if 'Namae' in line:
                continue
            arr = line.split('\t')
            if arr[0].strip(' ') == argg_name:
                block.append(arr)
        search_file.close()
    urls = {'Вернуться к стартовой анкете': url_for('main_page'),}
    return render_template('result.html', argg=argg, argg_name=argg_name, block=block, urls=urls)

if __name__ == '__main__':
    #t = file_creator()
    app.run(debug=True)