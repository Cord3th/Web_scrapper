from bs4 import BeautifulSoup
import requests
import pymorphy2
import csv

def hyperlinks(url):
    morph = pymorphy2.MorphAnalyzer()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    out = soup.find('div', class_ = 'mw-parser-output')
    for text in out.find_all('p'):
        for link in text.find_all('a'):
            if not link.get('href') == None and not link.get('href')[0] == '#':
                words = []
                prev = link.previous_sibling
                prev_str = str(prev)
                nextsib = link.next_sibling
                next_str = str(nextsib)
                if next_str == "&nbsp;":
                    next_str = ' '
                while prev == None or prev_str[0] == '<' or prev_str == ' ' or prev_str == '\n':
                    if prev == None:
                        prev_str = None
                        break
                    elif prev_str[0] == '<':
                        prev_str = prev.text
                        break
                    else:
                        prev = prev.previous_sibling
                        prev_str = str(prev)
                while nextsib == None or next_str == ' '  or next_str[0] == '<' or next_str == '\n':
                    if nextsib == None:
                        next_str = None
                        break
                    elif next_str[0] == '<':
                        next_str = nextsib.text
                        break
                    else:
                        nextsib = nextsib.next_sibling
                        next_str = str(nextsib)
                words.append(link.get('title'))
                if not prev_str == None:
                    if len(prev_str.split()) == 1:
                        words.append(morph.parse(prev_str)[0].normal_form)
                    else:
                        words.append(morph.parse(prev_str.split()[-2])[0].normal_form)
                        words.append(morph.parse(prev_str.split()[-1])[0].normal_form)
                for word in link.text.split():
                    words.append(morph.parse(word)[0].normal_form)
                if not next_str == None:
                    if len(next_str.split()) == 1:
                        words.append(morph.parse(next_str)[0].normal_form)
                    else:
                        words.append(morph.parse(next_str.split()[0])[0].normal_form)
                        words.append(morph.parse(next_str.split()[1])[0].normal_form)
                with open('result.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow((words))
                    
URL = 'https://ru.wikipedia.org/wiki/%D0%A3%D1%81%D0%B0%D0%B4%D1%8C%D0%B1%D0%B0_%D0%97%D0%BE%D1%82%D0%BE%D0%B2%D0%B0'
hyperlinks(URL)
