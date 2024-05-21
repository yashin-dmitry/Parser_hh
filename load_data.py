import psycopg2

from main import hh_data


def insert_company(conn, company):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO companies (name, url) VALUES (%s, %s) ON CONFLICT DO "
            "NOTHING",
            (company["name"], company["url"]))
        conn.commit()


def insert_vacancy(conn, vacancy, company_id):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO vacancies (name, url, salary, company_id) VALUES ("
            "%s, %s, %s, %s)",
            (vacancy["name"], vacancy["url"], vacancy["salary"], company_id))
        conn.commit()


def load_data_to_db(hh_data):
    conn = psycopg2.connect(database="hh_db", user="postgres",
                            password="postgres", host="127.0.0.1", port="5432")

    for item in hh_data:
        company = item["employer"]
        insert_company(conn, company)

        vacancy = item
        vacancy["salary"] = vacancy["salary"]["from"] if (vacancy["salary"]
                                                          ["to"] is None) else (
            f"{vacancy['salary']['from']} - "
            f"{vacancy['salary']['to']}")
        del vacancy["employer"]
        del vacancy["salary"]
        del vacancy["area"]
        del vacancy["published_at"]

        company_id = \
            conn.cursor().execute("SELECT id FROM companies WHERE name = %s",
                                  (company["name"],)).fetchone()[0]

        insert_vacancy(conn, vacancy, company_id)

    conn.close()


load_data_to_db(hh_data)
