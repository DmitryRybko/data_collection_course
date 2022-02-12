"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл.
"""

# Используем https://kinopoiskapiunofficial.tech/

import requests
from pprint import pprint
from prettytable import PrettyTable
import json
from datetime import date

API_KEY = "311d8a37-d72f-4ee9-97c7-73bef6889c67"

querystring = {"type": "TOP_AWAIT_FILMS",
               "page": 1}

headers = {
    'X-API-KEY': API_KEY
    }

response = requests.request("GET", "https://kinopoiskapiunofficial.tech/api/v2.2/films/top",
                            headers=headers, params=querystring)

movie_list = response.json()

with open('task_2_movie_list.json', 'w', encoding='utf-8') as f:
    json.dump(movie_list, f, ensure_ascii=False, indent=4)

repo_table = PrettyTable(["Name Rus", "Name Eng", "year"])
repo_table.align = "l"

for movie in movie_list["films"]:
    repo_table.add_row([movie["nameRu"], movie["nameEn"], movie["year"]])

print(f"Список самых ожидаемых фильмов на {date.today()} по данным Кинопоиска:")
print(repo_table)
