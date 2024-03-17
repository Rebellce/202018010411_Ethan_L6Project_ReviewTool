from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个 QWebEngineView 小部件
        self.webEngineView = QWebEngineView()

        # HTML5 代码，其中包含 CSS 用于样式化仪表盘
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        * {
  margin: 0;
  padding: 0;
}
body {
  background: transparent;
  display: flex;
  width: 100%%;
  height: 100vh;
  justify-content: center;
  align-items: center;
}
.main {
  width: 60vw;
  height: 60vw;
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
  height: 4vw;
  position: absolute;
  background: var(--sg);
  box-shadow: 0 0 0.5vw var(--sg), 0 0 1vw var(--sg), 0 0 2vw var(--sg);
  transition: 0.8s linear;
}


#pc {
  color: #00aaff; 
  font-size: 8vw;
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

        """ % {"number": 80}

        # 设置 QWebEngineView 小部件显示的内容
        self.webEngineView.setHtml(html_content)

        # 创建一个布局，并将 QWebEngineView 添加进去
        layout = QVBoxLayout()
        layout.addWidget(self.webEngineView)

        # 创建一个容器小部件并设置布局
        container = QWidget()
        container.setLayout(layout)

        # 设置 QMainWindow 的中央小部件
        self.setCentralWidget(container)

        # 显示主窗口
        self.show()


# 创建应用程序实例并运行
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
