import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

import json

PROXY = {
    "http": "yours proxy",
    "https": "yours proxy",
}

HEADERS = {
    "User-Agent": "yours user agent"
}

# URL of the website
MAIN_URL = "https://zakupki.gov.ru"


def save_to_file_json(data, file_name: str):
    with open(file_name, "w") as file:
        json.dump(data, file)

    print("File is saved!")


def get_soup(url, proxy, headers):
    response = requests.get(url, proxies=proxy, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


def url_contracts(soup):
    contracts = soup.find_all("div", class_="registry-entry__header-mid__number")
    result = []
    for contract in contracts:

        info = contract.find("a")
        result.append(
            {
                "url": info["href"],
                "number": info.text.strip(),
            }
        )
    return result


def main():
    results = []
    for _ in tqdm(range(0, 1), desc="TINs are bein' downloaded", ncols=100, colour="#D8F2A0"):
        url = f"https://zakupki.gov.ru/epz/contract/search/results.html?searchString=подшипники&morphology=on&search-filter=Дате+размещения&fz44=on&contractStageList_0=on&contractStageList_1=on&contractStageList_2=on&contractStageList_3=on&contractStageList=0%2C1%2C2%2C3&budgetLevelsIdNameHidden=%7B%7D&contractDateFrom=01.01.2024&sortBy=RELEVANCE&pageNumber=1&sortDirection=false&recordsPerPage=_100&showLotsInfoHidden=false"
        soup = get_soup(url, PROXY, HEADERS)
        results.append(url_contracts(soup))

    save_to_file_json(results, "result2024.json")
    pass


if __name__ == "__main__":
    main()
