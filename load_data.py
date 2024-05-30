import requests
from bs4 import BeautifulSoup
from db_manager import DBManager
from config import COMPANIES, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def load_data():
    db_manager = DBManager(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                           host=DB_HOST, port=DB_PORT)

    for company in COMPANIES:
        print(f"Parsing vacancies for {company}...")

        # Выполняем запрос к API HeadHunter
        url = f"https://hh.ru/search/vacancy?text=Сбербанк+AND+Python&area=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Парсим данные о вакансиях
        vacancies = soup.find_all("div", class_="vacancy-serp-item")
        for vacancy in vacancies:
            title = vacancy.find("a", class_="bloko-link").text.strip()
            salary = vacancy.find("span", class_="bloko-header-section-3")
            if salary:
                salary = salary.text.strip().replace("\xa0", "").replace(" ",
                                                                         "")
            else:
                salary = None
            url = f"https://hh.ru{vacancy.find('a', class_='bloko-link')['href']}"

            # Загружаем данные в базу данных
            company_id = db_manager.get_company_id(company)
            if company_id:
                db_manager.add_vacancy(company_id, title, salary, url)

    db_manager.close()
