import pandas as pd
import pymysql

import sys
import os

# import settings
cur_path = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(cur_path, "../conf")))
from settings import *


conn = pymysql.connect(host=db_host,
                       user=db_user,
                       password=db_passwd,
                       db=db_name,
                       port=int(db_port)
                      )

sql = 'select * from job_info where day=20180807'
df = pd.read_sql(sql, con=conn)