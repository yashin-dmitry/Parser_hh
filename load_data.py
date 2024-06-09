from db_manager import DBManager
from config import COMPANIES
from hh_api import get_vacancies_by_company

def load_data():
    db_manager = DBManager()

    for company in COMPANIES:
        print(f"Parsing vacancies for {company}...")

        vacancies = get_vacancies_by_company(company)

        for vacancy in vacancies:
            title = vacancy['name']
            salary = vacancy['salary']['from'] if vacancy['salary'] else None
            currency = vacancy['salary']['currency'] if vacancy['salary'] else None
            url = vacancy['alternate_url']

            db_manager.add_vacancy(company, title, salary, currency, url)
            print(f"Added vacancy: {title}")

    db_manager.close()

if __name__ == "__main__":
    load_data()

