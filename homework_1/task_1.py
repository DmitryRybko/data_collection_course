"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""

import requests
from pprint import pprint
from prettytable import PrettyTable
import json

user = "DmitryRybko"
response = requests.get(f"https://api.github.com/users/{user}/repos")
repo_list = response.json()

with open('task_1_repo_list_data.json', 'w', encoding='utf-8') as f:
    json.dump(repo_list, f, ensure_ascii=False, indent=4)


repo_table = PrettyTable(["Name", "url"])
repo_table.align = "l"

for repo in repo_list:
    repo_table.add_row([repo["name"], repo["url"]])

print(f"Список GitHub репозиториев пользователя {user}:")
print(repo_table)
