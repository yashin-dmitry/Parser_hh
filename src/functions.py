import configparser

import psycopg2

from src.db_manager import DBManager
from src.headhunterapi import HeadHunterAPI


def load_data(ids):
    user_input = input("Желаете ли вы занести информацию в БД? Y/N")
    if user_input.lower() == "y":

        db_manager = DBManager(dbname="postgres", user="postgres",
                               password="tdpro777", host="localhost",
                               port="5432")

        hh_api = HeadHunterAPI()
        for company in ids:
            print(f"Parsing vacancies for {company}...")

            vacancies = hh_api.load_vacancies(employer_id=company)
            one_company = hh_api.load_company(company)
            company_id = one_company["id"]
            company_name = one_company["name"]
            db_manager.add_company(company_id, company_name)
            for vacancy in vacancies:
                vacancy_id = vacancy['id']
                title = vacancy['name']
                salary = vacancy['salary']['from'] if vacancy[
                    'salary'] else None
                currency = vacancy['salary']['currency'] if vacancy[
                    'salary'] else None
                url = vacancy['alternate_url']
                try:
                    db_manager.add_vacancy(vacancy_id, company, title, salary,
                                           currency, url)
                except psycopg2.errors.UniqueViolation:
                    continue
                print(f"Added vacancy: {title}")

        db_manager.close()


def read_config(path_to_config):
    config = configparser.ConfigParser()

    # Явно указываем кодировку UTF-8 при чтении файла конфигурации
    config.read(path_to_config, encoding='utf-8')

    DB_CONFIG = {
        'dbname': config.get('DB', 'dbname'),
        'user': config.get('DB', 'user'),
        'password': config.get('DB', 'password'),
        'host': config.get('DB', 'host'),
        'port': config.get('DB', 'port')
    }

    COMPANIES = config.get('COMPANIES', 'companies').split(', ')

    return COMPANIES, DB_CONFIG
