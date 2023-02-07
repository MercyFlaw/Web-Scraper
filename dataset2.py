from selenium import webdriver
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
from urllib.request import Request, urlopen
import asyncio
from requests_html import AsyncHTMLSession
import time


with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines()]

prompt_list = []
text_list = []


async def generate(client,url):
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    response = await client.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup.find('title')) 
    for tags in soup.find_all('h2'):
        qs = ['how','why','what','when','where','who']
        tag = tags.text.strip()
        prompt = tag.lower()
        if prompt[-1] == "?" or any(item for item in qs if(item in prompt)):
            try:
                p = tags.find_next('p').text.strip()
                prompt_list.append(tag)
                text_list.append(p)
            except:
                print("ERROR")
                pass
    return 0

async def main(urls):
    client = AsyncHTMLSession()
    tasks = (generate(client,url) for url in urls)

    return await asyncio.gather(*tasks)

start = time.perf_counter()
results = asyncio.run(main(urls))
print(results)
finish = time.perf_counter() - start
print(finish)

dict = {'PROMPT': prompt_list, 'TEXT': text_list}
df = pd.DataFrame(dict)
to_csv = df.to_csv("D:\Workspace\chatGPT\data4.csv")
