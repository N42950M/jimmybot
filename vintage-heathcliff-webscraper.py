from datetime import datetime, timedelta
import requests
import os
import time
import random

start_date = datetime(1973, 9, 3)

end_date = datetime(1998, 7, 28)

os.chdir("./images")

def date_range(start, end):
    delta = timedelta(days=1)
    while start <= end:
        yield start
        start += delta

for date in date_range(start_date, end_date):
    randomsleep = random.randint(1, 5)
    time.sleep(randomsleep)
    date_str = date.strftime("%Y-%m-%d")
    url = f"https://heathcliff-images.storage.googleapis.com/vintage_heathcliff/{date_str}.png"
    file_name = f"{date.strftime("%Y-%m-%d")}.png"
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        with open("!output.txt", "a") as filee: 
            print(f"File downloaded as '{file_name}'", file=filee)
    else:
        with open("!output.txt", "a") as filee: 
            print(f"Failed to download file {file_name}, status code: {response.status_code}", file=filee)