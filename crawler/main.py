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

# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

CURRENT_YEAR = "2023"
CURRENT_MONTH = "05"

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

maxpage = 0

for k in track(range(0, maxpage + 1, 50), description="Processing"):
    driver.get("http://tieba.baidu.com/f?kw=纯几何&ie=utf-8&pn=" + str(k))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    data = (
        WebDriverWait(driver, 20)
        .until(EC.visibility_of_element_located((By.XPATH, '//*[@id="thread_list"]')))
        .get_attribute("innerHTML")
    )
    reg = r'href="/p/(.+?)" title="(.+?)".*?j_th_tit[\s\S]*?主题作者: (.+?)"[\s\S]*?创建时间">(.+?)<'
    ia = re.compile(reg)
    sa = re.findall(ia, data)
    for idx, item in enumerate(sa):
        date = item[3]
        if len(date) <= 5:
            if date.find(":") != -1:
                # TODAY
                date = f"{CURRENT_YEAR}-{CURRENT_MONTH}"
            else:
                res = re.findall(re.compile(r"([0-9]+?)-"), data)
                month = res[0][0]
                if len(month) == 1:
                    month = "0" + month
                date = f"{CURRENT_YEAR}-{month}"
        sa[idx] = {
            "pid": item[0],
            "title": item[1],
            "title_pinyin": "".join(lazy_pinyin(item[1])),
            "title_pinyin_first": "".join([x[0] for x in lazy_pinyin(item[1])]),
            "author": item[2],
            "date": date,
            "tags": [],
        }
    list = list + sa

list = sorted(list, key=lambda i: int(i["pid"]))

# 判断新帖子


with open("pb.html", "r", errors="ignore") as f:
    nhtml = f.read()

reg = r'/p/(.*?)"[\s\S]*?<td>\| (.*?) \| </td>'
ia = re.compile(reg)
taglist = re.findall(ia, nhtml)

for idx, x in enumerate(list):
    pid = x["pid"]
    fres = nhtml.find(pid)
    if fres != -1:
        # 判断是否有tag
        flag = 0
        thistag = ""
        for tag in taglist:
            if tag[0] == pid:
                flag = 1
                thistag = tag[1].split("|")
                break
        if flag == 1:
            # tag
            res = [re.findall(re.compile(r".*>(.*?)<"), x)[0] for x in thistag]
            list[idx]["tags"] = res
            continue

with open("pb.json", "w", errors="ignore") as f:
    json.dump(list, f, ensure_ascii=False, indent=4)
