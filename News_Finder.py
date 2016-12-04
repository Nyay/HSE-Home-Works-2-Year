import re
import os
import urllib.request as ur

def get_html_ramb():
    #global url
    try:
        url = 'https://news.rambler.ru/asia/35479636-mid-rossii-u-afganistana-net-alternativy-russkomu-oruzhiyu/items/'
        page = ur.urlopen (url)
        html_code = page.read().decode ('UTF-8')
        #print(text)
    except:
        html_code = ''
    return html_code

def get_links(html_code):
    try:
        result = re.findall ('<a\nhref="(.+?)"\nclass="j-metrics__clicks-out-source-subject article-sources__subject"', html_code)
        link_list = result
        #link_list = '\n'.join(result)
    except:
        link_list = ' No Links Found '
    #print(link_list)
    return link_list

def get_text(link_list):
    block1 = []
    block2 = []
    i = 0
    get_links(get_html_ramb())
    for i in range(len(link_list)):
        try:
            arr = link_list[i]
            url = arr
            page = ur.urlopen(url)
            html_code = page.read().decode('UTF-8')
            result = re.findall('<p>(.+?)</p>', html_code)
            artical = ''.join(result)
            result = re.sub('<.+?>','',artical)
            result = re.sub('&nbsp;',' ',result)
            result = re.sub('&mdash', '-', result)
            result = re.sub('&ndash', '-', result)
            result = re.sub('\xa0', ' ', result)
            result = re.sub('"', '', result)
            result = re.sub('&laquo;', '', result)
            result = re.sub('&raquo;', '', result)
            result = re.sub('«', ' ', result)
            artical2 = ''.join(result)
        except:
            artical2 = 'Problemes'
        block1.append(result)
    for element in block1:
        word = element.split(' ')
        word = set(word)
        block2.append(word)
    return block2

def setter(block2):
    set1 = block2[0]
    set2 = block2[1]
    set3 = block2[2]
    set4 = block2[3]
    set5 = block2[4]
    set6 = block2[6]
    set11 = set1
    set12 = set2
    set13 = set3
    set14 = set4
    set15 = set5
    set16 = set6
    final2 = set2 & set1 & set3 & set4 & set5 & set6
    set16 -= set2 | set3 | set4 | set5 | set1
    set15 -= set2 | set3 | set4 | set6 | set1
    set14 -= set2 | set3 | set6 | set5 | set1
    set13 -= set2 | set6 | set4 | set5 | set1
    set12 -= set6 | set3 | set4 | set5 | set1
    set11 -= set2 | set3 | set4 | set5 | set6
    final2 = ' , '.join(final2)
    set16 = ' , '.join(set16)
    set15 = ' , '.join(set15)
    set14 = ' , '.join(set14)
    set13 = ' , '.join(set13)
    set12 = ' , '.join(set12)
    set11 = ' , '.join(set11)
    f = open('final.txt','w',encoding='UTF-8')
    f.write('Общие слова для всех статей:\n\n' + final2 + '\n\nУникальные слова по 1 статье\n\n' + set11 + '\n\nУникальные слова по 2 статье\n\n' + set12 + '\n\nУникальные слова по 3 статье\n\n' + set13 + '\n\nУникальные слова по 4 статье\n\n' + set14 + '\n\nУникальные слова по 5 статье\n\n' + set15 + '\n\nУникальные слова по 6 статье\n\n' + set16)
    f.close()
setter(get_text(get_links(get_html_ramb())))