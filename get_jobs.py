import requests
import os , requests, json
from typing import List, Dict, Any

def find_jobs(job_name: str):
    url = "https://rapid-linkedin-jobs-api.p.rapidapi.com/search-jobs"

    querystring = {"keywords":job_name,
               "experienceLevel":"entryLevel",
               "onsiteRemote":"remote",
               "sort":"mostRelevant"}

    headers = {
	"X-RapidAPI-Key": "c1f10e869bmshc2e01e40e5fddc4p1af6dbjsn57dfdbd7de7a",
	"X-RapidAPI-Host": "rapid-linkedin-jobs-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    with open('realTimeJobSearch.json', 'w') as outfile:
        json.dump(response.json(), outfile)
        
    if (response.status_code == 200):
        return response.json()['data']
    return []

def salaryParser(salary: str) -> float:
    return float('.'.join(salary[:-1]))

def get_highest_salary(salaries: List[Dict[str, Any]]):
    highest_salary = salaries[0]
    for sal in salaries:
        try:
            # print(priceParser(product['offer']['price']))
            # print(product['product_rating'])
            if (salaryParser(sal['bonus']['salary']) > salaryParser(
                    highest_salary['bonus']['salary'])):
                highest_salary = sal
        except:
            pass
    return highest_salary