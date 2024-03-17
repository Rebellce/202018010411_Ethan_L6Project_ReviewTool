from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


class myGaugeWidget(QWidget):
    def __init__(self, parent=None, number=100):
        super().__init__(parent)
        self.number = number
        self.initUI()

    def initUI(self):
        self.webEngineView = QWebEngineView()
        self.loadContent()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.webEngineView)
        self.setLayout(layout)

    def resizeEvent(self, event, *args, **kwargs):
        size = min(self.width(), self.height())
        self.resize(size, size)  #

    def sizeHint(self):
        return QSize(200, 200)

    def loadContent(self):
        html_content = """
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <style>
                        * {
                  margin: 0;
                  padding: 0;
                  overflow: hidden;
                }
                body, html {
                width: 100%%;
                height: 100%%;
                overflow: hidden;
        }
                body {
                  background: Transparent;
                  display: flex;
                  width: 100%%;
                  height: 100vh;
                  justify-content: center;
                  align-items: center;
                }
                .main {
                  width: 95%%;
                  height: 95%%;
                  position: absolute;
                  display: flex;
                  justify-content: start;
                  align-items: center;
                }
                .main span {
                  --bg: black;
                  --sg: transparent;
                  position: absolute;
                  width: 100%%;
                  height: 100%%;
                  display: flex;
                  justify-content: center;
                  align-items: start;
                }
                .main span::after {
                  content: "";
                  width: 2vw;
                  height: 6vw;
                  position: absolute;
                  background: var(--sg);
                  box-shadow: 0 0 0.5vw var(--sg), 0 0 1vw var(--sg), 0 0 2vw var(--sg);
                  transition: 0.8s linear;
                }


                #pc {
                  color: #00aaff; 
                  font-size: 15vw;
                  font-weight: bold;
                  font-family: Arial, Helvetica, sans-serif;
                  text-shadow: 0.3vw 0.1vw 0.3vw darkgray, 0 0 0.5vw darkgray, 0 0 1vw darkgray;
                }


                        </style>

                <head>
                    <meta charset="UTF-8">
                </head>

                <body>
                    <div class="main"></div>
                    <label id="range" value=0 step="0.1"/>
                    <p id="pc">0%%</p>
                </body>

                </html>
                <script>
                var main = document.getElementsByClassName("main")[0];
                var range = document.getElementById("range");
                var pc = document.getElementById("pc");

                for (var i = 0; i < 100; i++) {
                    var span = document.createElement("span");
                    span.style.transform = "rotate(" + (360 - i / 100 * 360) + "deg)";
                    main.appendChild(span);
                }


                function dash(val) {
                    for (var i = 0; i < main.children.length; i++) {
                        var block = main.children[i];
                        if (i >= val) {
                            block.style.setProperty('--bg', 'black');
                            block.style.setProperty('--sg', 'transparent');
                        }
                        else {
                            block.style.setProperty('--bg', 'hsl(' + 55 / 100 * 360 + ',100%%,50%%)');
                            block.style.setProperty('--sg', 'hsl(' + 55 / 100 * 360 + ',100%%,50%%)');
                        }
                    }
                }

                window.onload = function() {
                    var initialValue = 0;
                    var targetValue = %(number)s; 
                    var interval = setInterval(function() {
                        initialValue += 0.2; 
                        var formattedValue = initialValue.toFixed(1); 
                        range.value = formattedValue;
                        range.style.backgroundSize = formattedValue + "%% 100%%";
                        pc.innerHTML = formattedValue + "%%";
                        dash(parseFloat(formattedValue));

                        if(initialValue >= targetValue) {
                            clearInterval(interval); 
                        }
                    }, 1); 
                }
                </script>

                        """ % {"number": self.number}
        self.webEngineView.setHtml(html_content)

    def refreshGauge(self, number=None):
        if number is not None:
            self.number = number
        self.loadContent()
