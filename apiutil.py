import json
import leveldb
import re
import time

from flask import Flask, request
import requests
import hashlib
from urllib.parse import urlencode
from typing import Dict, Any
app = Flask(__name__)
app_id = "2113380860"
app_key = "sbQXRkOEMXyYpQBk"
url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_wordner"

db = leveldb.LevelDB('/db/tencent')


def sign_params(params: Dict[str, Any]) -> Dict[str, Any]:
    items = sorted(params.items(), key=lambda x: x[0])
    sign_str = urlencode(items)
    sign_str += "&app_key=%s" % app_key
    m = hashlib.md5(sign_str.encode()).hexdigest().upper()
    params["sign"] = m
    return params


def postTencentNer(text: str):
    params = {
        "app_id": app_id,
        "time_stamp": int(time.time()),
        "nonce_str": "fa577ce340859f9fe",
        "text": text.encode("gbk",errors="ignore")
    }

    params = sign_params(params)
    resp = requests.post(url, data=params)
    data = resp.json(encoding="utf-8")
    return data

def my_split(str):
    str.replace("\n","。")
    str.replace(" ","")
    result=str.split("。")
    separate_lines = re.split('(.*?[。！])', str)
    lines=[]
    for sep in separate_lines:
        if sep :
            lines.append(sep)
    return lines

def articleNer(content):
    hash = hashlib.sha256()
    hash.update(content.encode())
    id=hash.hexdigest()
    try:
        nerDatas=db.Get(id.encode())
        dataOld = json.loads(nerDatas)
        return dataOld
    except:
        lines=my_split(content)
        groupStr=''
        nerDatas=[]
        for  i in range(len(lines)):
            if len(groupStr) <400 and i<len(lines)-1:
                groupStr+=lines[i]
                continue
            elif len(groupStr) <400 and i==len(lines)-1:
                 groupStr += lines[i]
            data=postTencentNer(groupStr)
            for ner in data["data"]["ner_tokens"]:
                nerDatas.append(ner)
            groupStr = ''
        resultNewl=json.dumps(nerDatas,ensure_ascii=False)
        db.Put(id.encode(),resultNewl.encode())
        return nerDatas
@app.route('/tencent/article',methods=['POST'])
def article():
    data = request.get_data()
    result=json.loads(data,encoding="gbk")
    nerDatas=articleNer(result["text"])
    return json.dumps(nerDatas,ensure_ascii=False)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)