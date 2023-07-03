import csv
from dataclasses import dataclass, fields, astuple
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import requests


@dataclass
class Object:
    name: str
    address: str
    phone: str
    site: str
    email: str


BASE_URL = "https://www.google.com/maps/"

OUTPUT_CSV_PATH = "lead_objects.csv"

OBJECT_FIELDS = [field.name for field in fields(Object)]

_driver: WebDriver | None =

# def parse_detail_block(product_soup: BeautifulSoup) ->


def get_detail_page_soup(key_word: str) -> BeautifulSoup:
    starting_page = requests.get(urljoin(BASE_URL, f"search/{key_word}")).content
    objects_soup = BeautifulSoup(starting_page, "html.parser")

    detail_url = objects_soup.select_one(".hfpxzc")["href"]


def parse_single_object(object_soup: BeautifulSoup) -> Object:

    driver = webdriver.Chrome()
    driver.get(detail_url)

    return Object(
        name=object_soup.select_one(".Nv2PK THOPZb CpccDe ")["label"],
        address=driver.find_element(By.CLASS_NAME, "Io6YTe fontBodyMedium kR99db ").text,
        phone=float(object_soup.select_one(".price").text.replace("$", "")),
        site=int(object_soup.select_one("p[data-rating]")["data-rating"]),
        email=int(object_soup.select_one(
            ".ratings > p.pull-right"
        ).text.split()[0])
    )


def get_objects_detail_urls(page_soup: BeautifulSoup) -> [str]:
    objects = page_soup.select(".hfpxzc")

    return [object_soup.select_one(".hfpxzc")["href"] for object_soup in objects]

    # return [parse_single_object(object_soup) for object_soup in objects]


def get_objects(key_word: str) -> [Object]:
    # logging.info("Start parsing laptops")
    page = requests.get(urljoin(BASE_URL, f"search/{key_word}")).content
    first_page_soup = BeautifulSoup(page, "html.parser")

    # get num of pages
    # num_pages = get_num_pages(first_page_soup)

    all_products = get_single_page_products(first_page_soup)

    # for page_num in range(2, num_pages + 1):
    #     # logging.info(f"Start parsing page #{page_num}")
    #     page = requests.get(LAPTOP_URL, {"page": page_num}).content
    #     soup = BeautifulSoup(page, "html.parser")
    #     all_products.extend(get_single_page_products(soup))

    return all_products


def write_products_to_csv(products: [Object]) -> None:
    with open(OUTPUT_CSV_PATH, "w") as file:
        writer = csv.writer(file)
        writer.writerow(OBJECT_FIELDS)
        writer.writerows([astuple(product) for product in products])


def main():
    objects = get_laptop_products(key_word="caffe")
    write_products_to_csv(objects)


if __name__ == '__main__':
    main()

