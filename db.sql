CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255)
);

CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255),
    salary VARCHAR(255),
    company_id INTEGER REFERENCES companies(id)
);
