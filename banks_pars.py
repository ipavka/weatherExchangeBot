import requests
from bs4 import BeautifulSoup as BS
import re

URL = 'https://www.genbank.ru/history-of-exchange-rates'
URL_RNKB = 'https://old.rncb.ru/fizicheskkim-litsam/valyutnye-operatsii/'
URL_WIND = 'http://wttr.in/Севастополь?format=%l:+%w'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) '
                         'Gecko/20100101 Firefox/82.0', 'accept': '*/*'}


def get_html(url):
    return requests.get(url, headers=HEADERS)


def genbank():
    html = get_html(URL)
    soup = BS(html.content, 'html.parser')

    cur_excha = soup.find_all('span', class_='kurs_left')
    resul_list = []
    for el in cur_excha:
        resul_list.append(el.text)
    return f'USD {chr(36)} {resul_list[0]} | {resul_list[1]}\nEUR {chr(8364)} ' \
           f'{resul_list[2]} | {resul_list[3]}\nGBP' \
           f' {chr(163)} ' \
           f'{resul_list[4]} | {resul_list[5]}'


def rnkb():
    html = get_html(URL_RNKB)

    soup = BS(html.content, 'html.parser')
    cur_excha = soup.find('table', class_='cours').get_text()

    #  Дата актуальности курса
    info_date = soup.find('h2').get_text()
    ready_nums = re.findall(r'\d+', info_date)

    result_list = cur_excha.split()
    usd_1 = result_list[5]
    usd_2 = result_list[6]
    eur_1 = result_list[9]
    eur_2 = result_list[10]

    return f"Курс на {'/'.join(ready_nums)}\n"\
           f"USD {chr(36)} {usd_1} | {usd_2}\n" \
           f"EUR {chr(8364)} {eur_1} | {eur_2}"


if __name__ == '__main__':
    pass
