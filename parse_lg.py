# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
import json
from requests_html import HTMLSession
import time
from selenium import webdriver


cookie = get_cookie('https://www.lagou.com/jobs/list_Python?px=default&city=%E6%88%90%E9%83%BD#filterBox')

# get html source code
def get_html(url):
    # session = HTMLSession()
    # r = session.get(url)    
    # return r.text
    driver = webdriver.chrome.webdriver.WebDriver()
    driver.get(url)    
    driver.delete_all_cookies()

    driver.implicitly_wait(10)

    # driver.find_element_by_class_name('pager_next').get_attribute('class')
    # pager_next pager_next_disabled
    time.sleep(10)
    return driver.page_source.encode('utf-8')


# get job_list_pages_link
def get_page_link(start_url):
    page_link = set()
    page_link.add(start_url)

    c = get_html(start_url)
    soup_c = BeautifulSoup(c, 'lxml')
    is_last = soup_c.find('a', class_='page_no pager_next_disabled')

    while is_last:
        next_url = soup_c.find_all('a', class_='page_no')[-1].get('href')
        page_link.add(next_url)

        c = get_html(next_url)
        soup_c = BeautifulSoup(c, 'lxml')
        is_last = soup_c.find('a', class_='page_no pager_next_disabled')
        time.sleep(5)

    return page_link


# get job_links
def get_job_list(url):
    content = get_html(url)
    soup_c = BeautifulSoup(content, 'lxml')

    job_links = soup_c.find_all('a', class_='position_link')
    job_links = [jl.get('href') for jl in job_links]

    return job_links


def get_job_info(url):
    content = get_html(url)
    # print(content)
    soup = BeautifulSoup(content, 'lxml')

    title = soup.title.text
    # company_name = soup.find('div', class_='company').text
    company_name = soup.find('h2', class_='fl').text
    position = soup.find('span', class_='name').text
    salary = soup.find('span', class_='salary').text

    position_label = soup.find_all('li', class_='labels')
    position_label = [lb.text for lb in position_label]

    job_request = soup.find('dd', class_='job_request').text.split('\n')[3:7]

    job_advantage = soup.find('dd', class_='job-advantage').text
    job_description = soup.find('dd', class_='job_bt').text

    work_add = soup.find('div', class_='work_addr').text.replace('\n',' ')
    work_add = re.sub(r'\s', '', work_add[:-1])[:-4]

    review_anchor = soup.find('a', class_='checkAll').get('href')

    job_company = soup.find('h2', class_='fl').text
    job_company = re.sub(r'\s', '', job_company.replace(soup.find('span', class_='dn').text, ''))

    company = soup.find('ul', class_='c_feature').text
    company = [re.sub(r'\s', '',cy) for cy in company.split('\n') if cy]

    job_info = {
        'company_name': company_name,
        'position': position,
        'salary': salary,
        'position_label': position_label,
        'job_request': job_request,
        'job_advantage': job_advantage,
        'job_description': job_description,
        'work_add': work_add,
        'review_anchor': review_anchor, 
    }
    company_info = {
        'name': job_company,
        'zone': company[0],
        'status': company[2],
        'people_num': company[4],
        'website': company[6]
    }

    return job_info, company_info


def main():
    start_url = 'https://www.lagou.com/zhaopin/Python/'
    page_links = get_page_link(start_url)
    # print(page_links)

    job_links = set()

    jbl = get_job_list(start_url)
    for pl in page_links:
        job_links.update(pl)
    # job_links.update(jbl)
    # print(job_links)

    for jl in job_links:
        print(jl)
        job_info, com_info = get_job_info(jl)
        with open('result.txt', 'a') as f:
            f.write(json.dumps(job_info) + '    ' + json.dumps(com_info) + '\n')

if __name__ == '__main__':
    main()


# start_url = 'https://www.lagou.com/zhaopin/Python/?filterOption=3'
# next_url = 'https://www.lagou.com/zhaopin/Python/2/'
