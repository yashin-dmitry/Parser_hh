import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(dbname=dbname, user=user,
                                     password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def add_vacancy(self, company, vacancy):
        # Проверяем, существует ли компания в базе данных
        self.cur.execute("SELECT id FROM companies WHERE name = %s", (company,))
        company_id = self.cur.fetchone()
        if not company_id:
            # Если компании нет в базе данных, добавляем ее
            self.cur.execute(
                "INSERT INTO companies (name) VALUES (%s) RETURNING id",
                (company,))
            company_id = self.cur.fetchone()[0]
        else:
            company_id = company_id[0]

        # Проверяем, существует ли вакансия в базе данных
        self.cur.execute(
            "SELECT id FROM vacancies WHERE company_id = %s AND name = %s",
            (company_id, vacancy['name']))
        vacancy_id = self.cur.fetchone()
        if not vacancy_id:
            # Если вакансии нет в базе данных, добавляем ее
            self.cur.execute(
                "INSERT INTO vacancies (company_id, name, salary, url) VALUES "
                "(%s, %s, %s, %s)",
                (
                    company_id, vacancy['name'], vacancy['salary'],
                    vacancy['url']))
            self.conn.commit()
