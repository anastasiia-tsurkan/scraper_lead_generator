import csv
from __future__ import annotations
from dataclasses import dataclass, fields, astuple
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
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

_driver: WebDriver | None = None


def get_driver() -> WebDriver:
    return _driver


def set_driver(new_driver: WebDriver) -> None:
    global _driver
    _driver = new_driver

# def parse_detail_block(product_soup: BeautifulSoup) ->


def get_detail_page_soup(url: str) -> BeautifulSoup:
    obj_detail = requests.get(urljoin(BASE_URL, url)).content
    return BeautifulSoup(obj_detail, "html.parser")


def parse_single_object(page_soup: BeautifulSoup) -> Object:

    url = get_objects_detail_urls(page_soup)
    object_soup = get_detail_page_soup(url)

    return Object(
        name=object_soup.select_one(".Nv2PK THOPZb CpccDe ")["label"],
        address=object_soup.select_one("Io6YTe fontBodyMedium kR99db ").text,
        phone=object_soup.select_one(""),
        site=int(object_soup.select_one("p[data-rating]")["data-rating"]),
        email=int(object_soup.select_one(
            ".ratings > p.pull-right"
        ).text.split()[0])
    )


def get_objects_detail_urls(page_soup: BeautifulSoup) -> [str]:
    objects = page_soup.select(".hfpxzc")

    return [object_soup.select_one(".hfpxzc")["href"] for object_soup in objects]


def get_objects(key_word: str) -> [Object]:
    page = requests.get(urljoin(BASE_URL, f"search/{key_word}")).content
    page_soup = BeautifulSoup(page, "html.parser")

    parse_single_object(page_soup)

    # for page_num in range(2, num_pages + 1):
    #     # logging.info(f"Start parsing page #{page_num}")
    #     page = requests.get(LAPTOP_URL, {"page": page_num}).content
    #     soup = BeautifulSoup(page, "html.parser")
    #     all_products.extend(get_single_page_products(soup))

    return all_objects


def write_objects_to_csv(objects: [Object]) -> None:
    with open(OUTPUT_CSV_PATH, "w") as file:
        writer = csv.writer(file)
        writer.writerow(OBJECT_FIELDS)
        writer.writerows([astuple(obj) for obj in objects])


def main():
    objects = get_objects(key_word="caffe")
    write_objects_to_csv(objects)


if __name__ == '__main__':
    main()

