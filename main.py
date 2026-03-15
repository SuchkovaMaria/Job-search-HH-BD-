from tabulate import tabulate

from config import config_params
from src.db_manager_class import DBManager
from src.utils import api_vacansy, create_database, save_data_database


def main():

    data = api_vacansy()
    create_database("vacancies")
    save_data_database(data, "vacancies")

    instance = DBManager("vacancies", config_params())
    operation = input(
        "Добро пожаловать в менеджер управления вакансиями!\n"
        "Выберите действие:\n"
        "1. Показать весь список компаний с количеством вакансий по ним;\n"
        "2. Показать список всех вакансий;\n"
        "3. Показать среднюю заработную плату по вакансиям;\n"
        "4. Показать список вакансий, у которых заработная плата выше средней;\n"
        "5. Поиск вакансий по слову.\n"
    )

    if operation == "1":
        print(
            tabulate(
                instance.get_companies_and_vacancies_count(),
                headers=["Компания", "Количество вакансий"],
                tablefmt="orgtbl",
            )
        )
    elif operation == "2":
        print(
            tabulate(
                instance.get_all_vacancies(),
                headers=["Компания", "Вакансия", "ЗП", "Ссылка на вакансию"],
                tablefmt="orgtbl",
            )
        )
    elif operation == "3":
        sr_salary = instance.get_avg_salary()
        print(f"Средняя заработная плата по вакансиям: {sr_salary}")
    elif operation == "4":
        print(
            tabulate(
                instance.get_vacancies_with_higher_salary(), headers=["Компания", "Вакансия", "ЗП"], tablefmt="orgtbl"
            )
        )
    elif operation == "5":
        key_word = input("Введите слово для поиска:\n")
        info = instance.get_vacancies_with_keyword(key_word)
        if len(info) == 0:
            print(f"Вакансий по слову {key_word} не найдено")
        else:
            print(tabulate(info, headers=["Компания", "Вакансия"], tablefmt="orgtbl"))
    else:
        print("Неверно введены данные")


if __name__ == "__main__":
    main()
