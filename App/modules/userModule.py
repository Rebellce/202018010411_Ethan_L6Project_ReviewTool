import hashlib
import json
import os

from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkCookieJar, QNetworkRequest, QNetworkReply, QNetworkCookie


class UserModule:
    def __init__(self):
        self.cookie = None
        self.manager = None
        self.ui = None
        self.email = ''
        self.firstName = ''
        self.lastName = ''
        self.state = 0  # 0: not logged in, 1: logged in


    def initUser(self, ui):
        self.ui = ui
        self.manager = QNetworkAccessManager(ui)
        self.cookie = QNetworkCookieJar()
        self.manager.setCookieJar(self.cookie)

    def register(self, data):
        request = QNetworkRequest(QUrl("http://localhost:5000/register"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        reply = self.manager.post(request, QByteArray(bytes(json.dumps(data), 'utf-8')))
        reply.finished.connect(self.responseRegister)

    def responseRegister(self):
        reply = self.manager.sender()
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        if reply.error() == QNetworkReply.NoError:
            response = json.loads(str(reply.readAll(), 'utf-8'))
            message = response['message']
            self.getUser()

        elif statusCode == 400:
            message = "User already exists!"
        else:
            print("Error:", reply.errorString())
            statusCode = -1
            message = "Something wrong..Try again later."
        reply.deleteLater()
        self.ui.responseRegister(message, statusCode)

    def login(self, data):
        request = QNetworkRequest(QUrl("http://localhost:5000/login"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        reply = self.manager.post(request, QByteArray(bytes(json.dumps(data), 'utf-8')))
        reply.finished.connect(self.responseLogin)

    def responseLogin(self):
        reply = self.manager.sender()
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        if reply.error() == QNetworkReply.NoError:
            response = json.loads(str(reply.readAll(), 'utf-8'))
            message = response['message']
            self.getUser()
        elif statusCode == 400:
            message = "Invalid credentials!"
        else:
            print("Error:", reply.errorString())
            if statusCode is None:
                message = f"Something wrong.. (NoServerResponse)"
            else:
                message = f"Something wrong.. ({statusCode})"
            statusCode = -1
        reply.deleteLater()
        self.ui.responseLogin(message, statusCode)

    def getUser(self):
        request = QNetworkRequest(QUrl("http://localhost:5000/getUser"))
        reply = self.manager.get(request)
        reply.finished.connect(self.responseGetUser)

    def responseGetUser(self):
        reply = self.manager.sender()
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        if reply.error() == QNetworkReply.NoError:
            response = json.loads(str(reply.readAll(), 'utf-8'))
            self.email = response['email']
            self.firstName = response['firstName']
            self.lastName = response['lastName']
            self.state = 1
            self.ui.jumpToUserLoggedIn()
            self.saveCookies()
        else:
            print("Error:", reply.errorString())
            self.email = self.firstName = self.lastName = ""
            self.state = 0
            self.ui.tabUser.setDisabled(False)
        reply.deleteLater()

    def logout(self):
        request = QNetworkRequest(QUrl("http://localhost:5000/logout"))
        reply = self.manager.get(request)
        reply.finished.connect(self.responseLogout)

    def responseLogout(self):
        reply = self.manager.sender()
        reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        self.email = self.firstName = self.lastName = ""
        self.state = 0
        if reply.error() != QNetworkReply.NoError:
            self.logout()
        else:
            self.ui.responseLogout()
            self.clearCookies()
        reply.deleteLater()

    def saveCookies(self, filename="cookies.dat"):
        cookies = self.cookie.allCookies()
        with open(filename, 'wb') as file:
            for cookie in cookies:
                file.write(bytes(cookie.toRawForm()) + b'\n')

    def loadCookies(self, filename="cookies.dat"):
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as file:
                    cookies = []
                    for line in file:
                        cookie = QNetworkCookie.parseCookies(line.strip())
                        if cookie:
                            cookies.extend(cookie)
                    self.cookie.setAllCookies(cookies)
                    self.manager.setCookieJar(self.cookie)
                    print("Cookies loaded successfully!")
            except Exception as e:
                print("Error:", e)
                return False
            return True

        else:
            return False

    def clearCookies(self, filename="cookies.dat"):
        if os.path.exists(filename):
            os.remove(filename)




def getSha256(rawData):
    return hashlib.sha256(rawData.encode('utf-8')).hexdigest()


def verifySha256(toVerifyData, givenSha256):
    serverSha256 = getSha256(toVerifyData)
    return serverSha256 == givenSha256


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
    from PyQt5.QtCore import QUrl, QByteArray
    from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


    class App(QWidget):
        def __init__(self):
            super().__init__()
            self.user = UserModule()
            self.user.initUser(self)

        def init_ui(self):
            self.setGeometry(300, 300, 300, 220)
            self.setWindowTitle('Login App')

            layout = QVBoxLayout(self)
            self.username_edit = QLineEdit(self, placeholderText="Enter username")
            self.password_edit = QLineEdit(self, placeholderText="Enter password")
            self.password_edit.setEchoMode(QLineEdit.Password)

            login_button = QPushButton('Login', self)
            login_button.clicked.connect(self.user.connectTest)

            layout.addWidget(self.username_edit)
            layout.addWidget(self.password_edit)
            layout.addWidget(login_button)


    app = QApplication(sys.argv)
    ex = App()
    ex.init_ui()
    ex.show()
    sys.exit(app.exec_())
