from datetime import datetime, timedelta
from lxml import html, etree
import requests
import re
import os
import time
import random

start_date = datetime(2002, 1, 2)

current_date = datetime.now()

os.chdir("./images")

def date_range(start, end):
    delta = timedelta(days=1)
    while start <= end:
        yield start
        start += delta


for date in date_range(start_date, current_date):
    randomsleep = random.randint(1, 5)
    time.sleep(randomsleep)
    date_str = date.strftime("%Y/%m/%d")
    url = f"https://www.gocomics.com/heathcliff/{date_str}"
    page = requests.get(url)
    tree = html.fromstring(page.content)
    try: 
        image = etree.tostring((tree.xpath('/html/body/div[1]/div[4]/div[1]/div/div[2]/div[3]/div[1]/div/div[1]/div/a/picture/img'))[0])
    except Exception:
        with open("!output.txt", "a") as filee: 
            print(f"no heathcliff comic for {date_str}", file=filee)
        continue
    link = re.findall(r"http[s]*\S+", image.decode('utf-8'))
    url = link[1]
    file_name = f"{date.strftime("%Y-%m-%d")}.gif"
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        with open("!output.txt", "a") as filee: 
            print(f"File downloaded as '{file_name}'", file=filee)
    else:
        with open("!output.txt", "a") as filee: 
            print(f"Failed to download file {file_name}, status code: {response.status_code}", file=filee)