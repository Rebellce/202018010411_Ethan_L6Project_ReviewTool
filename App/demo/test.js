//         html_content = """
//         <!DOCTYPE html>
//         <html>
//         <head>
//         <style>
//         * {
//   margin: 0;
//   padding: 0;
// }
// body {
//   background: #333;
//   display: flex;
//   width: 100%;
//   height: 100vh;
//   justify-content: center;
//   align-items: center;
// }
// .main {
//   width: 40vw;
//   height: 40vw;
//   position: absolute;
//   display: flex;
//   justify-content: start;
//   align-items: center;
// }
// .main span {
//   --bg: black;
//   --sg: transparent;
//   position: absolute;
//   width: 100%;
//   height: 100%;
//   display: flex;
//   justify-content: center;
//   align-items: start;
// }
// .main span::after {
//   content: "";
//   width: 0.5vw;
//   height: 2vw;
//   position: absolute;
//   background: var(--sg);
//   box-shadow: 0 0 0.5vw var(--sg), 0 0 1vw var(--sg), 0 0 2vw var(--sg);
//   transition: 0.8s linear;
// }
// input[type="range"] {
//   --c: #1e90ff;
//   width: 40vw;
//   height: 1vw;
//   position: absolute;
//   transform: translateY(25vw);
//   appearance: none;
//   background: linear-gradient(var(--c), var(--c)) no-repeat, black;
//   background-size: 0 100%;
//   border-radius: 0.5vw;
// }
// input[type="range"]::-webkit-slider-thumb {
//   appearance: none;
//   width: 2vw;
//   height: 2vw;
//   background: var(--c);
//   border-radius: 50%;
//   box-shadow: 0 0 1vw white, 0 0 2vw white;
// }
// #pc {
//   color: white;
//   font-size: 10vw;
//   font-family: Arial, Helvetica, sans-serif;
//   text-shadow: 0.2vw 0.2vw 0 gray, 0 0 1vw #1e90ff, 0 0 2vw #1e90ff,
//     0 0 4vw #1e90ff;
// }
//
//         </style>
//
// <head>
//     <meta charset="UTF-8">
//     <meta http-equiv="X-UA-Compatible" content="IE=edge">
//     <meta name="viewport" content="width=device-width, initial-scale=1.0">
//     <link rel="stylesheet" href="style.css">
//     <script src="script.js" defer></script>
//     <title>Document</title>
// </head>
//
// <body>
//     <div class="main"></div>
//     <input type="range" id="range" value=0 step="0.1">
//     <p id="pc">0%</p>
// </body>
//
// </html>
// <script>
// var main = document.getElementsByClassName("main")[0];
// var range = document.getElementById("range");
// var pc = document.getElementById("pc");
//
// // 创建span元素，并设置它们的初始变换
// for (var i = 0; i < 100; i++) {
//     var span = document.createElement("span");
//     span.style.transform = "rotate(" + (360 - i / 100 * 360) + "deg)";
//     main.appendChild(span);
// }
//
// // 定义一个函数，根据滑块的值来渲染颜色
// function dash(val) {
//     for (var i = 0; i < main.children.length; i++) {
//         var block = main.children[i];
//         if (i >= val) {
//             block.style.setProperty('--bg', 'black');
//             block.style.setProperty('--sg', 'transparent');
//         }
//         else {
//             block.style.setProperty('--bg', 'hsl(' + 50 / 100 * 360 + ',100%,50%)');
//             block.style.setProperty('--sg', 'hsl(' + 50 / 100 * 360 + ',100%,50%)');
//         }
//     }
// }
//
// // 监听滑块的输入事件，并更新颜色和文本
// range.addEventListener("input", function () {
//     var value = parseFloat(range.value).toFixed(1); // 转换为浮点数并保留1位小数
//     range.style.backgroundSize = value + "% 100%";
//     pc.innerHTML = value + "%"; // 显示保留1位小数的值
//     dash(parseFloat(value));
// });
//
// // 页面加载时缓慢增加滑块的值到50
// window.onload = function() {
//     var initialValue = 0;
//     var targetValue = 50; // 目标值
//     var interval = setInterval(function() {
//         initialValue += 0.1; // 以0.1为增量
//         var formattedValue = initialValue.toFixed(1); // 保留1位小数
//         range.value = formattedValue;
//         range.style.backgroundSize = formattedValue + "% 100%";
//         pc.innerHTML = formattedValue + "%";
//         dash(parseFloat(formattedValue));
//
//         if(initialValue >= targetValue) {
//             clearInterval(interval); // 当达到目标值时停止
//         }
//     }, 1); // 每20毫秒增加0.1，你可以调整这个速度
// }
// </script>
//
//         """