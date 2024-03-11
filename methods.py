import cv2
import pytesseract
import openai
from openai import OpenAI, AsyncOpenAI

from config import openai_TOKEN


def image_to_text(filename):
    image = cv2.imread(filename)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    return pytesseract.image_to_string(image, lang="rus+eng", config=r'--oem 3')


