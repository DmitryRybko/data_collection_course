"""
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность)
с сайтов HH(обязательно) и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:

    Наименование вакансии.
    Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
    Ссылку на саму вакансию.
    Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pprint import pprint

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
headers = {"User-Agent": user_agent}
vacancy_source = "hh.ru"
base_url = "https://hh.ru/search/vacancy"
search_text = "Python"
page_number = 0
items_on_page = 20

querystring = {"area": 1,
               "search_field": "description",
               "experience": "between1And3",
               "text": search_text,
               "clusters": "true",
               "ored_clusters": "true",
               "enable_snippets": "true",
               "from": "suggest_post",
               "industry": 43,  # финансовый сектор
               "professional_role": 96,  # Программист, разработчик
               "page": page_number,
               "items_on_page": items_on_page,
               }

positions_list = []


response = requests.request("GET", base_url, headers=headers, params=querystring)

if response.ok:
    dom = BeautifulSoup(response.text, "html.parser")
    expected_items = int(dom.find("h1", {"class": "bloko-header-section-3"}).getText().split(" ", 1)[0])
    expected_last_page = expected_items//items_on_page+1
    print(f'страниц с данными: {expected_last_page}')

    for x in range(expected_last_page+1):
        response = requests.request("GET", base_url, headers=headers, params=querystring)
        querystring["page"] = x
        dom = BeautifulSoup(response.text, "html.parser")
        positions = dom.find_all("div", {"class": "vacancy-serp-item"})

        for position in positions:
            position_data = {}

            position_name_data = position.find('a', {"data-qa": "vacancy-serp__vacancy-title"})
            position_name = position_name_data.getText()
            position_link = position_name_data["href"].split("?", 1)[0]

            position_compensation = position.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"})
            if position_compensation is None:
                min_compensation = None
                max_compensation = None
                currency = None

            else:
                position_compensation = position_compensation.getText()
                currency = position_compensation[position_compensation.rindex(' ') + 1:]
                if "от" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                    max_compensation = None
                elif "до" in position_compensation:
                    min_compensation = None
                    max_compensation = int(''.join(filter(str.isdigit, position_compensation)))
                elif "–" in position_compensation:
                    min_compensation = int(''.join(filter(str.isdigit, position_compensation.split("–", 1)[0])))
                    max_compensation = int(''.join(filter(str.isdigit, position_compensation.split("–", 1)[1])))


            position_data["position_source"] = vacancy_source
            position_data["position_name"] = position_name
            position_data["position_link"] = position_link
            position_data["min_compensation"] = min_compensation
            position_data["max_compensation"] = max_compensation
            position_data["currency"] = currency

            positions_list.append(position_data)


print(f'всего позиций: {len(positions_list)}')
pprint(positions_list)

"""
выводит в терминале:

страниц с данными:5
всего позиций:115
[{'currency': 'Not Indicated',
  'max_compensation': 'Not Indicated',
  'min_compensation': 'Not Indicated',
  'position_link': 'https://hh.ru/vacancy/51629618',
  'position_name': 'Python разработчик',
  'position_source': 'hh.ru'},
 {'currency': 'Not Indicated',
  'max_compensation': 'Not Indicated',
  'min_compensation': 'Not Indicated',
  'position_link': 'https://hh.ru/vacancy/51882397',
  'position_name': 'Scala разработчик',
  'position_source': 'hh.ru'},
 {'currency': 'руб.',
  'max_compensation': 380000,
  'min_compensation': 'Not Indicated',
  'position_link': 'https://hh.ru/vacancy/49590587',
  'position_name': 'Python разработчик',
  'position_source': 'hh.ru'},
 {'currency': 'руб.',
  'max_compensation': 'Not Indicated',
  'min_compensation': 150000,
  'position_link': 'https://hh.ru/vacancy/52217658',
  'position_name': 'Python разработчик / программист Python (Python Developer)',
  'position_source': 'hh.ru'},
 {'currency': 'руб.',
  'max_compensation': 280000,
  'min_compensation': 120000,
  'position_link': 'https://hh.ru/vacancy/52296666',
  'position_name': 'Python Developer',
  'position_source': 'hh.ru'},
  ....
  и т.д.
"""
