# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

with open('./lagou_jd.html', 'r') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')
type(soup)
print(soup.title)

