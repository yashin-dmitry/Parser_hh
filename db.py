import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def create_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            name VARCHAR(255) NOT NULL,
            salary INTEGER,
            currency VARCHAR(10),
            url VARCHAR(255)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def add_company(name):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO companies (name) VALUES (%s) ON CONFLICT DO NOTHING;",
        (name,))
    conn.commit()
    cur.close()
    conn.close()


def get_company_id(name):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("SELECT id FROM companies WHERE name=%s;", (name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None


def add_vacancy(company_name, name, salary, currency, url):
    company_id = get_company_id(company_name)
    if company_id is None:
        add_company(company_name)
        company_id = get_company_id(company_name)
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO vacancies (company_id, name, salary, currency, "
        "url) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
        (company_id, name, salary, currency, url))
    conn.commit()
    cur.close()
    conn.close()


def get_companies_and_vacancies_count():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, COUNT(v.id)
        FROM companies c
        LEFT JOIN vacancies v ON c.id = v.company_id
        GROUP BY c.id
        ORDER BY COUNT(v.id) DESC;
    """)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_all_vacancies():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, v.name, v.salary, v.currency, v.url
        FROM vacancies v
        INNER JOIN companies c ON v.company_id = c.id
        ORDER BY v.salary DESC, v.name ASC;
    """)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_avg_salary():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(salary)
        FROM vacancies
        WHERE salary IS NOT NULL;
    """)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0]


def get_vacancies_with_higher_salary():
    avg_salary = get_avg_salary()
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, v.name, v.salary, v.currency, v.url
        FROM vacancies v
        INNER JOIN companies c ON v.company_id = c.id
        WHERE v.salary > %s
        ORDER BY v.salary DESC, v.name ASC;
    """, (avg_salary,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_vacancies_with_keyword(keyword):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, v.name, v.salary, v.currency, v.url
        FROM vacancies v
        INNER JOIN companies c ON v.company_id = c.id
        WHERE v.name ILIKE %s
        ORDER BY v.salary DESC, v.name ASC;
    """, (f"%{keyword}%",))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
