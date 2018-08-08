# -*- coding:utf-8 -*-

import time
import os
import sys

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import conf
cur_path = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(cur_path, "../conf")))
from settings import *

Base = declarative_base()
day = time.strftime('%Y%m%d')


def get_engine(user, passwd, host, port, db):
    # 'mysql://lagou:lagou_passwd@localhost:3306/lagou'
    url = 'mysql://{user}:{passwd}@{host}:{port}/{db}'.format(user=user, passwd=passwd, host=host, port=port, db=db)
    return create_engine(url, echo=True)


def get_session(engine):
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


class Job(Base):
    __tablename__ = 'job_info'
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    company_name = Column(String(256))
    position = Column(String(128))
    salary = Column(String(32))
    position_label = Column(String(256))
    job_request = Column(String(2048))

    city = Column(String(32))
    work_experience = Column(String(32))
    education = Column(String(32))
    full_or_part = Column(String(32))

    job_advantage = Column(String(2048))
    job_description = Column(String(4096))
    work_add = Column(String(1024))
    review_anchor = Column(String(256))
    day = Column(String(16))


class Company(Base):
    __tablename__ = 'company_info'
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String(256))
    zone = Column(String(256))
    status = Column(String(256))
    people_num = Column(String(256))
    website = Column(String(128))
    day = Column(String(16))


engine = get_engine(db_user, db_passwd, db_host, db_port, db_name)
Base.metadata.create_all(engine)


def insert(engine, job_info, company_info):
    session = get_session(engine)

    if not job_info or not company_info:
        return

    job = Job(
        job_id=job_info['job_id'],
        company_id=job_info['company_id'],
        company_name=job_info['company_name'],
        position=job_info['position'],
        salary=job_info['salary'],
        position_label=job_info['position_label'],
        city=job_info['city'],
        work_experience=job_info['work_experience'],
        education=job_info['education'],
        full_or_part=job_info['full_or_part'],
        job_advantage=job_info['job_advantage'],
        job_description=job_info['job_description'],
        work_add=job_info['work_add'],
        review_anchor=job_info['review_anchor'],
        day=day
    )

    company = Company(
        company_id=company_info['id'],
        company_name=company_info['name'],
        zone=company_info['zone'],
        status=company_info['status'],
        people_num=company_info['people_num'],
        website=company_info['website'],
        day=day
    )

    if not session.query(Job).filter_by(job_id=job_info['job_id']).one_or_none():
        session.add(job)
    if not session.query(Company).filter_by(company_id=company_info['id']).one_or_none():
        session.add(company)

    session.commit()
