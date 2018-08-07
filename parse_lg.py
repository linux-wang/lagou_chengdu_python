# -*- coding: utf-8 -*-
import json
import logging
import logging.config
import random
import re

from bs4 import BeautifulSoup
from selenium import webdriver

from db import *

# logger
logging.config.fileConfig('./log.conf')
info_logger = logging.getLogger('info')
error_logger = logging.getLogger('error')
warn_logger = logging.getLogger('root')


# get job_links
def get_job_list(content):
    soup_c = BeautifulSoup(content, 'lxml')

    job_links = soup_c.find_all('a', class_='position_link')
    job_links = [jl.get('href') for jl in job_links]
    for jl in job_links:
        info_logger.info('get job_link: ' + jl)

    return job_links


def get_job_info(content, job_id):
    soup = BeautifulSoup(content, 'lxml')

    title = soup.title.text
    company_name = soup.find('div', class_='company').text
    position = soup.find('span', class_='name').text
    salary = soup.find('span', class_='salary').text

    position_label = soup.find_all('li', class_='labels')
    position_label = [lb.text for lb in position_label]

    job_request = soup.find('dd', class_='job_request').text.split('\n')[3:7]
    job_request = [jr.replace('/', '') for jr in job_request]
    city = job_request[0]
    work_experience = job_request[1]
    education = job_request[2]
    full_or_part = job_request[3]

    job_advantage = soup.find('dd', class_='job-advantage').text.replace('职位诱惑：', '')
    job_description = soup.find('dd', class_='job_bt').text

    work_add = soup.find('div', class_='work_addr').text.replace('\n', ' ')
    work_add = re.sub(r'\s', '', work_add[:-1])[:-4]

    review_anchor = soup.find('a', class_='checkAll').get('href')

    job_company = soup.find('h2', class_='fl').text
    job_company = re.sub(r'\s', '', job_company.replace(soup.find('span', class_='dn').text, ''))

    company = soup.find('ul', class_='c_feature').text
    company = [re.sub(r'\s', '', cy) for cy in company.split('\n') if cy]
    company_id = review_anchor.split('=')[-1]

    job_info = {
        'job_id': int(job_id),
        'company_id': int(company_id),
        'company_name': company_name,
        'position': position,
        'salary': salary,
        'position_label': ','.join(position_label),
        'city': city,
        'work_experience': work_experience,
        'education': education,
        'full_or_part': full_or_part,
        'job_advantage': job_advantage,
        'job_description': job_description,
        'work_add': work_add,
        'review_anchor': review_anchor
    }
    company_info = {
        'id': int(company_id),
        'name': job_company,
        'zone': company[0],
        # TODO: 以下部分数据有问题
        'status': company[2],
        'people_num': company[4],
        'website': company[6]
    }

    return job_info, company_info


def work(start_url):
    job_links = set()

    driver = webdriver.chrome.webdriver.WebDriver()
    driver.get(start_url)
    driver.implicitly_wait(10)
    content = driver.page_source.encode('utf-8')
    time.sleep(random.randint(4, 10))

    job_link = get_job_list(content)
    job_links.update(job_link)

    # is_last = driver.find_element_by_class_name('pager_next').get_attribute('class')
    # while is_last != 'pager_next pager_next_disabled':
    #     driver.find_element_by_class_name('pager_next').click()
    #     driver.implicitly_wait(10)
    #     content = driver.page_source.encode('utf-8')
    #
    #     job_link = get_job_list(content)
    #     job_links.update(job_link)
    #
    #     is_last = driver.find_element_by_class_name('pager_next').get_attribute('class')
    #     time.sleep(random.randint(5, 10))

    print(len(job_links))
    for jl in job_links:
        print(jl)
        driver.get(jl)
        job_content = driver.page_source.encode('utf-8')
        driver.implicitly_wait(10)
        job_id = jl.split('.')[-2].split('/')[-1]

        try:
            job_info, com_info = get_job_info(job_content, job_id)

            insert(session, job_info, com_info)

            with open('result.txt', 'a') as f:
                f.write(json.dumps(job_info) + '    ' + json.dumps(com_info) + '\n')
            info_logger.info('get job_info: ' + jl)

            print(job_info)
        except Exception as e:
            error_logger.error('get_job_info error: ' + jl + '  ' + e.args[0])

        time.sleep(random.randint(5, 10))


if __name__ == '__main__':
    start_url = 'https://www.lagou.com/jobs/list_Python?px=default&city=%E6%88%90%E9%83%BD#filterBox'
    work(start_url)
