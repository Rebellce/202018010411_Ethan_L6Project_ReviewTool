import json
# -*- coding: utf-8 -*-
import sys
import uuid
import requests
import base64
import hashlib

from imp import reload

import time

reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = '15aad6ef4101a19e'
APP_SECRET = 'RUW1OIAOuMZ0wm3LIbnEdaRbOROrjq4y'


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


def connect():
    f = open(r'E:\University\2023-2024\Semester_1\Pj\MyProject\Implementation\Code\EducatorsAssistant\App\demo\textPic.png', 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['detectType'] = '10012'
    data['imageType'] = '1'
    data['langType'] = 'en'
    data['img'] = q
    data['docType'] = 'json'
    data['signType'] = 'v3'
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
        # 解析JSON格式的响应体
        result = json.loads(response.content.decode('utf-8'))

        # 假设响应结果中的文本数据位于Result -> regions -> lines -> text
        # 按行打印识别结果
        for region in result.get("Result", {}).get("regions", []):
            for line in region.get("lines", []):
                print(line.get("text"))
    else:
        print("请求失败，状态码：", response.status_code)


if __name__ == '__main__':
    connect()
