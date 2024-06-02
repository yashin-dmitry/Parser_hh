import configparser
import os
from db_manager import DBManager
from hh_api import get_vacancies_by_company

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

db_config = {
    'dbname': config.get('DB', 'dbname'),
    'user': config.get('DB', 'user'),
    'password': config.get('DB', 'password'),
    'host': config.get('DB', 'host'),
    'port': config.get('DB', 'port')
}

companies = config.get('COMPANIES', 'companies').split(',')

db_manager = DBManager(**db_config)

for company in companies:
    vacancies = get_vacancies_by_company(company.strip())
    for vacancy in vacancies:
        db_manager.add_vacancy(company, vacancy)
        print(f"Adding vacancy: {vacancy['name']}")
        db_manager.add_vacancy(company, vacancy)
        print(f"Vacancy added: {vacancy['name']}")

print("Данные успешно добавлены в базу данных")
