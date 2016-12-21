import os
import re

def del_same():
    f_enter = open('text.txt','r', encoding='UTF-8')
    f_out = open('mystem_base.txt','w', encoding='UTF-8')
    text = f_enter.read()
    text = text.split()
    text = set(text)
    text = ' '.join(text)
    text_free = text.strip(',.!?-_')
    low_text = text_free.lower()
    f_out.write(low_text)
    f_enter.close()
    f_out.close()

def mystem_create():
    os.system('/Users/macbook/Downloads/mystem -di ' + '/Users/macbook/Desktop/HSE-Home-Works-2-Year/sql_hw/mystem_base.txt ' + '/Users/macbook/Desktop/HSE-Home-Works-2-Year/sql_hw/text_ms.txt ')

def get_words():
    full = []
    mystem_create()
    file_enter = open('text_ms.txt','r', encoding='UTF-8')
    file_exit = open('code.txt','w', encoding='UTF-8')
    f = file_enter.read()
    result = re.findall('(.+?)\{(.+?)=.+?\}', f, flags=re.DOTALL)
    for element in result:
        line = 'insert into DBT3 (Форма, Лемма) values ("' + element[0] +'","' + element[1] + '");'
        full.append(line)
    final = '\n'.join(full)
    file_exit.write(final)
    file_enter.close()
    file_exit.close()



mystem_create()
del_same()
get_words()