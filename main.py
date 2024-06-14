import os
from src.db_manager import DBManager
from src.functions import load_data, read_config
from src.hh_api import get_vacancies_by_company

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')
def main():
    list_id, config_connect = read_config(CONFIG_PATH)
    load_data(list_id)
    # # Создаем экземпляр класса DBManager, указывая параметры подключения к базе данных
    # db = DBManager(dbname="postgres", user="postgres",
    #                password="tdpro777", host="localhost", port="5432")
    #
    # # Получаем список всех компаний и количества вакансий у каждой компании
    # companies_and_vacancies_count = db.get_companies_and_vacancies_count()
    #
    # # Выводим результат на экран
    # print("Companies and vacancies count:")
    # for company, count in companies_and_vacancies_count:
    #     print(f"{company}: {count}")
    #
    # # Далее добавляем код для заполнения таблиц базы данных, например:
    # for company in companies:
    #     vacancies = get_vacancies_by_company(company)
    #     for vacancy in vacancies:
    #         db.add_vacancy(company, vacancy)
    #         print(f"Adding vacancy: {vacancy['name']}")


if __name__ == "__main__":
    main()

