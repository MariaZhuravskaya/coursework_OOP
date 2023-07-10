from src.utils import HeadHunterAPI, SuperJobAPI, JSONSaver, ComparisonVacancies


# Функция для взаимодействия с пользователем
class UserInteraction:
    json_saver = JSONSaver()

    def get_platforms_input(self):
        """Метод возвращает ответ пользователя о платформе с которой желаете получить вакансии"""
        return input("Выберите платформу с которой желаете получить вакансии: HeadHunter или SuperJob или список через запятую \n")

    def search_query_api(self, get_platforms_callback):
        """Метод возвращает словарь с выбранными платформами"""

        # Разрешенные платформы ввода
        supported_apis = {
            'HeadHunter': HeadHunterAPI(),
            'SuperJob': SuperJobAPI(),
        }

        # Выбор платформы пользователя
        apis = {

        }

        while True:
            search_query = get_platforms_callback()
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
        return apis

    def get_query_vacancies(self):
        """Метод возвращает ответ пользователя какую вакансию ищем"""
        return input("Какую вакансию ищем? Ключевые слова? \n")
    def search_query_vacancies(self, get_vacancies):
        """Метод возвращает ответ пользователя какую вакансию ищем"""
        search_query_vacancies = get_vacancies()
        if search_query_vacancies == "":
            search_query_vacancies = 'Python'
        return search_query_vacancies

    def comparison(self):
        """Метод возвращает ответ пользователя """
        return input("Сортировать вакансии по уровню заработной платы? 'Да'/ 'Нет': \n").upper()

    def filter_words(self):
        """Метод возвращает ответ пользователя """
        return input("Задать уровень заработной платы?: 'Да'/ 'Нет': \n").upper()

    def get_filter_words_salary_from(self):
        """Метод возвращает ответ пользователя """
        return input("Введите нижнее значение границы: ")

    def get_filter_words_salary_to(self):
        """Метод возвращает ответ пользователя """
        return input("Введите верхнее значение границы: ")

    def filter_words_salary(self, filter_input, get_filter_words_salary_from, get_filter_words_salary_to):
        """Метод возвращает список границ фильтров вакансий по ЗП """
        if filter_input == "":
            filter_words_salary_from = 10000
            filter_words_salary_to = 800000
            return [filter_words_salary_from, filter_words_salary_to]

        if filter_input == 'ДА':
            filter_words_salary_from = get_filter_words_salary_from()
            filter_words_salary_to = get_filter_words_salary_to()
            return [filter_words_salary_from, filter_words_salary_to]

        else:
            return []

    def top_n(self):
        """Метод возвращает ответ пользователя """
        return int(input("Введите количество вакансий для вывода: \n"))

    def all_vacancies(self, apis, vacancy_input):

        # Список вакансий с всех заданных платформ пользователем
        all_vacancies = []
        for api_name in apis.keys():
            api = apis.get(api_name)

            vacancies = api.get_vacancies(vacancy_input)
            all_vacancies.extend(vacancies)

        if not all_vacancies:
            raise TypeError("Нет вакансий, соответствующих заданным критериям. Повторите запрос.")
        return all_vacancies

    def comparison_json(self, vacancies, comparison_input):

        if comparison_input == 'ДА' or comparison_input == "":
            comparison_vacancies = ComparisonVacancies()
            comparison_lst = comparison_vacancies.comparison(vacancies)
        else:
            comparison_lst = vacancies
        self.json_saver.add_vacancy(comparison_lst)

    def filter_words_salary_from(self, salary_range_input, top_input):
        if len(salary_range_input) > 0:
            result_list = self.json_saver.get_vacancies_by_salary(int(salary_range_input[0]),
                                                                  int(salary_range_input[1]))
        else:
            delete_vacancy = input("Удалить вакансии, если не указан уровень заработной платы? 'Да'/ 'Нет': \n").upper()
            if delete_vacancy == 'ДА' or delete_vacancy == "":
                result_list = self.json_saver.delete_vacancy_salary()
            else:
                result_list = self.json_saver.get_all()
        return self.json_saver.get_top_vacancies(top_input, result_list)

    def print_result(self, result):
        if result:
            for j, i in enumerate(result):
                print()
                print(
                    f"""{j + 1}. {i.name}\n{i.url}\nУровень заработной платы: {i.salary}\nВид занятости: {i.employment}\n
                    Опыт работы: {i.experience}\nТребования к кандидату: {i.description}""")
        else:
            raise ValueError("Вакансии ао запросу не найдены. Повторите запрос.")

    def start(self):
        apis = self.search_query_api(self.get_platforms_input)
        vacancy_input = self.search_query_vacancies(self.get_query_vacancies)
        comparison_input = self.comparison()
        filter_input = self.filter_words()
        salary_range_input = self.filter_words_salary(filter_input, self.get_filter_words_salary_from, self.get_filter_words_salary_to)
        top_input = self.top_n()

        vacancies = self.all_vacancies(apis, vacancy_input)

        self.comparison_json(vacancies, comparison_input)

        result = self.filter_words_salary_from(salary_range_input, top_input)
        self.print_result(result)


if __name__ == "__main__":
    UserInteraction().start()
