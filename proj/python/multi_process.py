# -*- coding:utf-8 -*-

import time
import random

from multiprocessing import Process

def multi_process(x):
    counter = 0
    while counter < 3:
        sleep_sec = random.random()
        time.sleep(sleep_sec)
        print('multi_process', x)

        counter += 1

proc_num = 3
# 创建进程
# freeze_support() # window需要用到
proc_list = []
for i in range(proc_num):
    p = Process(target=multi_process, args=(i, ))
    proc_list.append(p)

# 开启进程
for p in proc_list:
    p.start()

# 阻塞进程，直到进程执行完，依次循环
for p in proc_list:
    p.join()

print('multi_process finish!')
