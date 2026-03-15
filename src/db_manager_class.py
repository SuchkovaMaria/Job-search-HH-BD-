from typing import Any

import psycopg2


class DBManager:
    """Класс обращения к БД"""

    def __init__(self, dbname: str, params: dict[str, Any]):
        """Инициализация менеджера базы данных"""

        self.dbname = dbname
        self.params = params
        self.conn = None

    def get_companies_and_vacancies_count(self) -> list[list]:
        """Получение списка всех компаний и количество их вакансий в БД"""

        self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employer_name, COUNT(*) FROM employer
                JOIN vacancies USING (employer_id)
                GROUP BY employer_id""")
            list_employer = cur.fetchall()
        self.conn.commit()
        self.conn.close()

        list_employer_res = [list(i) for i in list_employer]
        return list_employer_res

    def get_all_vacancies(self) -> list[list]:
        """Получение списока всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""

        self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employer_name, vacancy_name, salary_from, vacancy_url FROM employer
                JOIN vacancies USING (employer_id)
                """)
            list_vacancies = cur.fetchall()
        self.conn.commit()
        self.conn.close()

        list_vacancies_res = [list(i) for i in list_vacancies]

        return list_vacancies_res

    def get_avg_salary(self) -> float | None:
        """Получение средней заработной платы по вакансиям"""

        self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
        with self.conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies
                """)
            avg_salary = cur.fetchall()
        self.conn.commit()
        self.conn.close()
        result = round(float(avg_salary[0][0]), 1)
        return result

    def get_vacancies_with_higher_salary(self) -> list[list]:
        """Получение списка вакансий, у которых зарплата выше средней по всем вакансиям"""

        self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
        with self.conn.cursor() as cur:
            cur.execute("""SELECT employer_name, vacancy_name, salary_from FROM vacancies
                JOIN employer USING (employer_id)
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                """)
            list_vacancies_big_zp = cur.fetchall()
        self.conn.commit()
        self.conn.close()

        list_vacancies_big_zp_res = [list(i) for i in list_vacancies_big_zp]

        return list_vacancies_big_zp_res

    def get_vacancies_with_keyword(self, search_word: str) -> list[list]:
        """Получение списка вакансий по указанному слову"""

        self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT employer_name, vacancy_name FROM vacancies
                JOIN employer USING (employer_id)
                WHERE LOWER(vacancy_name) LIKE LOWER (%s)""",
                (f"%{search_word}%",),
            )
            list_vacancies_db = cur.fetchall()
        self.conn.commit()
        self.conn.close()

        list_vacancies_db_res = [list(i) for i in list_vacancies_db]

        return list_vacancies_db_res
