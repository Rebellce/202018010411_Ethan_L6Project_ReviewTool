from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView


class myGaugeWidget(QWidget):
    def __init__(self, parent=None, number=100, _type="", label="", color=55):
        """
        :param number: show the percentage of the gauge
        :param label: show the title of the gauge
        :param color: range 0~99, (0 is red) rainbow color, special parameter is "i" to show the rainbow color
        """
        super().__init__(parent)
        self.number = number
        self.label = label
        self.color = color
        self.type = _type
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
                  font-size: 12vw;
                  font-weight: bold;
                  font-family: Arial, Helvetica, sans-serif;
                  text-shadow: 0.3vw 0.1vw 0.3vw darkgray, 0 0 0.5vw darkgray, 0 0 1vw darkgray;
                  text-align: center;
                }
                #type {
                    color: #00aaff; 
                    font-size: 12vw;
                    font-weight: bold;
                    font-family: Arial, Helvetica, sans-serif;
                    text-shadow: 0.3vw 0.1vw 0.3vw darkgray, 0 0 0.5vw darkgray, 0 0 1vw darkgray;
                    text-align: center;
                }
                #lab {
                    color: #00aaff; 
                    font-size: 8vw;
                    font-weight: bold;
                    font-family: Arial, Helvetica, sans-serif;
                    text-shadow: 0.3vw 0.1vw 0.3vw darkgray, 0 0 0.5vw darkgray, 0 0 1vw darkgray;
                    text-align: center;
                }

                </style>

                <head>
                    <meta charset="UTF-8">
                </head>

                <body>
                    <div class="main"></div>
                    <label id="range" value=0 step="0.1"/>
                    <p id="pc">0%%</p>
                    <p id="type">%(type)s</p>
                    <p id="lab">%(label)s</p>
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
                            block.style.setProperty('--bg', 'hsl(' + %(color)s / 100 * 360 + ',100%%,50%%)');
                            block.style.setProperty('--sg', 'hsl(' + %(color)s / 100 * 360 + ',100%%,50%%)');
                        }
                    }
                }

                window.onload = function() {
                var initialValue = 0;
                var targetValue = %(number)s; 
                var duration = 1500; 
                var updateInterval = 30; 
                var totalSteps = duration / updateInterval;
                var incrementPerStep = targetValue / totalSteps; 
            
                var interval = setInterval(function() {
                    initialValue += incrementPerStep; 
                    if(initialValue >= targetValue) {
                        initialValue = targetValue;
                        clearInterval(interval); 
                    }
                    var formattedValue = initialValue.toFixed(1); 
                    range.value = formattedValue;
                    range.style.backgroundSize = formattedValue + "%% 100%%";
                    pc.innerHTML = formattedValue + "%%";
                    dash(parseFloat(formattedValue));
                }, updateInterval); 
            };

                </script>

                        """ % {"number": self.number, "color": self.color, "type": self.type, "label": self.label}
        self.webEngineView.setHtml(html_content)

    def refreshGauge(self, number=None, label=None, color=None):
        if number is not None:
            self.number = number
        if label is not None:
            self.label = label
        if color is not None:
            self.color = color
        self.loadContent()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = myGaugeWidget(number=50, _type="GPT", label="Highly likely human", color=50)
    w.show()
    sys.exit(app.exec_())