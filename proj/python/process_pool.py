# -*- coding:utf-8 -*-

import time

from multiprocessing.pool import Pool


def process_pool(x):
    counter = 0
    while counter < 3:
        time.sleep(1)

        counter += 1


if __name__ == '__main__':
    pool = Pool(3)
    st = time.time()
    ret = pool.map(process_pool, ['a', 'b', 'c'])
    ds = time.time()
    print('time cost:', ds-st)
