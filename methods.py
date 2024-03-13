import cv2
import pytesseract
from fuzzywuzzy import process
from keras.preprocessing import image
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np
from pyzbar import pyzbar


def image_to_text(filename):
    image = cv2.imread(filename)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    return pytesseract.image_to_string(image, lang="eng+rus", config=r'--oem 3 --psm 6', output_type="dict")


def get_qr_data(filename):
    filename = filename
    img = cv2.imread(filename)  # Считываем файл с изображением
    qrcodes = pyzbar.decode(img)  # Создается список найденных кодов
    return qrcodes