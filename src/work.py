import requests  # Для выполнения HTTP-запросов
import json  # Для работы с JSON
from abc import ABC, abstractmethod


# Абстрактный класс, задающий интерфейс для работы с API вакансий
class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def save_to_file(self, filename):
        pass

    @abstractmethod
    def load_from_file(self, filename):
        pass


# Класс для работы с API hh.ru
class HHJobAPI(JobAPI):
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        self.vacancies = []

    def get_vacancies(self, search_text, area=1, per_page=20):
        params = {"text": search_text, "area": area, "per_page": per_page}
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            self.vacancies = response.json().get('items', [])
        else:
            print("Error fetching data from hh.ru")

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.vacancies = json.load(file)


# Пример использования
hh_api = HHJobAPI()
hh_api.get_vacancies("уборщик")
hh_api.save_to_file("vacancies.json")
