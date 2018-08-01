# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

with open('./tmp.html', 'r') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')

title = soup.title.text
company_name = soup.find('div', class_='company').text
position = soup.find('span', class_='name').text

print('company_nam:', company_name)
print('position:', position)

salary = soup.find('span', class_='salary').text
print('salary:', salary)

position_label = soup.find_all('li', class_='labels')
position_label = [lb.text for lb in position_label]
print('position_label', position_label)

job_request = soup.find('dd', class_='job_request')
job_request = job_request.text.split('\n')[3:7]
print('job_request', job_request)

job_advantage = soup.find('dd', class_='job-advantage').text
print(job_advantage)

job_description = soup.find('dd', class_='job_bt').text
print(job_description)

work_add = soup.find('div', class_='work_addr').text.replace('\n',' ')
work_add = re.sub(r'\s', '', work_add[:-1])
print('work_add:', work_add)

review_anchor = soup.find('a', class_='checkAll').get('href')
print('review_anchor:', review_anchor)


job_company = soup.find('h2', class_='fl').text
job_company = re.sub(r'\s', '', job_company.replace(soup.find('span', class_='dn').text, ''))
print(job_company)

company = soup.find('ul', class_='c_feature').text
company = [re.sub(r'\s', '',cy) for cy in company.split('\n') if cy]
print(company[0], company[2], company[4], company[6])
# company = re.sub(r'\s', ' ', company)
# print(company)