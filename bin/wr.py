#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def commit(last=False):
    while len(temp) != 4:
        temp.append('')
    data.append(temp)
    if not last:
        data.append(['', '', '', ''])
        data.append(['/////////////////', '/////////////////', '//////////////////', '////////////////'])
        data.append(['', '', '', ''])


if (len(sys.argv) > 2):
    print("Only one argment is accepted, try to use '...'")
elif len(sys.argv) < 2:
    parm = input('Waiting for input...\nSearch: ')
else:
    parm = sys.argv[1]

url = "https://www.wordreference.com/enit/" + parm

try:
    html = requests.get(url).content
    parsed_html = BeautifulSoup(html, features="html5lib")
    table = parsed_html.body.find('table', attrs={'class': 'WRD'})
    data = []
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    FrLang = rows[1].contents[0].text
    ToLang = rows[1].contents[2].text
    rows = rows[2:]

    count = 0
    temp = []
    for i in range(len(rows)):
        cols = rows[i].find_all('td')
        if rows[i].get('id') != None:  # E una nuova traduzione
            tmpString = ""
            tmpString = cols[0].find('strong').text  # Parametro cercato
            try:
                span = " " + cols[1].find('span').text.strip() + " "  # Casi d'tilizzo in ToLang
                cols[1].find('span').clear()
            except:
                span = ''

            tmpString += " " + cols[1].text.strip()  # Casi d'utilizzo in FrLang
            temp.append(tmpString)

            cols[2].find('em').clear()
            temp.append(span + cols[2].text.strip())  # Traduzione + casi d'utilizzo
            # data.append(temp)
        else:
            if cols[1].get('class') == ['FrEx']:
                try:
                    temp[2] += '\n' + cols[1].text.strip()
                except:
                    temp.append(cols[1].text.strip())
            elif cols[1].get('class') == ['ToEx']:
                try:
                    temp[3] += '\n' + cols[1].text.strip()
                except:
                    temp.append(cols[1].text.strip())
            elif cols[1].get('class') == ['To2']:
                try:
                    span = cols[1].find('span').text.strip() + " "  # Casi d'utilizzo in ToLang
                    cols[1].find('span').clear()
                except:
                    span = ''
                temp[0] += '\n--------------------\n' + cols[1].text.strip()  # Casi d'utilizzo in FrLang
                cols[2].find('em').clear()
                temp[1] += '\n--------------------\n' + (
                        span + cols[2].text.strip())  # Traduzione + casi d'utilizzo
        if i < len(rows) - 1 and rows[i + 1].get('id') != None:
            commit()
            temp = []
        elif i == len(rows) - 1:
            commit(last=True)
        # cols = [ele.text.strip() for ele in cols]'',
    for row in data:
        if len(row) != 4:
            print(row)
    t = PrettyTable([FrLang, ToLang, "FrEx", "ToEx"])
    t.add_rows(data)
    t._max_width = {FrLang: 20, ToLang: 20, "FrEx": 40, "ToEx": 40}
    print(t)
except:
    import webbrowser

    webbrowser.get('firefox').open(url)
    exit(-1)
