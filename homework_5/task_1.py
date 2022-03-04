"""
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
в базу данных (от кого, дата отправки, тема письма, текст письма полный)
"""

import time

from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service


s = Service('./chromedriver')
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

browser = webdriver.Chrome(service=s, options=chrome_options)
browser.implicitly_wait(5)

browser.get('https://account.mail.ru/login')


login_elem = browser.find_element(By.NAME, 'username')
login_elem.send_keys('study.ai_172')
login_elem.send_keys(Keys.ENTER)

pass_elem = browser.find_element(By.NAME, 'password')
pass_elem.send_keys('NextPassword172#')
pass_elem.send_keys(Keys.ENTER)

# включаем вид с колонкой справа с содержанием письма

settings_elem = browser.find_element(By.CLASS_NAME, 'settings')
settings_elem.click()

try:
    settings_column_elem = browser.find_element(By.XPATH, '//div[@data-test-id="3pane-disabled"]')
    settings_column_elem.click()
except NoSuchElementException:  # если этого элемента нет, то опция уже включена
    pass

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()  # закрываем меню настроек

# получение количества писем

webdriver.ActionChains(browser).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
mail_qty_menu = browser.find_element(By.CLASS_NAME, "portal-menu-element_deselect")
mail_qty_item = int(mail_qty_menu.find_element(By.CLASS_NAME, 'button2__txt').text)

webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

# получение данных из писем

mail_list = []

for i in range(mail_qty_item):
    webdriver.ActionChains(browser).send_keys(Keys.ARROW_DOWN).perform()

    mail_item_dict = {}

    time.sleep(1)  # иначе страница не успевает обновиться

    try:  # особо тяжелые e-mails не должны блокировать работу

        mail_title = browser.find_element(By.CLASS_NAME, 'thread-subject').text
        mail_sender = browser.find_element(By.CLASS_NAME, 'letter-contact').text
        mail_date = browser.find_element(By.CLASS_NAME, 'letter__date').text
        mail_contents = browser.find_element(By.CLASS_NAME, 'letter-body__body-content').get_attribute('innerHTML')

        print(f"reading mail {i+1} of {mail_qty_item}: {mail_title}")

        mail_item_dict["mail_title"] = mail_title
        mail_item_dict["mail_sender"] = mail_sender
        mail_item_dict["mail_date"] = mail_date
        mail_item_dict["mail_contents"] = mail_contents

        mail_list.append(mail_item_dict)

    except NoSuchElementException:
        continue


client = MongoClient('localhost', 27017)
data_base = client["mail_database"]

mail_collection = data_base.mail_collection

try:
    for mail_item in mail_list:
        mail_collection.insert_one(mail_item)

except DuplicateKeyError:
    print(f'Duplicate key error, item with id {mail_item.get("_id")} skipped')

print("данные добавлены в базу данных")
print(f'всего позиций: {len(mail_list)}')


"""
OUTPUT:

reading mail 1 of 251: Вход с нового устройства в аккаунт
reading mail 2 of 251: Вход с нового устройства в аккаунт
reading mail 3 of 251: Fake Videos, Awards 2021, Gooey Numbers, Open UI, Web Components
reading mail 4 of 251: study.ai_172, посмотрите новости Salice Rose и Abhishek Bachchan и других пользователей в своей ленте
reading mail 5 of 251: Вход с нового устройства в аккаунт
reading mail 6 of 251: Коронавирус COVID-19: самое важное от 03.03.2022
reading mail 7 of 251: ГАРАНТ. Ежедневный мониторинг федерального законодательства от 03.03.2022
reading mail 8 of 251: В компании Discord грядут важные обновления политики
reading mail 9 of 251: ГАРАНТ. Ежедневный мониторинг московского законодательства от 03.03.2022
reading mail 10 of 251: Garant. Daily monitoring of the Federal legislation at 03.03.2022
reading mail 11 of 251: Топ новостей за 24 часа для вас
reading mail 12 of 251: Почему нужно получить IT-профессию
reading mail 13 of 251: Huemint, Gothic Architecture, Fruit Stickers, CSS Features, Color System
reading mail 14 of 251: Вход с нового устройства в аккаунт
reading mail 15 of 251: ГАРАНТ. Правовая картина дня от 02.03.2022
reading mail 16 of 251: ГАРАНТ. Главное для бухгалтера за день: информация Минфина и ФНС России, новости, правовые консультации от 02.03.2022
reading mail 17 of 251: ГАРАНТ. Ежедневный мониторинг федерального законодательства от 02.03.2022
reading mail 18 of 251: Garant. Daily monitoring of the Federal legislation at 02.03.2022
reading mail 19 of 251: Топ новостей за 24 часа для вас
reading mail 20 of 251: Cascading Server Sheets, Open Web Advocacy, Modern MacPaint, New MDN, Gmail Case Study
reading mail 21 of 251: ГАРАНТ. Новое в налоговом законодательстве от 01.03.2022
reading mail 22 of 251: ГАРАНТ. Новости органов государственной власти от 01.03.2022
reading mail 23 of 251: ГАРАНТ. Правовая картина дня от 01.03.2022
reading mail 24 of 251: ГАРАНТ. Главное для бухгалтера за день: информация Минфина и ФНС России, новости, правовые консультации от 01.03.2022
reading mail 25 of 251: Коронавирус COVID-19: самое важное от 01.03.2022
reading mail 26 of 251: ГАРАНТ. Ежедневный мониторинг федерального законодательства от 01.03.2022
reading mail 27 of 251: Garant. Daily monitoring of the Federal legislation at 01.03.2022
reading mail 28 of 251: Issue #494: Optimizing Full-Screen Images, Auto-Filling CSS Grid
reading mail 29 of 251: Топ новостей за 24 часа для вас
reading mail 30 of 251: Тест: Узнайте, кто вы в IT?
reading mail 31 of 251: Exclusive offer | Reveal it now
reading mail 32 of 251: La Patria, Indeed Redesign, Helvetica, CSS Logic, Russian Bots
reading mail 33 of 251: 🥞 Вкусные предложения к Масленице!
reading mail 34 of 251: ✏ HTML Tips & Tricks That You Will Love To Know and more...
reading mail 35 of 251: Топ новостей за 24 часа для вас
reading mail 36 of 251: Розыгрыш айпадов и последний день низких цен
reading mail 37 of 251: comiCSS, Figma Tricks, Headless Components, Unfamiliar Product, CSS Specificity
reading mail 38 of 251: Умер актер «Улиц разбитых фонарей» Борис Соколов
reading mail 39 of 251: What is Web 3.0 and will it change our lives?
reading mail 41 of 251: Топ новостей за 24 часа для вас
reading mail 42 of 251: instagram, brunogissoni и nylonmag сделали новые публикации
reading mail 43 of 251: ✏ How to Create Your Own Wordle and more...
reading mail 44 of 251: Топ новостей за 24 часа для вас
reading mail 45 of 251: 📈 Повышение цен на все программы с 1 марта
reading mail 46 of 251: У Вас новое личное сообщение [Geek Brains]
reading mail 47 of 251: ✏ Top 87 Web Design Tools For Developer and more...
reading mail 49 of 251: Mailchimp & BandLab screens
reading mail 50 of 251: 📈 Повышение цен на все программы с 1 марта
reading mail 51 of 251: Shaders and Gradients, SVG Masks, Insoles, Twitter’s Source Code, Comic Sans
reading mail 52 of 251: Кудрявцева объяснила, почему содержит мужа-хоккеиста: «Зарабатываю я, а он в поиске себя»
reading mail 53 of 251: ✏ How To Develop A Text Editor For The Web and more...
reading mail 54 of 251: Топ новостей за 24 часа для вас
reading mail 55 of 251: Скидки до -50% в эти выходные!
reading mail 56 of 251: Text Editor, Ememem, Landscape Photo, Coffee Makers, CSS Database Queries
reading mail 57 of 251: У дочери Константина Меладзе была найдена опухоль
reading mail 58 of 251: Отвечаем на вопросы сегодня в прямом эфире
reading mail 59 of 251: Issue #493: Cascade Layers, CSS Scroll Snap
reading mail 60 of 251: ✏ 6 Domain Name Trends for 2022 and more...
reading mail 61 of 251: Топ новостей за 24 часа для вас
reading mail 62 of 251: Readable Writing, Color & Design, Web Browsers, Design Matters, Middle-East Languages
reading mail 63 of 251: Вопросы, которые страшно задавать
reading mail 64 of 251: ✏ Myth-Busting NFTs: 7 Claims Fact-Checked and more...
reading mail 65 of 251: Топ новостей за 24 часа для вас
reading mail 66 of 251: В IT не хватает гуманитариев
reading mail 67 of 251: 🎁 Шикарный выбор подарков к 23 февраля!
reading mail 68 of 251: Chinese vs English UI, Markdown, Fake Agency, Black Creatives, Cascade Layers
reading mail 69 of 251: Топ новостей за 24 часа для вас
reading mail 70 of 251: 🔔 Срок действия ваших купонов истекает!
reading mail 71 of 251: Успейте попасть в новый поток программы Разработчик
reading mail 72 of 251: Inspiring Websites, Moment, Google Slides, Accessibility & Disabilities, Inspirational Websites
reading mail 73 of 251: Алину Загитову заподозрили в романе с хоккеистом. Что о нем известно
reading mail 74 of 251: ✏ The Most Popular Front-end Frameworks in 2022 and more...
reading mail 75 of 251: Топ новостей за 24 часа для вас
reading mail 76 of 251: ✏ Beginner's Guide to Responsive Images in HTML and more...
reading mail 77 of 251: У Вас новое личное сообщение [Geek Brains]
reading mail 78 of 251: Топ новостей за 24 часа для вас
reading mail 79 of 251: Вам отправлено (9) предложений о работе
reading mail 80 of 251: ✏ How to Create a GitHub Repository and more...
reading mail 81 of 251: Топ новостей за 24 часа для вас
reading mail 82 of 251: Indeed & TodayTix screens
reading mail 83 of 251: Krispy Kreme, Medium Accessibility, 99% Developers, Roboto Serif, Line Separator
reading mail 84 of 251: Что скрывает в себе «Разработчик»?
reading mail 85 of 251: «Это наезд»: Кабаева резко отреагировала на допинг-скандал вокруг 15-летней Валиевой
reading mail 87 of 251: Топ новостей за 24 часа для вас
reading mail 88 of 251: Вам открыт урок
reading mail 89 of 251: LEGO Letterpress, Optical Illusions, State of CSS, hue.tools, Swiping vs Tapping
reading mail 90 of 251: 💣 Скидки до -50% в эти Щедрые выходные!
reading mail 91 of 251: Вас приглашают наши студенты
reading mail 92 of 251: ✏ 6 Creative Ideas for CSS Link Hover Effects and more...
reading mail 94 of 251: Топ новостей за 24 часа для вас
reading mail 95 of 251: Linguistic Games, City Generator, Dynamic Color, State of JS, Functions
reading mail 96 of 251: Почему вы не любите свою работу
reading mail 97 of 251: Трусову и Щербакову экстренно проверили после положительного допинг-теста Валиевой. Нашли ли что-то у них
reading mail 98 of 251: ✏ 20 Best New Websites, February 2022 and more...
reading mail 99 of 251: Топ новостей за 24 часа для вас
reading mail 100 of 251: ❤️ Для влюбленных в скидки
reading mail 101 of 251: Rounded Corners, Bob Gill, State of Dataviz, Cascade Layers, Open Source Love
reading mail 102 of 251: ⌛ Остался 1 день спецпредложений! Успевайте!
reading mail 103 of 251: study.ai_172, посмотрите новости Ricky Harun и Emma Roberts и других пользователей в своей ленте
reading mail 104 of 251: ✏ 50 Cool Web And Mobile Project Ideas for 2022 and more...
reading mail 105 of 251: Топ новостей за 24 часа для вас
reading mail 106 of 251: ❤️ Валентинка с сюрпризом
reading mail 107 of 251: Iconographic Encyclopædia, Brand Names, pppointed, Design Tokens, The.com
reading mail 108 of 251: Фото дня: 15-летняя Валиева не сдерживает слез в объятиях Тутберидзе
reading mail 109 of 251: ✏ Creating Generative SVG Grids and more...
reading mail 110 of 251: У Вас новое личное сообщение [Geek Brains]
reading mail 111 of 251: ✏ Building an Adaptive Favicon and more...
reading mail 112 of 251: Топ новостей за 24 часа для вас
reading mail 113 of 251: Получите бесплатно 7 курсов
reading mail 114 of 251: instagram, kingjames и gal_gadot сделали новые публикации
reading mail 115 of 251: ✏ 16 Best Typeface Micro-Sites and more...
reading mail 116 of 251: Топ новостей за 24 часа для вас
reading mail 117 of 251: Vinted & Skyscanner screens
reading mail 118 of 251: 2022, Adaptive Favicon, CSSUI, Generative Grids, Move Over JavaScript
reading mail 119 of 251: Умерла 40-летняя звезда «Оттепели» Евгения Брик
reading mail 120 of 251: Готовы зарабатывать в IT через полгода?
reading mail 121 of 251: ✏ The Story of Campy the Typeface and more...
reading mail 122 of 251: Директора GeekBrains ждут вас в прямом эфире!
reading mail 123 of 251: Топ новостей за 24 часа для вас
reading mail 124 of 251: 🎆 Скидки до -40% на конфеты в коробках к празднику! 💕
reading mail 125 of 251: Adobe XD, Cassette Archive, Good News, Campy, Aspect Ratio
reading mail 126 of 251: Замешанная в допинг-скандале 15-летняя фигуристка продолжит участие в Олимпиаде
reading mail 127 of 251: 👨💻 Кому на IT-рынке жить хорошо
reading mail 128 of 251: ✏ Laravel 9 is Now Released and more...
reading mail 129 of 251: Активируй 500 бонусных рублей!
reading mail 130 of 251: Топ новостей за 24 часа для вас
reading mail 131 of 251: Персональные предложения на любимые товары!
reading mail 132 of 251: Context Menus, Old Masters, Chrome Icon, Diverging Palettes, Dialog Element
reading mail 133 of 251: 👨💻 Как попасть в IT за 6 месяцев
reading mail 134 of 251: ✏ 15 Best New Fonts February 2022, and more…
reading mail 136 of 251: Favicons, Japan Trip, Non-Boring Gradients, System Versioning, Design Memes
reading mail 137 of 251: 💕 Спецпредложения ко Дню Святого Валентина!
reading mail 138 of 251: Топ новостей за 24 часа для вас
reading mail 139 of 251: Минус 55% на цифровые профессии 2022
reading mail 140 of 251: Guide to Wordle, Groundhog Predictions, Red Light, Automator, Creating Components
reading mail 141 of 251: «Позволяли прятаться в доме»: как грабители вдовы Градского узнали о 100 млн рублей
reading mail 143 of 251: Топ новостей за 24 часа для вас
reading mail 144 of 251: ✏ How to Use Hand-Drawn Elements in Web Design and more...
reading mail 145 of 251: Топ новостей за 24 часа для вас
reading mail 146 of 251: 🔥 На что спорим?
reading mail 147 of 251: ✏ How to Do an A/B Testing and more...
reading mail 148 of 251: 3…2…Твоя СКИДКА почти сгорела🔥
reading mail 149 of 251: Топ новостей за 24 часа для вас
reading mail 150 of 251: Phantom & Luminary screens
reading mail 151 of 251: Бесплатный практикум по программированию
reading mail 152 of 251: Alexa, Washington Commanders, Vertex.im, Nifty Portal, Generative Art
reading mail 153 of 251: Можно ли дважды переболеть «омикроном»
reading mail 154 of 251: ✏ The Difference Between Good UI and Good UX and more...
reading mail 155 of 251: Топ новостей за 24 часа для вас
reading mail 156 of 251: Swyx Rewrite, Wordles, Settings, California Design System, SVG Drawing
reading mail 157 of 251: 🍊 Вкусные скидки Щедрых выходных до 6 февраля!
reading mail 158 of 251: Топ новостей за 24 часа для вас
reading mail 159 of 251: Issue #491: Fancy Borders, Untangling Flexbox Mysteries
reading mail 160 of 251: Знакомим с программированием за 7 дней
reading mail 161 of 251: Tesla Update, Inclusive Design, Block Protocol, HyperCardSimulator, Polypane 8
reading mail 162 of 251: 74-летняя София Ротару заразилась «омикроном»
reading mail 163 of 251: ✏ VR, AR, MR, XR: Which Reality is the Best? And more…
reading mail 164 of 251: Топ новостей за 24 часа для вас
reading mail 165 of 251: Get a .COM domain for FREE with hosting
reading mail 166 of 251: Haematopoiesis, Pipe Operator, Gerrymandering, fit-content, Amazon Psychology
reading mail 167 of 251: 💣⏰Кибер дни до 2 февраля! Успевайте!
reading mail 168 of 251: ✏ How to Customize a WooCommerce Product Page for Free and more...
reading mail 169 of 251: Топ новостей за 24 часа для вас
reading mail 170 of 251: Tesla UX, 30$ Website, Medieval Branding, Bytes, French Dispatch
reading mail 171 of 251: Барановскую заподозрили в романе с недавно разведенным Лепсом — и вот почему
reading mail 172 of 251: ✏ The Most Popular JavaScript Frameworks of 2022 and more...
reading mail 173 of 251: Топ новостей за 24 часа для вас
reading mail 174 of 251: Tech that will invade our lives in 2022
reading mail 175 of 251: 🏷️ Последние 36 часов распродажи
reading mail 176 of 251: У Вас новое личное сообщение [Geek Brains]
reading mail 177 of 251: ✏ How to Get Started With UX Research and more...
reading mail 178 of 251: Топ новостей за 24 часа для вас
reading mail 179 of 251: 🔥 Скидки до -50% в эти выходные!
reading mail 180 of 251: ✏ The Baseline For Web Development In 2022 and more...
reading mail 181 of 251: Топ новостей за 24 часа для вас
reading mail 182 of 251: Dusk & Grubhub screens
reading mail 183 of 251: Успей активировать 1500 бонусных рублей!
reading mail 185 of 251: Google Analytics, clay.css, where(), Semantics, Web Components
reading mail 186 of 251: 🎁 Дарим пробник цифровых профессий 2022
reading mail 187 of 251: Подарок в честь вашего Дня Рождения!
reading mail 188 of 251: Стильно! Пугачева выгуляла пуховик за 90 тысяч рублей и попала в объектив Галкина
reading mail 189 of 251: ✏ 5 Creative Management Trends to Watch in 2022 and more...
reading mail 190 of 251: Топ новостей за 24 часа для вас
reading mail 191 of 251: Как перестать откладывать дела на потом
reading mail 192 of 251: 🚀 Успейте купить! Щедрые выходные! Кибердни продолжаются!
reading mail 193 of 251: Maya Angelou, Arabic Type, Free Stuff, Background Shift, Hooked
reading mail 194 of 251: У Вас новое личное сообщение [Geek Brains]
reading mail 195 of 251: ✏ How to Build a Customer-Centric Culture, and more…
reading mail 196 of 251: Вам письмо от директора GeekBrains
reading mail 197 of 251: Топ новостей за 24 часа для вас
reading mail 199 of 251: Вдова Градского впервые прокомментировала ограбление: «Виновные понесут наказание»
reading mail 200 of 251: Вам пишет исполнительный директор GeekBrains
reading mail 201 of 251: ✏ How Do You Know if Your Design is Good? And more…
reading mail 202 of 251: Issue #490: Cascade Layers, CSS Fingerprint
reading mail 203 of 251: Топ новостей за 24 часа для вас
reading mail 204 of 251: Для тех, кто интересуется аналитикой
reading mail 205 of 251: Wordle UX, Charm, Accessibility, Pika, Physical Product
reading mail 206 of 251: 🎊 Кибер дни! Скидки до -60% на сотни товаров!
reading mail 207 of 251: Issue 336
reading mail 208 of 251: ✏ How I Scaled My Freelance Business To $10,000/month and more...
reading mail 209 of 251: Топ новостей за 24 часа для вас
reading mail 210 of 251: Вам письмо от директора GeekBrains
reading mail 211 of 251: Click and Swap, Frontend Predictions, Div Divisiveness, Changing Fonts, Spotify Icons
reading mail 212 of 251: Умер французский модельер Тьери Мюглер
reading mail 213 of 251: ✏ How To Make 6 Figures As A Freelancer and more...
reading mail 214 of 251: Как пойти в IT [если ты гуманитарий или технарь]
reading mail 215 of 251: ✏ How to Make a Chart With ChartJS and more...
reading mail 216 of 251: study.ai_172, посмотрите новости Shawn Mendes и The Tonight Show и других пользователей в своей ленте
reading mail 217 of 251: У Вас новое личное сообщение [Geek Brains]
reading mail 218 of 251: ✏ How to Get Started with the MVP Workflow and more...
reading mail 219 of 251: MetaMask & Babbel screens
reading mail 220 of 251: Wayfinding Icons, Cascade Layers, Tesla UI, Inspirational Websites, Component Libraries
reading mail 221 of 251: Подольская и Пресняков купили роскошную квартиру в центре столицы
reading mail 222 of 251: Минус 55% на цифровые профессии 2022
reading mail 223 of 251: ✏ How to Use Different CSS Color Values and more...
reading mail 224 of 251: Levels of Hype, Spatial Web, New Normal, Framer Sites, Badges
reading mail 225 of 251: 🏄 Щедрые выходные! Кибер дни! Распродажа!
reading mail 226 of 251: ✏ 10 Design Principles Every Designer Should Know, and more…
reading mail 227 of 251: Issue #489: Fluid Typography, Cascade Layers
reading mail 228 of 251: CSS Speedrun, GPS, Wiki History, UI Components, Writing With Respect
reading mail 229 of 251: IT для каждого
reading mail 230 of 251: Умер звезда «Моей прекрасной няни»
reading mail 231 of 251: ГАРАНТ. Новости органов государственной власти от 18.01.2022
reading mail 232 of 251: ГАРАНТ. Новое в налоговом законодательстве от 18.01.2022
reading mail 233 of 251: ✏ The Case Against UX Testing, and more…
reading mail 234 of 251: ГАРАНТ. Правовая картина дня от 18.01.2022
reading mail 235 of 251: ГАРАНТ. Главное для бухгалтера за день: информация Минфина и ФНС России, новости, правовые консультации от 18.01.2022
reading mail 237 of 251: Топ новостей за 24 часа для вас
reading mail 238 of 251: Хотите выиграть бесплатное обучение в GeekBrains?
reading mail 239 of 251: 3D Scenes, Rotae, Consistency Sin, Front-end Tools, Polka Dot
reading mail 240 of 251: 💣 Скидки до -90%! Распродажа!
reading mail 241 of 251: ГАРАНТ. Правовая картина дня от 17.01.2022
reading mail 242 of 251: ГАРАНТ. Главное для бухгалтера за день: информация Минфина и ФНС России, новости, правовые консультации от 17.01.2022
reading mail 244 of 251: instagram, jlo и shrutzhaasan сделали новые публикации
reading mail 245 of 251: ГАРАНТ. Ежедневный мониторинг московского законодательства от 17.01.2022
reading mail 246 of 251: ✏ 6 Ways Open-source Devs Can Make Money and more...
reading mail 247 of 251: ГАРАНТ. Самые важные документы недели от 17.01.2022
reading mail 248 of 251: Garant. Daily monitoring of the Federal legislation at 17.01.2022
reading mail 251 of 251: Встреча с генеральным директором GeekBrains
данные добавлены в базу данных
всего позиций: 239
"""