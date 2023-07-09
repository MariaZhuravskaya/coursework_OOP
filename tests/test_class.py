import pytest

import src
from src.utils import SuperJobAPI, HeadHunterAPI, Vacancy, ComparisonVacancies, JSONSaver


def test_get_vacancies():
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()
    # Получение вакансий с платформ
    hh_vacancies = hh_api.get_vacancies("Python")
    superjob_vacancies = superjob_api.get_vacancies("Python")
    assert len(hh_vacancies) > 0
    assert isinstance(hh_vacancies[0], Vacancy)
    assert len(superjob_vacancies) > 0
    assert isinstance(superjob_vacancies[0], Vacancy)


def test_comparison():
    vacancies = [
        src.utils.Vacancy("1", "", "70 - 100", 70, 100, "", "", "", "", ""),
        src.utils.Vacancy("2", "", "50 - 120", 50, 120, "", "", "", "", ""),
        src.utils.Vacancy("3", "", "20 - 80", 20, 80, "", "", "", "", "")
    ]

    comparison_vacancies = ComparisonVacancies()
    comparison_lst = comparison_vacancies.comparison(vacancies)

    assert len(comparison_lst) == len(vacancies)
    assert comparison_lst[0].name == "3"
    assert comparison_lst[1].name == "2"
    assert comparison_lst[2].name == "1"


def test_get_vacancies_by_salary():
    filter_words_salary_from = '50000'
    filter_words_salary_to = '150000'
    json_saver = JSONSaver()
    vacancies = [
        src.utils.Vacancy("1", "", "70000 - 100000", 70000, 100000, "", "", "", "", ""),
        src.utils.Vacancy("2", "", "50000 - 120000", 50000, 120000, "", "", "", "", ""),
        src.utils.Vacancy("3", "", "20000 - 80000", 20000, 80000, "", "", "", "", ""),
        src.utils.Vacancy("4", "", "100000 - 180000", 100000, 180000, "", "", "", "", ""),
        src.utils.Vacancy("5", "", "5000 - 15000", 5000, 15000, "", "", "", "", "")
    ]
    json_saver.add_vacancy(vacancies)
    result_list = json_saver.get_vacancies_by_salary(int(filter_words_salary_from), int(filter_words_salary_to))

    assert result_list[0].name == "1"
    assert result_list[1].name == "2"
    assert len(result_list) == 2


def test_delete_vacancy_salary():
    json_saver = JSONSaver()
    vacancies = [
        src.utils.Vacancy("1", "", "70000 - 100000", 70000, 100000, "", "", "", "", ""),
        src.utils.Vacancy("2", "", "0 - 0", 0, 0, "", "", "", "", ""),
        src.utils.Vacancy("3", "", "20000 - 80000", 20000, 80000, "", "", "", "", ""),
        src.utils.Vacancy("4", "", "100000 - 180000", 100000, 180000, "", "", "", "", ""),
        src.utils.Vacancy("5", "", "0 - 0", 0, 0, "", "", "", "", "")
    ]
    json_saver.add_vacancy(vacancies)
    result_list = json_saver.delete_vacancy_salary()

    assert result_list[0].name == "1"
    assert result_list[1].name == "3"
    assert result_list[2].name == "4"
    assert len(result_list) == 3


def test_get_top_vacancies():
    json_saver = JSONSaver()
    top_n = 2
    vacancies = [
        src.utils.Vacancy("1", "", "70000 - 100000", 70000, 100000, "", "", "", "", ""),
        src.utils.Vacancy("2", "", "0 - 0", 0, 0, "", "", "", "", ""),
        src.utils.Vacancy("3", "", "20000 - 80000", 20000, 80000, "", "", "", "", ""),
        src.utils.Vacancy("4", "", "90000 - 100000", 90000, 100000, "", "", "", "", ""),
        src.utils.Vacancy("5", "", "60000 - 90000", 60000, 90000, "", "", "", "", ""),
        src.utils.Vacancy("6", "", "55000 - 70000", 55000, 70000, "", "", "", "", ""),
        src.utils.Vacancy("7", "", "0 - 0", 0, 0, "", "", "", "", "")
    ]
    json_saver.add_vacancy(vacancies)
    result_list = json_saver.delete_vacancy_salary()
    json_saver.get_top_vacancies(top_n, result_list)
    assert result_list[0].name == "1"
    assert result_list[1].name == "3"
    assert len(result_list) == 5

@pytest.fixture()
def fixture_hh_vacancies():
    hh_vacancies = [
        src.utils.Vacancy("1. Junior/Middle backend разработчик на Fast API (Python)","https://api.hh.ru/vacancies/82841724?host=hh.ru", "60000 - 100000", 60000, 100000,"Полная занятость", "От 1 года до 3 лет","Уверенные знаниями языка и стандартных библиотек Python 3. Умение писать качественный и эффективный код на Python","", ""),
        src.utils.Vacancy("2. Data-инженер/Python-разработчик (strong junior)","https://api.hh.ru/vacancies/82440187?host=hh.ru", "70000 - 120000", 70000, 120000, "Полная занятость", "Нет опыта", "Среднее профессиональное образование", "", ""),
        src.utils.Vacancy("3. Программист", "https://api.hh.ru/vacancies/82650854?host=hh.ru", "55000 - 110000", 55000, 110000, "", "", "", "", ""),
        src.utils.Vacancy("4. PHP-программист", "https://api.hh.ru/vacancies/83030748?host=hh.ru", "100000 - 180000", 100000, 180000, "", "", "", "", ""),
        src.utils.Vacancy("5. Аналитик данных", "https://api.hh.ru/vacancies/81241165?host=hh.ru", "0 - 0", 0, 0, "", "", "", "", "")
    ]
    return hh_vacancies


def test_user_interaction_1(fixture_hh_vacancies):

    search_query_vacancies = 'Python'  # input("Какую вакансию ищем? Ключевые слова? \n")
    comparison = 'Да'   # input("Сортировать вакансии по уровню заработной платы? 'Да'/ 'Нет': \n").upper()
    filter_words = 'Да'   # input("Задать уровень заработной платы?: 'Да'/ 'Нет': \n").upper()
    filter_words_salary_from = '50000'    #    input("Введите нижнее значение границы: ")
    filter_words_salary_to = '120000'     # input("Введите верхнее значение границы: ")
    top_n = 3   #int(input("Введите количество вакансий для вывода: \n"))

    comparison_vacancies = ComparisonVacancies()
    comparison_lst = comparison_vacancies.comparison(fixture_hh_vacancies)
    json_saver = JSONSaver()
    json_saver.add_vacancy(comparison_lst)
    result_list = json_saver.get_vacancies_by_salary(int(filter_words_salary_from), int(filter_words_salary_to))
    json_saver.get_top_vacancies(top_n, result_list)
    assert result_list[0].name == "3. Программист"
    assert result_list[1].name == "1. Junior/Middle backend разработчик на Fast API (Python)"
    assert result_list[2].name == "2. Data-инженер/Python-разработчик (strong junior)"
    assert result_list[1].salary == "60000 - 100000"
    assert result_list[1].url == "https://api.hh.ru/vacancies/82841724?host=hh.ru"

def test_user_interaction_2(fixture_hh_vacancies):

    search_query_vacancies = 'Python'  # input("Какую вакансию ищем? Ключевые слова? \n")
    comparison = 'Нет'   # input("Сортировать вакансии по уровню заработной платы? 'Да'/ 'Нет': \n").upper()
    filter_words = 'Да'   # input("Задать уровень заработной платы?: 'Да'/ 'Нет': \n").upper()
    filter_words_salary_from = '50000'    #    input("Введите нижнее значение границы: ")
    filter_words_salary_to = '120000'     # input("Введите верхнее значение границы: ")
    top_n = 3   #int(input("Введите количество вакансий для вывода: \n"))

    json_saver = JSONSaver()
    json_saver.add_vacancy(fixture_hh_vacancies)
    result_list = json_saver.get_vacancies_by_salary(int(filter_words_salary_from), int(filter_words_salary_to))
    json_saver.get_top_vacancies(top_n, result_list)
    assert result_list[0].name == "1. Junior/Middle backend разработчик на Fast API (Python)"
    assert result_list[1].name == "2. Data-инженер/Python-разработчик (strong junior)"
    assert result_list[2].name == "3. Программист"


def test_user_interaction_3(fixture_hh_vacancies):

    search_query_vacancies = 'Python'  # input("Какую вакансию ищем? Ключевые слова? \n")
    comparison = 'Нет'   # input("Сортировать вакансии по уровню заработной платы? 'Да'/ 'Нет': \n").upper()
    filter_words = 'Нет'   # input("Задать уровень заработной платы?: 'Да'/ 'Нет': \n").upper()
    top_n = 5   #int(input("Введите количество вакансий для вывода: \n"))

    json_saver = JSONSaver()
    json_saver.add_vacancy(fixture_hh_vacancies)
    result_list = json_saver.get_all()
    json_saver.get_top_vacancies(top_n, result_list)
    assert result_list[0].name == "1. Junior/Middle backend разработчик на Fast API (Python)"
    assert result_list[1].name == "2. Data-инженер/Python-разработчик (strong junior)"
    assert result_list[2].name == "3. Программист"
    assert result_list[3].name == "4. PHP-программист"
    assert result_list[4].name == "5. Аналитик данных"
    assert len(result_list) == 5

def test_user_interaction_4(fixture_hh_vacancies):

    search_query_vacancies = 'Python'  # input("Какую вакансию ищем? Ключевые слова? \n")
    comparison = 'Нет'   # input("Сортировать вакансии по уровню заработной платы? 'Да'/ 'Нет': \n").upper()
    filter_words = 'Нет'   # input("Задать уровень заработной платы?: 'Да'/ 'Нет': \n").upper()
    delete_vacancy = 'Да' #input("Удалить вакансии, если не указан уровень заработной платы? 'Да'/ 'Нет': \n").upper()
    top_n = 4   #int(input("Введите количество вакансий для вывода: \n"))

    json_saver = JSONSaver()
    json_saver.add_vacancy(fixture_hh_vacancies)
    result_list = json_saver.delete_vacancy_salary()
    json_saver.get_top_vacancies(top_n, result_list)
    assert result_list[0].name == "1. Junior/Middle backend разработчик на Fast API (Python)"
    assert result_list[1].name == "2. Data-инженер/Python-разработчик (strong junior)"
    assert result_list[2].name == "3. Программист"
    assert result_list[3].name == "4. PHP-программист"
    assert len(result_list) == 4


