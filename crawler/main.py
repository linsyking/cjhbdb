#!/usr/bin/env python3
'''
@Author: King
@Date: 2023-05-28 12:23:39
@Email: linsy_king@sjtu.edu.cn
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
from pypinyin import lazy_pinyin

chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

from rich.progress import track


driver.get("https://tieba.baidu.com/f?kw=纯几何")
input("Press enter when you are ready")
data = (
    WebDriverWait(driver, 20)
    .until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="frs_list_pager"]/a[11]'))
    )
    .get_attribute("href")
)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

reg = r'pn=(.*)'
ia = re.compile(reg)
sa = re.findall(ia, data)
maxpage = 0
for x in sa:
    maxpage = int(x)
print("Total page:" + str(maxpage))
list = []

for k in track(range(0, maxpage + 1, 50), description="Processing"):
    driver.get("http://tieba.baidu.com/f?kw=纯几何&ie=utf-8&pn=" + str(k))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    data = (
        WebDriverWait(driver, 20)
        .until(EC.visibility_of_element_located((By.XPATH, '//*[@id="thread_list"]')))
        .get_attribute("innerHTML")
    )
    reg = r'href="/p/(.+?)" title="(.+?)"[\s\S]*?主题作者: (.+?)"'
    ia = re.compile(reg)
    sa = re.findall(ia, data)
    for idx, item in enumerate(sa):
        sa[idx] = {
            "pid": item[0],
            "title": item[1],
            "title_pinyin": "".join(lazy_pinyin(item[1])),
            "title_pinyin_first": "".join([x[0] for x in lazy_pinyin(item[1])]),
            "author": item[2],
            "tags": [],
        }
    list = list + sa

list = sorted(list, key=lambda i: int(i["pid"]))

with open("../public/pb.json", "r", errors="ignore") as f:
    data = json.load(f)

for idx, x in enumerate(list):
    pid = x["pid"]
    for item in data:
        if item['pid'] == pid:
            list[idx]["tags"] = item['tags']
            break

with open("pb.json", "w", errors="ignore") as f:
    json.dump(list, f, ensure_ascii=False, indent=4)
