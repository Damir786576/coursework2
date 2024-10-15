from abc import ABC, abstractmethod
import json
import os.path


class JSONVacancy(ABC):
    @abstractmethod
    def safe_vacancy(self, stock_list):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class HHVacancy(JSONVacancy):
    def __init__(self):
        self.file_name_save = "../data/vacancies.json"

    def safe_vacancy(self, stock_list):
        if not stock_list:
            print("Вакансий с такими критериями нет")
            return

        try:
            if os.path.exists(self.file_name_save):
                with open(self.file_name_save, 'r', encoding="utf-8") as file:
                    data = json.load(file)
                data.extend([item for item in stock_list if item not in data])
            else:
                data = stock_list

            with open(self.file_name_save, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Вакансии успешно сохранены в {self.file_name_save}")
        except Exception as e:
            print(f"Ошибка при сохранении вакансий: {e}")

    def delete_vacancy(self):
        if os.path.exists(self.file_name_save):
            try:
                os.remove(self.file_name_save)
                print(f"Файл {self.file_name_save} успешно удален")
            except Exception as e:
                print(f"Ошибка при удалении файла: {e}")
        else:
            print(f"Файл {self.file_name_save} не существует")

