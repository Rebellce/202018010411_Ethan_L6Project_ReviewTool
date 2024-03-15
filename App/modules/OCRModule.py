import io
from PIL import Image
import pytesseract
from PyQt5.QtCore import QBuffer, QIODevice
import sys
import uuid
import requests
import base64
import hashlib

from imp import reload

import time
import json

reload(sys)
YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '15aad6ef4101a19e'
APP_SECRET = 'RUW1OIAOuMZ0wm3LIbnEdaRbOROrjq4y'


def localOCR(self):
    self.textEditOCRResult.clear()
    if self.image is not None:
        self.view.activate = False
        self.view.crop_rect = None
        img = _getIMGObject(self.pixmap)
        text = pytesseract.image_to_string(img, lang='eng')
        if text:
            self.textEditOCRResult.setText("OCR Result by Local Engine:\n" + text)
        else:
            self.textEditOCRResult.setHtml(formatError("No text recognized!"))
    else:
        self.textEditOCRResult.setHtml(formatError("No image to recognize!"))
    self.buttonOCR.setDisabled(False)
    self.comboBoxInterface.setDisabled(False)


def onlineOCR(self):
    self.textEditOCRResult.clear()

    if self.image is not None:
        try:
            self.view.activate = False
            self.view.crop_rect = None
            q = _getBase64(self.pixmap)
            data = {'detectType': '10012',
                    'imageType': '1',
                    'langType': 'en',
                    'img': q,
                    'docType': 'json',
                    'signType': 'v3'}
            curtime = str(int(time.time()))
            data['curtime'] = curtime
            salt = str(uuid.uuid1())
            signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
            sign = encrypt(signStr)
            data['appKey'] = APP_KEY
            data['salt'] = salt
            data['sign'] = sign

            response = do_request(data)

            if response.status_code == 200:
                result = json.loads(response.content.decode('utf-8'))
                text = ""
                for region in result.get("Result", {}).get("regions", []):
                    for line in region.get("lines", []):
                        text += line.get("text") + "\n"
                if text:
                    self.textEditOCRResult.setText("OCR Result:\n" + text)
                else:
                    self.textEditOCRResult.setHtml(formatError("No text recognized!"))
            else:
                self.textEditOCRResult.setText("Online engine error, status code: " + str(response.status_code))

        except requests.exceptions.RequestException as e:
            error_message = "Network error: " + str(e)
            self.textEditOCRResult.setHtml(formatError(error_message))

        except ValueError as e:
            error_message = "Error processing the OCR results: " + str(e)
            self.textEditOCRResult.setHtml(formatError(error_message))

        except Exception as e:
            error_message = "An unexpected error occurred: " + str(e)
            self.textEditOCRResult.setHtml(formatError(error_message))
    else:
        self.textEditOCRResult.setHtml(formatError("No image to recognize!"))

    self.buttonOCR.setDisabled(False)
    self.comboBoxInterface.setDisabled(False)


def _getIMGObject(pixmap):
    qimage = pixmap.toImage()
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, 'PNG')
    buffer.seek(0)
    IMG = Image.open(io.BytesIO(buffer.data()))
    return IMG


def _getBase64(pixmap):
    qimage = pixmap.toImage()
    buffer = QBuffer()
    buffer.open(QIODevice.WriteOnly)
    qimage.save(buffer, "PNG")
    byte_data = buffer.data()
    buffer.close()
    Base64data = base64.b64encode(byte_data).decode('utf-8')

    return Base64data


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def formatError(message):
    """Format the error message with red color using HTML."""

    return f"<p style='color: red;'>{message}</p>"
