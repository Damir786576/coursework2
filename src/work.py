import requests
import json
from abc import ABC, abstractmethod
from src.api import base_url


class Job:
    def __init__(self, title, url, pay, desc, firm):
        self.title = title
        self.url = url
        self.pay = pay
        self.desc = desc
        self.firm = firm

    def __str__(self):
        pay_str = self.pay if self.pay else "Not specified"
        return f"{self.title} at {self.firm}\nPay: {pay_str}\nDesc: {self.desc}\nURL: {self.url}"

    def __lt__(self, other):
        return self.comp_pay() < other.comp_pay()

    def comp_pay(self):
        if not self.pay:
            return 0
        if isinstance(self.pay, (int, float)):
            return self.pay
        return sum(self.pay) / 2  # Use average for range


class API(ABC):
    @abstractmethod
    def get_jobs(self, query, area=1, limit=20):
        pass

    @abstractmethod
    def save_json(self, filename):
        pass


def parse_pay(pay_data):
    if not pay_data:
        return 0
    from_pay = pay_data.get('from')
    to_pay = pay_data.get('to')
    return (from_pay, to_pay) if from_pay and to_pay else from_pay or to_pay or 0


class HHAPI(API):
    def __init__(self):
        self.jobs = []

    def get_jobs(self, query, area=1, limit=20):
        params = {"text": query, "area": area, "per_page": limit}
        resp = requests.get(base_url, params=params)
        if resp.status_code == 200:
            data = resp.json().get('items', [])
            self.jobs = [self.parse_job(item) for item in data]
        else:
            print(f"Error fetching data: Status code {resp.status_code}")
        return self.jobs

    @staticmethod
    def parse_job(item):
        title = item.get('name')
        url = item.get('alternate_url')
        pay = parse_pay(item.get('salary'))
        desc = item.get('snippet', {}).get('requirement', 'No description')
        firm = item.get('employer', {}).get('name', 'Unknown')
        return Job(title, url, pay, desc, firm)

    def save_json(self, filename):
        job_data = [
            {
                "title": j.title,
                "firm": j.firm,
                "pay": j.pay,
                "desc": j.desc,
                "url": j.url
            } for j in self.jobs
        ]

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(job_data, file, ensure_ascii=False, indent=4)
        print(f"Jobs saved to {filename}")

    def sort_jobs(self):
        self.jobs.sort(reverse=True)


if __name__ == '__main__':
    # Initialize the API with the base URL
    api = HHAPI()

    # Fetch jobs for Python Developers
    print("Fetching jobs for Python Developers...")
    jobs = api.get_jobs("Python Developer", area=1, limit=50)

    print(f"Found {len(jobs)} jobs")

    # Sort jobs by pay (highest to lowest)
    print("Sorting jobs by pay...")
    api.sort_jobs()

    # Save all jobs to a JSON file
    out_file = "../data/vacancies.json"
    print(f"Saving all jobs to {out_file}...")
    api.save_json(out_file)
