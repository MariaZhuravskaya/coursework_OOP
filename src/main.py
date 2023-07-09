from src.utils import HeadHunterAPI, SuperJobAPI, JSONSaver, ComparisonVacancies


# Функция для взаимодействия с пользователем

def user_interaction():

    # Разрешенные платформы ввода
    supported_apis = {
        'HeadHunter': HeadHunterAPI(),
        'SuperJob': SuperJobAPI(),
    }

    # Выбор платформы пользователя
    apis = {

    }

    while True:
        search_query = input("Выберите платформу с которой желаете получить вакансии: HeadHunter или SuperJob или список через запятую \n")
        platforms = search_query.split(",")
        all_ok = True
        for platform in platforms:
            platform = platform.strip()
            if platform not in supported_apis:
                all_ok = False
                break
            else:
                apis.setdefault(platform, supported_apis.get(platform))
        if all_ok:
            break

    search_query_vacancies = input("Какую вакансию ищем? Ключевые слова? \n")
    comparison = input("Сортировать вакансии по уровню заработной платы? 'Да'/ 'Нет': \n").upper()
    filter_words = input("Задать уровень заработной платы?: 'Да'/ 'Нет': \n").upper()

    if search_query_vacancies == "":
        search_query_vacancies = 'Python'

    if filter_words == "":
        filter_words_salary_from = 10000
        filter_words_salary_to = 800000

    if filter_words == 'ДА':
        filter_words_salary_from = input("Введите нижнее значение границы: ")
        filter_words_salary_to = input("Введите верхнее значение границы: ")
    top_n = int(input("Введите количество вакансий для вывода: \n"))

    json_saver = JSONSaver()

    # Список вакансий с всех заданных платформ пользователем
    all_vacancies = []
    for api_name in apis.keys():
        api = apis.get(api_name)

        vacancies = api.get_vacancies(search_query_vacancies)
        all_vacancies.extend(vacancies)

    if all_vacancies == []:
        raise TypeError("Нет вакансий, соответствующих заданным критериям. Повторите запрос.")

    if comparison == 'ДА' or comparison == "":
        comparison_vacancies = ComparisonVacancies()
        comparison_lst = comparison_vacancies.comparison(all_vacancies)
    else:
        comparison_lst = all_vacancies
    json_saver.add_vacancy(comparison_lst)

    if filter_words == 'ДА' or filter_words == "":
        result_list = json_saver.get_vacancies_by_salary(int(filter_words_salary_from), int(filter_words_salary_to))
    else:
        delete_vacancy = input("Удалить вакансии, если не указан уровень заработной платы? 'Да'/ 'Нет': \n").upper()
        if delete_vacancy == 'ДА' or comparison == "":
            result_list = json_saver.delete_vacancy_salary()
        else:
            result_list = json_saver.get_all()
    return json_saver.get_top_vacancies(top_n, result_list)


if __name__ == "__main__":
    d = user_interaction()
    for j, i in enumerate(d):
        print()
        print(
            f"""{j + 1}. {i.name}\n{i.url}\nУровень заработной платы: {i.salary}\nВид занятости: {i.employment}\nОпыт работы: {i.experience}\nТребования к кандидату: {i.description}""")
