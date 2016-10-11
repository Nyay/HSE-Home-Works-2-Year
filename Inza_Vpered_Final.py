import urllib.request as ur
import re
import html.parser
import os

def cleaning(text):
    regBr = re.compile('<br />',flags = re.U|re.DOTALL)
    regTag = re.compile('<.*?>',flags = re.U|re.DOTALL)
    regScript = re.compile('<script>.*?</script>',flags = re.U|re.DOTALL) 
    regComment = re.compile('<!--.*?-->', flags = re.U|re.DOTALL)
    regAd = re.compile('http://.+?/', flags = re.U|re.DOTALL) 
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regBr.sub("\n", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t=regAd.sub("", clean_t)
    clean_t=html.parser.HTMLParser().unescape(clean_t)
    return clean_t
    
def get_text(num):
    global url
    try:
        url = 'http://inza-vpered.ru/article/' + str(num) + '/'
        page = ur.urlopen (url)
        text = page.read().decode ('UTF-8')
    except:
        text = ''
    return text
    
def plain_cut(text):
    try:
        result = re.findall ('<div class="b-block-text__text">\n(.+?)\n', text)
        plain_text = ''.join (result)
    except:
        plain_text = ' No Text Found '
    return plain_text
    
def date_cut(text):
    try:
        result = re.search('<span class="date">(\d{2}\.\d{2}\.\d{4})</span>', text, flags=re.DOTALL)
        data = result.group(1)
        data = ''.join(data)
    except:
        data = ' No Date Found '
    return data
    
def author_cut(text):
    try:
        result = re.search('<span class="b-object__detail__author__name">(.+?)</span>', text, flags=re.DOTALL)
        author = result.group(1)
        author = ''.join (author)
    except:
        author = ' NoName '
    return author
    
def title_cut(text):
    try:
        result = re.search('<meta name="title" content="(.+?)"/>', text, flags=re.DOTALL)
        title = result.group(1)
        title = ''.join (title)
    except:
        title = ' No Title Found '
    return title
    
def category_cut(text):
    try:
        result = re.findall('<a href="/article/\?category=.+?">(.+?)</a>', text)
        category =  ' ' .join(result)
        category = ''.join (category)
    except:
        title = ' No Category Found '
    return category

def row_create():
    row = '%s\t%s\t\t\t%s\t%s\tПублицистика\t\t\t%s\t\tНейтральный\tн-возраст\tн-уровень\tРайонная\t%s\t"Вперед"\t\t%s\tГазета\tРоссия\tУльяновская область\tru'
    string = (row % (path_row, author, title, date, category, url, year))
    file = open('C:\\Users\\sony\\Desktop\\magazine\\metadata.csv', 'a', encoding='UTF-8')
    file.write(string + "\n")
    file.close()

def file_create():
    if not os.path.exists('C:\\Users\\sony\\Desktop\\magazine\\plain\\' + year + '\\' + month):
        os.makedirs('C:\\Users\\sony\\Desktop\\magazine\\plain\\' + year + '\\' + month)
    file = open ('C:\\Users\\sony\\Desktop\\magazine\\plain\\' + year + '\\' + month + '\\' + num + '.txt', 'w', encoding='UTF-8')
    file.write ('@au ' + author + '\n' + '@ti ' + title + '\n' + '@da ' + date + '\n' + '@topic ' + category + '\n' + '@url ' + url + '\n' + '\n' + statment )
    file.close()

def suicide_file():
    file = open ('C:\\Users\\sony\\Desktop\\magazine\\KILLME.txt', 'w', encoding='UTF-8')
    file.write (statment)
    file.close()

def mystem_xml():
    if not os.path.exists ('C:\\Users\\sony\\Desktop\\magazine\\mystem-xml\\' + year + '\\' + month):
        os.makedirs ('C:\\Users\\sony\\Desktop\\magazine\\mystem-xml\\' + year + '\\' + month)
    os.system ('C:\\mystem.exe -cdi ' + path + ' C:\\Users\\sony\\Desktop\\magazine\\mystem-xml\\' +  year + '\\' + month + '\\' + num + '.xml')
    
def mystem_txt():
     if not os.path.exists ('C:\\Users\\sony\\Desktop\\magazine\\mystem-plain\\' + year + '\\' + month):
        os.makedirs ('C:\\Users\\sony\\Desktop\\magazine\\mystem-plain\\' + year + '\\' + month)
     os.system ('C:\\mystem.exe -cdi ' + path + ' C:\\Users\\sony\\Desktop\\magazine\\mystem-plain\\' +  year + '\\' + month + '\\' + num + '.txt')
    
for num in range(74036,111912): # Подставить любой свой range для поиска страниц (их id)
    num = str(num)
    text = get_text(num)
    if text != '':
        print ('Found something here: ' + url)
        statment = cleaning(plain_cut(text))
        if statment!= '':
            date = cleaning(date_cut(text))
            year = ''.join(re.findall('\d{4}', date))
            month = ''.join(re.findall('\d{2}\.(\d{2})\.\d{4}', date))
            author = cleaning(author_cut(text))
            category = cleaning(category_cut(text))
            title = cleaning(title_cut(text))
            path_row = ('C:\\Users\\sony\\Desktop\\magazine\\plain\\' + year + '\\' + month + '\\' + num + '.txt')
            path = ('C:\\Users\\sony\\Desktop\\magazine\\KILLME.txt') 
            file_create()
            row_create()
            suicide_file()
            mystem_xml()
            mystem_txt()
            os.remove (path)
    else:
        print ('Nothing to find on page: ' + num)
