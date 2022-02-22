"""2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты)."""
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
data_base = client["positions_database"]
positions_collection = data_base.positions_collection

salary_level = 100000
print()
print(f"выборка из базы данных вакансий с зарплатой выше {salary_level}:")

salary_filter = {'$or': [
    {'min_compensation': {'$gt': 100000}},
    {'max_compensation': {'$gt': 100000}}
]
}

search_result = client['positions_database']['positions_collection'].find(filter=salary_filter)
pprint(list(search_result))
