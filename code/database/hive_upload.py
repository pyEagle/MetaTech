# -*- coding:utf-8 -*-

import os

import pandas as pd

from impala.dbapi import connect
from impala.util import as_pandas


def main(csv_file):
    # os.system('hadoop fs -put ./demo1.csv /tmp')
    conn = connect(
        host='', 
        port=0, 
        user='',
        password='', 
        auth_mechanism='',
        )
    cursor = conn.cursor()
    
    cursor.execute("LOAD DATA INPATH '{}' INTO TABLE temp.pandas_write_data_test".format(csv_file))
    cursor.close()

if __name__ == "__main__":
    csv_file = '/tmp/demo.csv'
    main(csv_file)

