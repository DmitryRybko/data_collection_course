from pprint import pprint
import requests
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lxml import html

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/98.0.4758.102 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

top_news_urls = list(set(dom.xpath("//div[@class='block']//@href")))  # используем set для дедубликации

news_list = []

for news_url in top_news_urls:

    news_item_dict = {}
    news_url_item = news_url
    print(news_url)
    response = requests.get(news_url, headers=headers)
    dom = html.fromstring(response.text)

    news_item_data = dom.xpath("//div[contains(@class, 'article')]")

    news_date = news_item_data[0].xpath(".//span/@datetime")[0]
    news_source = news_item_data[0].xpath(".//span[contains(@class, 'link__text')]/text()")[0]
    news_title = news_item_data[2].xpath(".//p/text()")[0].replace("\xa0", " ")

    news_item_dict["url"] = news_url
    news_item_dict["date"] = news_date
    news_item_dict["source"] = news_source
    news_item_dict["title"] = news_title

    news_list.append(news_item_dict)

pprint(news_list)

client = MongoClient('localhost', 27017)
data_base = client["news_database"]

news_collection = data_base.news_collection

try:
    for news_item in news_list:
        news_collection.insert_one(news_item)

except DuplicateKeyError:
    print(f'Duplicate key error, item with id {news_item.get("_id")} skipped')

print("данные добавлены в базу данных")
print(f'всего позиций: {len(news_list)}')

"""
OUTPUT:

[{'date': '2022-02-28T10:32:17+03:00',
  'source': 'ТАСС',
  'title': '. Российские военные завоевали господство в воздухе над всей '
           'Украиной, сообщил в понедельник на брифинге официальный '
           'представитель Минобороны РФ Игорь Конашенков.',
  'url': 'https://news.mail.ru/incident/50239411/'},
 {'date': '2022-02-28T15:21:48+03:00',
  'source': 'Lenta.Ru',
  'title': 'Власти Европейского союза (ЕС) заставили российских дипломатов '
           'получать визы. Об этом сообщил замглавы МИД России Евгений Иванов, '
           'передает РИА Новости.',
  'url': 'https://news.mail.ru/politics/50245128/'},
 {'date': '2022-02-28T15:56:06+03:00',
  'source': 'Спорт РИА Новости',
  'title': 'Московский «Спартак» будет исключен из текущего розыгрыша Лиги '
           'Европы по решению Союза европейских футбольных ассоциаций (УЕФА) '
           'из-за ситуации на Украине, сообщает Bild, а также немецкая версия '
           'Sky.',
  'url': 'https://sportmail.ru/news/football-eurocups/50245859/'},
 {'date': '2022-02-28T13:50:09+03:00',
  'source': 'Life.ru',
  'title': 'Немецкий футбольный клуб «Шальке-04» досрочно расторг спонсорский '
           'контракт с компанией «Газпром» на фоне событий на Украине, '
           'сообщает пресс-служба клуба.',
  'url': 'https://sportmail.ru/news/football-foreign/50243847/'},
 {'date': '2022-02-28T15:39:48+03:00',
  'source': '© РИА Новости',
  'title': 'РВСН, Северный и Тихоокеанский флоты, а также Дальняя авиация '
           'начали нести боевое дежурство усиленным составом, заявил министр '
           'обороны Сергей Шойгу.',
  'url': 'https://news.mail.ru/politics/50245092/'},
 {'date': '2022-02-28T15:53:45+03:00',
  'source': '© РИА Новости',
  'title': ' Президент России Владимир Путин предложил на совещании по '
           'экономике обсудить санкции, которые вводит так называемая «империя '
           'лжи» — западное сообщество.',
  'url': 'https://news.mail.ru/politics/50245820/'},
 {'date': '2022-02-28T16:12:35+03:00',
  'source': '© РИА Новости',
  'title': 'Россия в качестве ответной меры на запрет европейских государств '
           'на выполнение полетов российских самолетов ограничила выполнение '
           'полетов авиакомпаниям 36 государств, сообщает Росавиация.',
  'url': 'https://news.mail.ru/politics/50246683/'},
 {'date': '2022-02-28T11:40:13+03:00',
  'source': 'Известия',
  'title': 'Индексация пенсий, штрафы за отсутствие ТО и опасный мусор.',
  'url': 'https://news.mail.ru/society/50235667/'},
 {'date': '2022-02-28T16:03:31+03:00',
  'source': 'РБК',
  'title': 'Минобороны опровергает участие срочников в военной операции на '
           'Украине.',
  'url': 'https://news.mail.ru/politics/50246534/'},
 {'date': '2022-02-28T15:46:58+03:00',
  'source': '© РИА Новости',
  'title': ' В Белоруссии начались переговоры между делегациями России и '
           'Украины, сообщил корреспондент РИА Новости.',
  'url': 'https://news.mail.ru/politics/50244148/'},
 {'date': '2022-02-28T12:15:39+03:00',
  'source': 'ТАСС',
  'title': ' Власти Украины обращаются к Евросоюзу с просьбой о немедленном '
           'присоединении по новой специальной процедуре. Об этом в '
           'понедельник заявил президент Украины Владимир Зеленский.',
  'url': 'https://news.mail.ru/politics/50241339/'}]
"""
