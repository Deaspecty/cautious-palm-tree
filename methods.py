import json
import logging
import re

import coloredlogs
import cv2
import pytesseract
from pyzbar import pyzbar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from entities import Cheque

coloredlogs.install(level="DEBUG")


def image_to_text(filename):
    image_obj = cv2.imread(filename)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    return pytesseract.image_to_string(image_obj, lang="eng+rus", config=r'--oem 3 --psm 6', output_type="dict")


def get_qr_data(filename):
    filename = filename
    img = cv2.imread(filename)  # Считываем файл с изображением
    qrcodes = pyzbar.decode(img)  # Создается список найденных кодов
    return qrcodes


def parse_cheque_site(url):
    options = Options()
    options.add_argument("--headless")
    options.headless = True
    geckodriver_path = '/usr/local/bin/geckodriver'
    # geckodriver_path = 'D:\\PROJECTS\\GECKODRIVER\\geckodriver.exe'

    service = Service(executable_path=geckodriver_path)
    # Создание экземпляра драйвера Firefox
    driver = webdriver.Firefox(options=options, service=service)
    data = {}
    if url.startswith("http://consumer.oofd.kz"):
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/app-root/block-ui/app-search/div/div/div[3]"
                                                      "/div/app-ticket/div/div/div/app-ticket-header")))
        tag_app_ticket_header = driver.find_elements("xpath", "/html/body/app-root/block-ui/app-search/div/div/div[3]"
                                                              "/div/app-ticket/div/div/div/app-ticket-header/*")
        tag_app_ticket_items = driver.find_elements("xpath", "/html/body/app-root/block-ui/app-search/div/div/div[3]"
                                                             "/div/app-ticket/div/div/div/app-ticket-items/*")
        tag_ticket_total = driver.find_elements("class name", "ticket-totals/*")
        data = {
            "tag_app_ticket_header": tag_app_ticket_header,
            "tag_app_ticket_items": tag_app_ticket_items,
            "tag_ticket_total": tag_ticket_total,
            "url": "http://consumer.oofd.kz"
        }
    print(data.__len__())
    return data


def format_data(data):
    cheque_json = {}
    if data.__len__() != 0:
        if data["url"].startswith("http://consumer.oofd.kz"):
            items = []
            tag_ticket_items = data["tag_app_ticket_items"]
            tag_ticket_header = data["tag_app_ticket_header"]
            rows_count = len(tag_ticket_items)
            for row in range(1, rows_count):
                items.append([])
                a_list = tag_ticket_items[row].find_elements(By.XPATH,
                                                             "/html/body/app-root/block-ui/app-search/div/div/div[3]/div/"
                                                             "app-ticket/div/div/div/app-ticket-items/div[2]/div/div[1]/"
                                                             f"div[{row}]/*")
                print(a_list)
                for a in a_list:
                    items[row - 1].append(a.text)

            cheque_json = {
                "column_names": tag_ticket_items[0].text.split("\n"),
                "items": items,
                "no_format_header": tag_ticket_header[0].text
            }
            for row in cheque_json["no_format_header"].split("\n"):
                cheque_json.update(search_in_text(row))
    return cheque_json


class Pattern:
    def __init__(self, startswith, pattern, tag):
        self.startswith = startswith
        self.pattern = pattern
        self.tag = tag

    def check(self, text: str):
        if text.startswith(self.startswith):
            re.search(self.pattern, text).group(1)


def search_in_text(text: str):
    search_patterns = [
        Pattern("ИИН/БИН:", "ИИН/БИН:\s*(\d+)", "iin_bin"),
        Pattern("Сер. номер ККМ:", "Сер. номер ККМ:\s*(\d+)", "kkm"),
        Pattern("Регистрационный номер:", "Регистрационный номер:\s*(\d+)", "reg_num"),
        Pattern("Адрес торговой точки:", "Адрес торговой точки:(.*)", "address"),
        Pattern("Продажа,", "Продажа,(.*)", "sale"),
        Pattern("ФП:", "ФП:(.*)", "fp")
    ]
    found_value = {}
    for pattern in search_patterns:
        if text.startswith(pattern.startswith):
            found_value.update({pattern.tag: re.search(pattern.pattern, text).group(1)})
        # elif re.search("(\d{2}\.\d{2}\.\d{4}) / (\d{2}:\d{2})", text):  # datetime pattern
        #     result = re.search("(\d{2}\.\d{2}\.\d{4}) / (\d{2}:\d{2})", text)
        #     found_value.update({search_patterns[pattern]: result.group(1) + " " + result.group(2)})

    return found_value  # None


def beautifulize_data_one(data: dict):
    text = f"Номер чека: {data['fp']}\n\
Адрес торговой точки: {data['address']}\n\
Оплата: {data['sale']}\n\
\
Товары: \n\
"
    items = data.get("items")
    column_names = data.get("column_names")
    index = {"№": 0}
    for i in range(len(column_names)):
        match column_names[i]:
            case "Название":
                index.update({"name": i})
            case "Цена":
                index.update({"price": i})
            case "Кол-во":
                index.update({"quantity": i})
            case "Сумма":
                index.update({"sum": i})
    for product in items:
        text += f"{product[0]} {product[index['name']]} - " \
                f"{product[index['price']]} * {product[index['quantity']]} = " \
                f"{product[index['sum']]}\n"
    text += f"\nИтого: "
    return text


def beautifulize_data_all(data: dict):
    text = f""
    counter = 1
    for cheque in data:
        if cheque[2] is not None:
            cheque_json = json.loads(cheque[2])
            print(cheque_json)
            items = cheque_json.get("items")
            column_names = cheque_json.get("column_names")
            index = {"№": 0}
            sum = 0
            for i in range(len(column_names)):
                if column_names[i] == "Название":
                    index.update({"name": i})
                elif column_names[i] == "Цена":
                    index.update({"price": i})
                elif column_names[i] == "Кол-во":
                    index.update({"quantity": i})
                elif column_names[i] == "Сумма":
                    print(column_names[i], i)
                    index.update({"sum": i})

            for product in items:
                # text += f"{product[0]} {product[index['name']]} - " \
                #         f"{product[index['price']]} * {product[index['quantity']]} = " \
                #         f"{product[index['sum']]}\n"
                print(product)
                s = product[index['sum']].split(",")[0].replace(" ", "")
                print(s)
                sum += int(s)
            text += f"{counter}. {sum}тг\n"
            counter += 1
    return text
