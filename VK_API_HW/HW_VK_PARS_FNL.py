import requests
import re
import collections
import matplotlib.pyplot as plt


def count(obj):
    block = obj.split(' ')
    try:
        block.remove('')
        num = len(block)
    except ValueError:
        num = len(block)
    return num


def cleaner(obj):
    result = re.sub('<br>', ' ', obj)
    result = re.sub('https\:\/\/(vk\.com)\/(video|doc|audio|photo)(\-)?[0-9]*?\_[0-9]*', '', result)
    result = re.sub('- ', ' ', result)
    result = re.sub(' / ', ' ', result)
    result = re.sub('\.', '', result)
    result = re.sub(',', '', result)
    result = re.sub('\[id[0-9]*?\|', '', result)
    result = re.sub('\[club[0-9]*?\|', '', result)
    result = re.sub('\] ', ' ', result)
    result = re.sub('   ', ' ', result)
    result = re.sub('  ', ' ', result)
    return result


def graf_plot(dictp):
    block_1 = []
    block_2 = []
    for el in dictp:
        block_1.append(el)
    block_1 = sorted(block_1)
    for el in block_1:
        block_2.append(dictp[el])
    print(block_1, block_2)
    plt.plot(block_1, block_2)
    plt.show()
    plt.close()


def graf(dictio, titles, ylabels, xtick):
    some_nums = [dictio[something] for something in dictio]
    some_labs = [something for something in dictio]
    plt.bar(range(len(some_labs)), some_nums)
    plt.title(str(titles))
    plt.ylabel(str(ylabels))
    plt.xlabel(str(xtick))
    plt.xticks(range(len(some_labs)), some_labs, rotation=90)
    plt.legend()
    plt.rcParams.update({'font.size': 1})
    plt.show()
    plt.close()


def collector():
    item = []
    num_hi = []
    num_low = []
    years = {}
    dicti_2 = {}
    towns = {}
    file_to_write = open('post_text.txt', 'w', encoding='UTF-8')
    file_to_write.write('\tНазвание группы: Kyoto Animation\n\tСсылка на группу: https://vk.com/kyoani\n')
    i = [0, 100]
    link = 'https://api.vk.com/method/wall.get'
    for number in i:
        parameters = {'version': '5.62',
                      'owner_id': '-256132',
                      'count': 100,
                      'offset': number}
        response = requests.get(link, params=parameters)
        result = response.json()['response']
        for x in range(1, 101):
            if result[x]['text'] != '':
                num_1 = count(cleaner(result[x]['text']))
                one_id = result[x]['id']
                file_to_write.write('\n\n\tID поста: ' + str(one_id) + '\n\n\tТестк поста: \n\n' + cleaner(result[x]['text']) + '\n\n\tКомментарии:\n')
                link2 = 'https://api.vk.com/method/wall.getComments'
                parameters_comments = {'version': '5.62',
                                       'owner_id': '-256132',
                                       'post_id': one_id,
                                       'count': 100}
                response = requests.get(link2, params=parameters_comments)
                result_2 = response.json()['response']
                num_2 = []
                for stuff in result_2:
                    try:
                        if stuff['text'] != '':
                            file_to_write.write('\n' + cleaner(stuff['text']) + '\n')
                            ix = int(count(cleaner(stuff['text'])))
                            num_2.append(ix)
                    except BaseException:
                        continue
                    user_id = stuff['from_id']
                    link_user = 'https://api.vk.com/method/users.get'
                    parameters_user = {
                        'user_ids': user_id,
                        'fields': 'home_town,bdate'
                    }
                    response_1 = requests.get(link_user, params=parameters_user)
                    result_3 = response_1.json()['response']
                    for info in result_3:
                        try:
                            if info['home_town'] != '':
                                town = info['home_town']
                                if info['home_town'] in towns:
                                    towns[str(town)].append(ix)
                                else:
                                    towns[str(town)] = []
                                    towns[str(town)].append(ix)
                        except KeyError:
                            continue
                        try:
                            if info['bdate'] != '':
                                date = info['bdate']
                                pray = re.search('([0-9][0-9][0-9][0-9])', date)
                                try:
                                    if pray.group(0) in years:
                                        years[pray.group(0)].append(ix)
                                    else:
                                        years[pray.group(0)] = []
                                        years[pray.group(0)].append(ix)
                                except AttributeError:
                                    continue
                        except KeyError:
                            continue
                dicti_2[num_1] = num_2
                num_hi.append(num_1)
                num_low.append(num_2)
    for el in years:
        years[el] = sum(years[el]) // len(years[el])
    graf(years, 'Соотношение возраст/кол-во слов в комментарии', 'Количество слов для каждого года', 'Год рождения пользователя')
    for el in dicti_2:
        try:
            dicti_2[el] = sum(dicti_2[el]) // len(dicti_2[el])
        except ZeroDivisionError:
            dicti_2[el] = 0
            continue
    graf_plot(dicti_2)
    for el in towns:
        towns[el] = sum(towns[el]) // len(towns[el])
    graf(towns, 'Среднее количество слов в комментарии для каждого города', 'Среднее количество слов', 'Город проживания позльзователя')
    return item

collector()
