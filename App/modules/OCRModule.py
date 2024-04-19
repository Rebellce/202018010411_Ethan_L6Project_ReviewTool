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
from PyQt5.QtCore import QThread, pyqtSignal

reload(sys)
YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '15aad6ef4101a19e'
APP_SECRET = 'RUW1OIAOuMZ0wm3LIbnEdaRbOROrjq4y'


class OCRThread(QThread):
    finished = pyqtSignal(str, bool)
    OCREngine = "local"
    ui = None

    def __init__(self, OCREngine, ui, parent=None):
        super().__init__(parent)
        self.OCREngine = OCREngine
        self.ui = ui

    def run(self):
        print("OCRThread started")
        if self.OCREngine == "local":
            text, errorFlag = inThreadLocal(self.ui)
            pass
        elif self.OCREngine == "online":
            text, errorFlag = inThreadOnline(self.ui)
            pass
        else:
            assert False, "Unknown OCR engine"
        self.finished.emit(text, errorFlag)


def localOCR(self):
    self.textEditOCRResult.clear()
    self.OCRThread = OCRThread("local", self)
    self.OCRThread.finished.connect(lambda text, errorFlag: _finishOCR(self, text, errorFlag))
    self.OCRThread.start()


def inThreadLocal(ui):
    if ui.image is not None:
        ui.view.activate = False
        ui.view.crop_rect = None
        img = _getIMGObject(ui.pixmap)
        text = pytesseract.image_to_string(img, lang='eng')

        if text:
            errorFlag = False

        else:
            text = "No text recognized!"
            errorFlag = True
    else:
        text = "No image to recognize!"
        errorFlag = True
    return text, errorFlag


def onlineOCR(self):
    self.textEditOCRResult.clear()
    self.OCRThread = OCRThread("online", self)
    self.OCRThread.finished.connect(lambda text, errorFlag: _finishOCR(self, text, errorFlag))
    self.OCRThread.start()


def inThreadOnline(ui):
    if ui.image is not None:
        try:
            ui.view.activate = False
            ui.view.crop_rect = None
            q = _getBase64(ui.pixmap)
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
                    errorFlag = False
                else:
                    text = "No text recognized!"
                    errorFlag = True
            else:
                text = "Online engine error, status code: " + str(response.status_code)
                errorFlag = True

        except requests.exceptions.RequestException as e:
            text = "Network error: " + str(e)
            errorFlag = True

        except ValueError as e:
            text = "Error processing the OCR results: " + str(e)
            errorFlag = True

        except Exception as e:
            text = "An unexpected error occurred: " + str(e)
            errorFlag = True

    else:
        text = "No image to recognize!"
        errorFlag = True
    return text, errorFlag


def _finishOCR(ui, text="", errorFlag=False):
    if errorFlag:
        ui.textEditOCRResult.setHtml(formatError(text))
        ui.OCRSwitch = False
    else:
        ui.textEditOCRResult.setHtml(formatNormal(text))
        ui.OCRSwitch = True
    ui.buttonOCR.setDisabled(False)
    ui.comboBoxInterface.setDisabled(False)


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


def formatNormal(message):
    """Format the normal message with black color using HTML."""
    return f"<p style='color: black;'>{message}</p>"
