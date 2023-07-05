from __future__ import annotations

import time

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# from leads.models import Lead


_driver: WebDriver | None = None

def set_driver(new_driver: WebDriver) -> None:
    global _driver
    _driver = new_driver

def get_driver() -> WebDriver:
    return _driver


def get_elements_by_key_word(key_word: str, location: str) -> [WebElement]:
    driver = get_driver()
    location = location.replace(" ", "+")
    driver.get(f"https://www.google.com/maps/search/{key_word}+{location}/")
    driver.fullscreen_window()
    elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    # for elem in elements:
    #     elem.click()

    # Wait for the page to load
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))

    # search_box = driver.find_element(By.ID, "searchboxinput")
    # search_box.send_keys(f"{key_word} {location}")
    # search_box.submit()

    # Wait for the search results to load
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "section-result")))

    # Extract the required information for each result
    results = driver.find_elements(By.CLASS_NAME, "hfpxzc")

    return results


def get_email_and_website(element) -> [str]:
    email_element = element.find_element(By.CLASS_NAME, "section-result-info-container")
    email_link = email_element.find_element(By.TAG_NAME, "a") if email_element else None
    email = email_link.text if email_link and "@" in email_link.text else ""

    website_element = element.find_element(
        By.CLASS_NAME, "section-result-action-button"
    ).get_attribute("href")
    website = website_element if website_element else ""

    if not email:
        if not website:
            email = ""
        else:
            pass

    return [email, website]


# def get_lead_instances(elements: [WebElement]) -> [Lead]:
#     data = []
#
#     for element in elements:
#         # item = {}
#         email_website = get_email_and_website(element)
#         lead_item = Lead(
#             name=element.find_element(
#                 By.CLASS_NAME, "section-result-title"
#             ).text,
#             full_address=element.find_element(
#                 By.CLASS_NAME, "section-result-location"
#             ).text,
#             phone_number=element.find_element(
#                 By.CLASS_NAME, "section-result-phone-number"
#             ).get_attribute("aria-label"),
#             website=email_website[1],
#             email=email_website[0],
#         )
#
#         data.append(lead_item)
#
#     return data


if __name__ == '__main__':
    with webdriver.Chrome() as new_driver:
        set_driver(new_driver)
        result = get_elements_by_key_word("кафе", "Кривий Ріг")
        print(result, len(result))

