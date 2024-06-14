import psycopg2

class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(dbname=dbname, user=user,
                                     password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS companies (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE
                );
            """)
        with self.conn:
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY,
                    company_id INTEGER REFERENCES companies(id),
                    name VARCHAR(255) NOT NULL,
                    salary INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(255)
                );
            """)

    def add_vacancy(self, vacancy_id, company, title, salary, currency, url):
        with self.conn:
            self.cur.execute(
                "INSERT INTO vacancies (id, company_id, name, salary, currency, url) VALUES "
                "(%s, %s, %s, %s, %s, %s)",
                (vacancy_id, company, title, salary, currency, url))

    def add_company(self, company_id, company_name):
        with self.conn:
            self.cur.execute(
                "INSERT INTO companies (id, name) VALUES "
                "(%s, %s)",
                (company_id, company_name))

    def get_company_id(self, company_name):
        self.cur.execute("SELECT id FROM companies WHERE name=%s;", (company_name,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_companies_and_vacancies_count(self):
        self.cur.execute("""
            SELECT companies.name, COUNT(vacancies.id)
            FROM companies
            LEFT JOIN vacancies ON companies.id = vacancies.company_id
            GROUP BY companies.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("""
            SELECT companies.name, vacancies.name, vacancies.salary, vacancies.currency, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("""
            SELECT AVG(salary)
            FROM vacancies
        """)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("""
            SELECT *
            FROM vacancies
            WHERE salary > %s
        """, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute("""
            SELECT *
            FROM vacancies
            WHERE name ILIKE %s
        """, ('%' + keyword + '%',))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
