# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Job(Base):
    __tablename__ = 'job_info'
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    company_name = Column(String(256))
    position = Column(String(128))
    salary = Column(String(32))
    position_label = Column(String(256))
    job_request = Column(String(2048))
    job_advantage = Column(String(2048))
    job_description = Column(String(2048))
    work_add = Column(String(1024))
    review_anchor = Column(String(256))


class Company(Base):
    __tablename__ = 'company_info'
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(256))
    zone = Column(String(256))
    status = Column(String(256))
    people_num = Column(String(128))
    website = Column(String(128))


    # job_info = {
    #     'job_id': int(job_id),
    #     'company_id': int(company_id),
    #     'company_name': company_name,
    #     'position': position,
    #     'salary': salary,
    #     'position_label': position_label,
    #     'job_request': job_request,
    #     'job_advantage': job_advantage,
    #     'job_description': job_description,
    #     'work_add': work_add,
    #     'review_anchor': review_anchor
    # }
    # company_info = {
    #     'id': int(company_id),
    #     'name': job_company,
    #     'zone': company[0],
    #     'status': company[2],
    #     'people_num': company[4],
    #     'website': company[6]
    # }


def get_session(user, passwd, host, port, db):
    # 'mysql://lagou:lagou_passwd@localhost:3306/lagou'
    url = 'mysql://{user}:{passwd}@{host}:{port}/{db}'.format(user=user, passwd=passwd, host=host, port=port, db=db)
    engine = create_engine(url, echo=True)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    return session


def insert(session, job_info, company_info):

    if not job_info or not company_info:
        return

    job = Job(
        job_id=job_info['job_id'],
        company_id=job_info['company_id'],
        company_name=job_info['company_name'],
        position=job_info['position'],
        salary=job_info['salary'],
        position_label=job_info['position_label'],
        job_request=job_info['job_request'],
        job_advantage=job_info['job_advantage'],
        job_description=job_info['job_description'],
        work_add=job_info['work_add'],
        review_anchor=job_info['review_anchor']
    )

    company = Company(
        company_id=company_info['id'],
        company_name=company_info['name'],
        zone=company_info['zone'],
        status=company_info['status'],
        people_num=company_info['people_num'],
        website=company_info['website']
    )

    session.add_all([job, company])
    session.commit()


def save_to_db(job_info, company_info):
    session = get_session('lagou', 'lagou_passwd', 'localhost', '3306', 'lagou')
    insert(session, job_info, company_info)
