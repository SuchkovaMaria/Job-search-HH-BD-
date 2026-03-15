from typing import Any

import psycopg2
import requests

from config import config_params


def api_vacansy() -> list[dict]:
    """Функция получения списка вакансий из API"""

    url_requests = "https://api.hh.ru/vacancies"
    params_requests = {
        "employer_id": ["15478", "3529", "1740", "78638", "4181", "3776", "39305", "87021", "2180", "64174"],
        "host": "hh.ru",
    }
    headers_requests = {
        "HH-User-Agent": "HH-User-Agent",
    }

    response = requests.get(url=url_requests, params=params_requests, headers=headers_requests)
    data = response.json()

    return data["items"]


def create_database(database_name: str | Any) -> None:
    """Создание бызы данных и таблиц"""

    params_sql = config_params()
    connect_sql = psycopg2.connect(dbname="postgres", **params_sql)
    connect_sql.autocommit = True
    cursor_sql = connect_sql.cursor()
    cursor_sql.execute(f"DROP DATABASE {database_name}")
    cursor_sql.execute(f"CREATE DATABASE {database_name}")

    cursor_sql.close()
    connect_sql.close()

    conn = psycopg2.connect(dbname=database_name, **params_sql)
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE employer (
            employer_id varchar(20) PRIMARY KEY,
            employer_name varchar(100) NOT NULL,
            employer_url TEXT,
            employer_alternate_url TEXT NOT NULL)""")

    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE vacancies (
            vacancy_id varchar(20) PRIMARY KEY,
            vacancy_name varchar(100) NOT NULL,
            salary_from INT,
            salary_to INT,
            vacancy_url TEXT,
            employer_id varchar(20) REFERENCES employer(employer_id))""")

    conn.commit()
    conn.close()


def save_data_database(data_vacancies: list[dict[str, Any]], database_name: str | Any) -> None:
    """Функция заполнения таблиц"""

    params_sql = config_params()
    conn = psycopg2.connect(dbname=database_name, **params_sql)
    with conn.cursor() as cur:
        employer_in_tabl = []
        for employer in data_vacancies:
            employer_id = employer["employer"]["id"]
            if employer_id not in employer_in_tabl:
                employer_in_tabl.append(employer_id)
                employer_name = employer["employer"]["name"]
                employer_url = employer["employer"]["url"]
                employer_alternate_url = employer["employer"]["alternate_url"]
                cur.execute(
                    """
                INSERT INTO employer (employer_id, employer_name, employer_url, employer_alternate_url)
                VALUES (%s, %s, %s, %s)
                """,
                    (employer_id, employer_name, employer_url, employer_alternate_url),
                )

        for vacancy in data_vacancies:
            vacancy_id = vacancy["id"]
            vacancy_name = vacancy["name"]
            if not vacancy["salary"]:
                salary_from = None
                salary_to = None
            else:
                salary_from = vacancy["salary"]["from"]
                salary_to = vacancy["salary"]["to"]
            vacancy_url = vacancy["url"]
            employer_id = vacancy["employer"]["id"]
            cur.execute(
                """
                        INSERT INTO vacancies
                        (vacancy_id, vacancy_name, salary_from, salary_to, vacancy_url, employer_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                (vacancy_id, vacancy_name, salary_from, salary_to, vacancy_url, employer_id),
            )

    conn.commit()
    conn.close()
