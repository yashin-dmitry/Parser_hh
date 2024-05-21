import psycopg2


class DBManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(dbname=dbname, user=user,
                                     password=password, host=host, port=port)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT c.name, COUNT(v.id) FROM companies c JOIN vacancies v "
                "ON c.id = v.company_id GROUP BY c.id")
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT v.name, v.salary, v.url, c.name FROM vacancies v JOIN "
                "companies c ON v.company_id = c.id")
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(v.salary) FROM vacancies v")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT v.name, v.salary, v.url, c.name FROM vacancies v JOIN "
                "companies c ON v.company_id = c.id WHERE v.salary > (SELECT "
                "AVG(v.salary) FROM vacancies v)")
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT v.name, v.salary, v.url, c.name FROM vacancies v JOIN "
                "companies c ON v.company_id = c.id WHERE v.name LIKE %s",
                (f"%{keyword}%",))
            return cur.fetchall()
