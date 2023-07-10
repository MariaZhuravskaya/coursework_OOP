import pytest

import src
from src.main import UserInteraction
from src.utils import SuperJobAPI, HeadHunterAPI

def test_search_query_api():
    user = UserInteraction()
    result = user.search_query_api(lambda: 'HeadHunter, SuperJob')
    assert len(result) == 2
    assert isinstance(result.get("HeadHunter"), HeadHunterAPI)
    assert isinstance(result.get("SuperJob"), SuperJobAPI)

    result = user.search_query_api(lambda: 'SuperJob, HeadHunter')
    assert len(result) == 2
    assert isinstance(result.get("SuperJob"), SuperJobAPI)
    assert isinstance(result.get("HeadHunter"), HeadHunterAPI)

    result = user.search_query_api(lambda: 'HeadHunter')
    assert len(result) == 1
    assert isinstance(result.get("HeadHunter"), HeadHunterAPI)

    result = user.search_query_api(lambda: 'SuperJob')
    assert len(result) == 1
    assert isinstance(result.get("SuperJob"), SuperJobAPI)

def test_search_query_vacancies():
    user = UserInteraction()
    result = user.search_query_vacancies(lambda: 'Java')
    result1 = user.search_query_vacancies(lambda: '')
    assert result == 'Java'
    assert result1 == 'Python'


def test_filter_words_salary():
    user = UserInteraction()
    filter_words_salary_from = lambda: '25000'
    filter_words_salary_to = lambda: '120000'
    result = user.filter_words_salary('ДА', filter_words_salary_from, filter_words_salary_to)
    assert result == ['25000', '120000']
