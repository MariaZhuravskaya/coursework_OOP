from abc import ABC, abstractmethod
# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os


class APIJob(ABC):

    @abstractmethod
    def get_page(self, vacancies, page_number):
        pass

    @abstractmethod
    def get_vacancies(self, vacancies):
        pass


class JSON(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_all(self):
        pass

    def get_vacancies_by_salary(self, salary_from, salary_to):
        pass


    @abstractmethod
    def get_top_vacancies(self, n, lst):
        pass

    @abstractmethod
    def delete_vacancy_salary(self):
        pass


class SuperJobAPI(APIJob):

    def get_page(self, vacancies, page_number):
        """
        :param vacancies: наименование вакансии (например: "Python разработчик")
        :param page_number: номер страницы просмотра
        :return:
        """
        SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
        relative_url = 'vacancies/'
        headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
        # catalogue_id = 48  # id каталога "Разработка, программирование"
        # town_id = 4  # id города Москва
        vacancies_count = 100
        keyword = vacancies
        url_params = {'page': page_number, 'count': vacancies_count, 'keyword': keyword}

        # Посылаем запрос к API
        response = requests.get('https://api.superjob.ru/2.0/%s' % relative_url, params=url_params, headers=headers)
        data = response.content.decode()
        return json.loads(data)

    def get_vacancies(self, vacancies):
        """
        Получение вакансий с HH.ru по наименованию вакансии
        :param vacancies: наименованию вакансии (например: "Python разработчик")
        :return: Метод возвращает список объектов класса Vacancy в установленном формате
        """
        all_vacancies = []
        first_page = self.get_page(vacancies, 0)
        all_vacancies.extend(first_page['objects'])

        vacancies = []

        for vacancy in all_vacancies:
            name = vacancy['profession'] or ''
            url = vacancy['link'] or ''
            salary = f"{vacancy['payment_from']} - {vacancy['payment_to']}" or 0
            salary_from = vacancy['payment_from'] or 0
            salary_to = vacancy['payment_to'] or 0
            area = vacancy['town']['title'] or ''
            employment = vacancy['type_of_work']['title'] or ''
            experience = vacancy['experience']['title'] or ''
            description = vacancy['candidat'] or ''

            vacancies.append(Vacancy(name, url, salary, salary_from, salary_to, area, employment, experience,
                                     description, "SuperJob"))

        return vacancies


class HeadHunterAPI(APIJob):

    def get_page(self, vacancies, page_number):
        """
        :param vacancies: наименование вакансии (например: "Python разработчик")
        :param page_number: номер страницы просмотра
        :return:
        """
        # Указываем адрес API для подключения в соответствующую переменную:
        API_URL = 'https://api.hh.ru/vacancies'

        params = {
            'text': vacancies,  # Текст фильтра. Какую вакансию ищем
            'area': 1,  # Поиск ощуществляется по вакансиям города Москва
            'page': page_number,  # Индекс страницы поиска на HH
            'per_page': 100  # Кол-во вакансий на 1 странице
        }

        # Посылаем запрос к API
        response = requests.get(API_URL, params)
        # Декодируем его ответ, чтобы Кириллица отображалась корректно
        data = response.content.decode()
        # Преобразуем текст ответа запроса в справочник Python
        return json.loads(data)

    def get_vacancies(self, vacancies):
        """
        Получение вакансий с HH.ru по наименованию вакансии
        :param vacancies: наименованию вакансии (например: "Python разработчик")
        :return: Метод возвращает список объектов класса Vacancy в установленном формате
        """
        all_vacancies = []
        first_page = self.get_page(vacancies, 0)
        all_vacancies.extend(first_page['items'])

        for page_number in range(1, first_page['pages']):
            page = self.get_page(vacancies, page_number)
            all_vacancies.extend(page['items'])

        for vacancy in all_vacancies:
            if isinstance(vacancy['salary'], dict):
                if vacancy['salary']['from'] is not None:
                    vacancy.setdefault('salary_from', vacancy['salary']['from'])
                    if vacancy['salary']['to'] is not None:
                        vacancy.setdefault('salary_to', vacancy['salary']['to'])
                    else:
                        vacancy.setdefault('salary_to', 0)
                else:
                    vacancy.setdefault('salary_from', 0)
                    if vacancy['salary']['to'] is not None:
                        vacancy.setdefault('salary_to', vacancy['salary']['to'])
                    else:
                        vacancy.setdefault('salary_to', 0)
            else:
                vacancy.setdefault('salary_to', 0)
                vacancy.setdefault('salary_from', 0)

        vacancies = []

        for vacancy in all_vacancies:
            name = vacancy['name'] or ''
            url = vacancy['url'] or ''
            salary = f"{vacancy['salary_from']} - {vacancy['salary_to']}"
            salary_from = vacancy['salary_from'] or 0
            salary_to = vacancy['salary_to'] or 0
            area = vacancy['area']['name'] or ''
            employment = vacancy['employment']['name'] or ''
            experience = vacancy['experience']['name'] or ''
            description = vacancy['snippet']['requirement'] or ''

            vacancies.append(Vacancy(name, url, salary, salary_from, salary_to, area, employment, experience,
                                     description, "HeadHunter"))

        return vacancies


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    # __slots__ = ('name', 'url', 'salary', 'area', 'employment', 'salary_from', 'salary_to', 'experience', 'description', 'platform')

    def __init__(self, name: str, url: str, salary: str, salary_from: int, salary_to: int, area: str, employment: str,
                 experience: str, description: str, platform: str):
        """
        :param name: наименование вакансии
        :param url: адрес вакансии
        :param area: город поиска
        :param salary: уровень заработной платы
        :param salary_from: уровень заработной платы от..
        :param salary_to: уровень заработной платы до..
        :param employment: вид занятости
        :param experience: опыт работы
        :param description: требования к кандидату и описание вакансии
        """
        self.name = name
        self.url = url
        self.salary = salary
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.area = area
        self.employment = employment
        self.experience = experience
        self.description = description
        self.platform = platform

    def __setattr__(self, key, value):
        if (key == 'name' and isinstance(value, str)) or (key == 'url' and isinstance(value,
                                                                                      str)) or (
                key == 'salary' and isinstance(
            value, str)) or (key == 'salary_from' and isinstance(
            value, int)) or (key == 'salary_to' and isinstance(
            value, int)) or (key == 'area' and isinstance(value, str)) or (key == 'employment' and isinstance(value,
                                                                                                              str)) or (
                key == 'experience' and isinstance(value,
                                                   str)) or (key == 'description' and isinstance(value,
                                                                                                 str)) or (
                key == 'platform' and isinstance(value,
                                                 str)):
            object.__setattr__(self, key, value)
        else:
            raise AttributeError('Недопустимое значение атрибута')


class ComparisonVacancies:
    """
    Класс для сортирвки экземпляров класса Vacancy
    """

    def comparison(self, vacancies):
        """
        Метод сравнивает экземпляры класса Vacancy по salary_from и
        возвращает отсортированный список по возрастанию
        """
        Vacancy.__eq__ = lambda self, other: self.salary_from == other.salary_from  # ==
        Vacancy.__lt__ = lambda self, other: self.salary_from < other.salary_from  # <
        Vacancy.__le__ = lambda self, other: self.salary_from <= other.salary_from  # <=
        Vacancy.__gt__ = lambda self, other: self.salary_from > other.salary_from  # >
        Vacancy.__ge__ = lambda self, other: self.salary_from >= other.salary_from  # >=
        comparison_vacancies = sorted(vacancies)
        return comparison_vacancies


class VacancyEncoder(json.JSONEncoder):
    """
     Класс позволяющий сериализовать неизвесный энкодеру тип
    """

    def default(self, obj):
        if isinstance(obj, Vacancy):
            attrs = obj.__dict__
            attrs['__type__'] = obj.__class__.__name__
            return attrs
        return json.JSONEncoder.default(self, obj)


def VacancyDecoderFunction(jsonDict):
    """
    Десиреализация json - объекта в пользовательский тип
    """
    if '__type__' in jsonDict and jsonDict['__type__'] == 'Vacancy':
        return Vacancy(
            jsonDict['name'],
            jsonDict['url'],
            jsonDict['salary'],
            jsonDict['salary_from'],
            jsonDict['salary_to'],
            jsonDict['area'],
            jsonDict['employment'],
            jsonDict['experience'],
            jsonDict['description'],
            jsonDict['platform'],
        )
    return jsonDict


class JSONSaver(JSON):
    """
    Класс для сохранения информации о вакансиях в JSON-файл и работы с ним
    """

    def __init__(self):
        """
        Метод создает пустой файл vacancies.json
        """
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps([]))

    def add_vacancy(self, vacancies):
        """
        Метод добавляет найденные вакансии в файл json
        :param vacancy: список обектов класса Vacancy
        """
        all_vacancies = self.get_all()
        all_vacancies.extend(vacancies)

        with open('vacancies.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(all_vacancies, ensure_ascii=False, cls=VacancyEncoder))


    def get_all(self):
        """
        Открываем файл для чтения и выбираем вакансии по зп
        :param salary:
        :return:список вакансий отфильтрованных по ЗП
        """
        with open('vacancies.json', 'r', encoding='utf-8') as file:
            vacancies = json.load(file, object_hook=VacancyDecoderFunction)
        return vacancies

    def get_vacancies_by_salary(self, salary_from, salary_to):
        """
        Метод фильтрует список вакансий по заданным граница ЗП
        :param salary_from: нижнее значение границы ЗП
        :param salary_to: верхнее значение границы ЗП
        :return:список вакансий отфильтрованных по ЗП
        """
        vacancies = self.get_all()
        salary_lst = []

        for s in vacancies:
            if s.salary_from >= salary_from and 0 < s.salary_to <= salary_to:
                salary_lst.append(s)
            else:
                continue
        return salary_lst

    def delete_vacancy_salary(self):
        """
        Метод удаляет вакансии, у которых не указан уровень ЗП
        """
        vacancies = self.get_all()
        minimal = 0
        for vacancy in vacancies:
            if vacancy.salary == '0 - 0':
                vacancies.pop(minimal)
            else:
                None
            minimal = minimal + 1
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(vacancies, ensure_ascii=False, cls=VacancyEncoder))
        return vacancies

    def get_top_vacancies(self, n, lst):
        """
        Метод возвращает заданное колличество вакансий из списка
        :param n: колличество выводимых вакансий пользователю
        :param lst: список объектов
        :return:первые n - объектов
        """
        return lst[:n]




if __name__ == '__main__':
    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()

    superjob_api = SuperJobAPI()

    # Получение вакансий с разных платформ
    hh_vacancies = hh_api.get_vacancies("Python")

    # superjob_vacancies = superjob_api.get_vacancies("Python")

    comparison = ComparisonVacancies()
    hh = comparison.comparison(hh_vacancies)
    # # Создание экземпляра класса для работы с вакансиями
    #
    # # Сохранение информации о вакансиях в файл
    json_saver = JSONSaver()
    json_saver.add_vacancy(hh)
    json_saver.get_vacancies_by_salary("100000 - 150000")
    # json_saver.delete_vacancy(vacancy)

    # superjob_api = SuperJobAPI()
# superjob_vacancies = superjob_api.get_vacancies("Python")
