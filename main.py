from db_manager import DBManager
from hh_api import get_vacancies_by_company


def main():
    # Создаем экземпляр класса DBManager, указывая параметры подключения к базе данных
    db = DBManager(dbname="my_database", user="my_user",
                   password="my_password", host="localhost", port="5432")

    # Получаем список всех компаний и количества вакансий у каждой компании
    companies_and_vacancies_count = db.get_companies_and_vacancies_count()

    # Выводим результат на экран
    print("Companies and vacancies count:")
    for company, count in companies_and_vacancies_count:
        print(f"{company}: {count}")

    # Далее добавляем код для заполнения таблиц базы данных, например:
    for company in companies:
        vacancies = get_vacancies_by_company(company)
        for vacancy in vacancies:
            db.add_vacancy(company, vacancy)
            print(f"Adding vacancy: {vacancy['name']}")


if __name__ == "__main__":
    main()

