import logging
import re

import coloredlogs
import cv2
import pytesseract
from pyzbar import pyzbar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

coloredlogs.install()


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
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    data = {}
    if url.startswith("http://consumer.oofd.kz"):
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
    elif url.startswith("https://ofd.beeline.kz"):
        tag_ready_ticket = driver.find_element("class name", "ready_ticket")
        data = {
            "tag_ready_ticket": tag_ready_ticket,
            "url": "https://ofd.beeline.kz"
        }
    print(data)
    return data


def format_data(data):
    cheque_json = {}
    if data["url"].startswith("http://consumer.oofd.kz"):
        items = []
        tag_ticket_items = data["tag_app_ticket_items"]
        tag_ticket_header = data["tag_app_ticket_header"]
        rows_count = len(tag_ticket_items)
        for row in range(1, rows_count):
            items.append(str(tag_ticket_items[row].text).split("\n"))

        cheque_json = {
            "column_names": tag_ticket_items[0].text.split("\n"),
            "items": items,
            "no_format_header": tag_ticket_header[0].text
        }
    elif data["url"].startswith("https://ofd.beeline.kz"):
        data["url"] = "https://ofd.beeline.kz"
    return cheque_json


def search_in_text(text):
    search_patterns = {
        "ИИН/БИН:\s*(\d+)": "iin_bin",
        "Сер. номер ККМ:\s*(\d+)": "kkm",
        "Регистрационный номер:\s*(\d+)": "reg_num",
        "Адрес торговой точки:(.*)": "address",
        "Продажа, (.*)": "sale",
        "ФП: (.*):": "fp",
    }
    found_value = {}
    for pattern in search_patterns:
        if re.search(pattern, text):
            found_value.update({search_patterns[pattern]: re.search(pattern, text).group(1)})
        elif re.search("(\d{2}\.\d{2}\.\d{4}) / (\d{2}:\d{2})", text):  # datetime pattern
            result = re.search("(\d{2}\.\d{2}\.\d{4}) / (\d{2}:\d{2})", text)
            found_value.update({search_patterns[pattern]: result.group(1) + " " + result.group(2)})

    return found_value  # None
