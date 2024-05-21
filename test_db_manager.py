from db_manager import DBManager

def main():
    db_manager = DBManager(dbname="hh_db", user="postgres", password="postgres", host="127.0.0.1", port="5432")

    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    print("Companies and vacancies count:")
    for company, count in companies_and_vacancies_count:
        print(f"{company}: {count}")

    all_vacancies = db_manager.get_all_vacancies()
    print("\nAll vacancies:")
    for vacancy, salary, url, company in all_vacancies:
        print(f"{vacancy} ({salary}) [{url}] ({company})")

    avg_salary = db_manager.get_avg_salary()
    print(f"\nAverage salary: {avg_salary}")

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    print("\nVacancies with higher salary:")
    for vacancy, salary, url, company in vacancies_with_higher_salary:
        print(f"{vacancy} ({salary}) [{url}] ({company})")

    vacancies_with_keyword = db_manager.get_vacancies_with_keyword("Python")
    print("\nVacancies with keyword 'Python':")
    for vacancy, salary, url, company in vacancies_with_keyword:
        print(f"{vacancy} ({salary}) [{url}] ({company})")

if __name__ == "__main__":
    main()
