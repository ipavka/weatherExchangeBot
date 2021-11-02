import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta
import time
import re
from config import wind_dir

URL_SINOP = 'https://sinoptik.ua/погода-севастополь'
URL_SEV_INFO = 'https://forum.sevastopol.info/'
URL_SEV_METEO = 'http://sevmeteo.info/'
URL_WTR = 'http://wttr.in/Севастополь?format=Ощущается+%f\n'
URL_WTR_WIND = 'http://wttr.in/Севастополь?format=%l:+%w'  # ветер
URL_WTR_OTHER = 'http://wttr.in/Севастополь?format=Рассвет %S+\nСумерки %d'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) '
                         'Gecko/20100101 Firefox/82.0', 'accept': '*/*'}


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return requests.get(url, headers=HEADERS)
    else:
        return False


def sinop():
    """Погода на сегодня"""
    html = get_html(URL_SINOP)
    soup = BS(html.content, 'html.parser')

    temp_today = soup.find('div', class_='main loaded').get_text().strip().split('    ')
    descrip = soup.find('div', class_='description').get_text()

    return f'{temp_today[0].title()}\n' \
           f'Температура воздуха\n{temp_today[1].title()}\n' \
           f'{descrip.strip()}'


def sinop_tomor():
    """ Получаем завтра исходя из актуальной даты """
    # берем завтрашний день
    named_tuple = time.localtime()
    a = time.strftime("%Y-%m-%d", named_tuple)
    dt = datetime.strptime(a, '%Y-%m-%d')
    result = dt + timedelta(days=1)
    dey_tomor = result.strftime('%Y-%m-%d')

    html = get_html(URL_SINOP)
    soup = BS(html.content, 'html.parser')
    sp = BS(get_html(f'{URL_SINOP}/{dey_tomor}').content, 'html.parser')  # ссылка на завтра
    descrip = sp.select('.description')[0].text
    temp_tomor = soup.select('#bd2')[0].text.replace('    ', ' ')
    return f'{temp_tomor}\n' \
           f' {descrip.strip()}'


def sev_meteo():
    """ Температура с sevmeteo.info """
    if get_html(URL_SEV_METEO):
        html = get_html(URL_SEV_METEO)
        soup = BS(html.content, 'lxml')
        is_work = soup.find('head')
        if is_work:
            temp_now = soup.find('h3').text
            all_data = soup.find_all('h3')[-1].text
            return temp_now, all_data, 'meteoInfo'
        else:
            return None, 'С сайтом "sevmeteo.info" что-то не так... о_О', 'sevmeteo.info'


def temp_sevas():
    """ Сейчас """
    #  Температура сейчас с Sevinfo
    if get_html(URL_SEV_METEO):
        html = get_html(URL_SEV_INFO)
        soup = BS(html.content, 'html.parser')
        temp_now = soup.find('strong')

        #  Ощущается как с 'wttr.in'
        resp_t = requests.get(URL_WTR)

        #  сила и направление ветра
        resp_w = requests.get(URL_WTR_WIND)
        step_1 = resp_w.text.split()[-1]
        step_2 = re.findall(r'\d+', step_1)
        step_3 = round(int(*step_2) * 0.28, 1)
        step_4 = step_1[-4:].replace('km/h', 'm/s')
        step_5 = resp_w.text.split()[1][0:1]

        #  рассвет и сумерки
        dawn_sunset = requests.get(URL_WTR_OTHER)

        # история температур
        html_2 = get_html(URL_SINOP)
        soup_2 = BS(html_2.content, 'html.parser')
        hist_temp = soup_2.find('p', class_='infoHistory').get_text()
        hist_temp_2 = soup_2.find('p', class_='infoHistoryval').get_text().strip()

        return f'в Севастополе {temp_now.text}°C\n' \
               f'{resp_t.text}\n' \
               f'ветер {wind_dir(ord(step_5))}{step_3}{step_4}\n' \
               f'{dawn_sunset.text}\n' \
               f'{hist_temp.title()}\n' \
               f'{hist_temp_2.title()}'
    else:
        return f'{sev_meteo()[0]}\n' \
               f'{sev_meteo()[1]}\n' \
               f'{sev_meteo()[2]}'


if __name__ == '__main__':
    pass
