from src.work import HHAPI


def interact_with_user():
    api = HHAPI()

    while True:
        # Step 1: Ask for job search query
        query = input("Введите место работы (или «exit», чтобы выйти из приложения): ")
        if query.lower() == 'exit':
            print("Спасибо за использование. До свидания!")
            break

        # Fetch jobs and sort them
        try:
            jobs = api.get_jobs(query)
            api.sort_jobs()
        except Exception as e:
            print(f"Произошла ошибка {e}")
            continue

        # Step 2: Display top 5 jobs by salary
        print("Top 5 jobs by salary:")
        for job in api.jobs[:5]:
            print(f'{job}\n')

        # Step 3: Ask for keyword to search in descriptions
        keyword = input("Введите ключевое слово для поиска в описаниях вакансий: ").lower()
        matching_jobs = [job for job in api.jobs if keyword in job.desc.lower()]
        if len(matching_jobs) == 0:
            print("По данному описанию ничего не найдено")
        for job in matching_jobs:
            print(f'{job}\n')

        # Step 4: Save all jobs to JSON file
        filename = "../data/vacancies.json"
        api.save_json(filename)


if __name__ == "__main__":
    interact_with_user()
