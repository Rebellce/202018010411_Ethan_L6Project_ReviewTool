from PIL import Image, ImageFilter, ImageEnhance
import pytesseract

# 打开图像文件
image_path = 'textPic.png'
image = Image.open(image_path)


# 使用更详细的OCR引擎模式和页面分割模式
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(image, config=custom_config, lang='eng')


print("识别到的文字：")
print(text)
