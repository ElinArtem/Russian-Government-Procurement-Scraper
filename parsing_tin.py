import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

import json
import time

PROXY = {
    "http": "yours proxy",
    "https": "yours proxy",
}

HEADERS = {
    "User-Agent": "yours user agent"
}

# URL of the website
MAIN_URL = "https://zakupki.gov.ru"


# help functions
def connect_json(file_name="all_category.json"):
    print("JSON File conect!")
    with open(file_name, encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_to_file_json(data, file_name: str):
    with open(file_name, "w") as file:
        json.dump(data, file)

    print("File is saved!")


def save_to_file(content, file_name: str):
    with open(file_name, "a", encoding="utf-16") as f:
        f.write(str(content).replace("'", '"'))
    print(f"File '{file_name}' is saved")


# main functions
def get_soup(url, proxy, headers):
    response = requests.get(url, proxies=proxy, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)


def find_cost(soup):
    return (soup.find("span", class_="cardMainInfo__content cost")).text.strip()


def find_name(soup):
    name = (
        soup.find("td", class_="tableBlock__col tableBlock__col_first text-break")
        .text.strip()
        .split("\n")[0]
    )
    return name


def find_tin(soup):
    sections = soup.find_all("section", class_="section")
    for section in sections:
        span_name = section.find("span", class_="grey-main-light")
        if span_name:
            if span_name.text == "ИНН:":
                tin = section.find_all("span")[-1].text

            else:
                tin = None
    return tin


def find_date(soup):
    return (
        soup.find("div", class_="date mt-auto")
        .find("span", class_="cardMainInfo__content")
        .text
    )


def main():
    info = connect_json("result2024.json")
    # Wrap the iteration with tqdm to show a progress bar
    for i in tqdm(range(len(info)), desc="ИНН качается", ncols=100, colour="#D8F2A0"):
        try:
            soup = get_soup(MAIN_URL + info[i].get("url"), PROXY, HEADERS)

            info[i]["url"] = MAIN_URL + info[i].get("url")
            info[i]["tin"] = find_tin(soup)
            info[i]["cost"] = find_cost(soup)
            info[i]["nameSupplier"] = find_name(soup)
            info[i]["date"] = find_date(soup)
        except Exception as e:
            info[i]["url"] = MAIN_URL + info[i].get("url")
            info[i]["tin"] = None
            info[i]["cost"] = None
            info[i]["nameSupplier"] = None
            info[i]["date"] = None
            print(f"Error on {info[i].get('number')}: {e}")
        time.sleep(0.5)

    save_to_file_json(info, "tins2024.json")


if __name__ == "__main__":
    main()

