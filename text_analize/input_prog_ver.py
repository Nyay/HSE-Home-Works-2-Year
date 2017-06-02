from pymystem3 import Mystem
import random
import sqlite3

selector = 'true'


def text_creator(input_text):
    connection = sqlite3.connect('lemmas_plus.db')
    table_name = 'data'
    cursor = connection.cursor()
    list_to_reply = []
    m = Mystem()
    ana = m.analyze(input_text)
    for element in ana:
        if ',' in element['text'] or '.' in element['text'] or '!' in element['text'] or '?' in element['text']:
            reply = element['text'].strip(' ')
            list_to_reply.append(reply)
        elif 'analysis' in element and element['analysis'] != []:
            gr = element['analysis'][0]['gr']
            part_1 = gr.split('=')[0]
            part_2 = gr.split('=')[1]
            if '(' in part_2:
                part_2 = part_2.strip('(')
                part_2 = part_2.strip(')')
                list_of_part_2 = part_2.split('|')
                par = random.sample(list_of_part_2, 1)
                analyze_string = part_1 + ',' + par[0]
                new_list = []
                command = 'SELECT lemma FROM ' + table_name + " WHERE morphological_analysis = '"\
                          + str(analyze_string) + "';"
                cursor.execute(command)
                level_1 = cursor.fetchall()
                for level_2 in level_1:
                    for lemma in level_2:
                        new_list.append(lemma)
                try:
                    lemma_final = random.sample(new_list, 1)
                    list_to_reply.append(lemma_final[0] + ' (' + analyze_string + ')')
                except ValueError:
                    print('error3')
            elif part_2 == '':
                analyze_string = part_1
                new_list = []
                command = 'SELECT lemma FROM ' + table_name + " WHERE morphological_analysis = '" + str(analyze_string)\
                          + "';"
                cursor.execute(command)
                level_1 = cursor.fetchall()
                for level_2 in level_1:
                    for lemma in level_2:
                        new_list.append(lemma)
                try:
                    lemma_final = random.sample(new_list, 1)
                    list_to_reply.append(lemma_final[0])
                except ValueError:
                    print('error1')
            else:
                analyze_string = part_1 + ',' + part_2
                new_list = []
                command = 'SELECT lemma FROM ' + table_name + " WHERE morphological_analysis = '" + str(analyze_string)\
                          + "';"
                cursor.execute(command)
                level_1 = cursor.fetchall()
                for level_2 in level_1:
                    for lemma in level_2:
                        new_list.append(lemma)
                try:
                    lemma_final = random.sample(new_list, 1)
                    list_to_reply.append(lemma_final[0])
                except ValueError:
                    print('error2')
    string_to_reply = ' '.join(list_to_reply)
    string_to_reply = string_to_reply.lower()
    connection.close()
    print('\n' + string_to_reply + '\n')
    return string_to_reply

print('Привет!\nЯ программа, которая отвечает предложением, в котором все слова заменены на какие-то случайные другие'
      ' слова той же части речи и с теми же грамматическими характеристиками.\n\n'
      'Если тебе надоело, просто оставь поле пустым\n')
while selector == 'true':
    text = input('Введите фразу:')
    if text == '':
        print('\nДо скорого!')
        selector = 'false'
    else:
        text_creator(text)
