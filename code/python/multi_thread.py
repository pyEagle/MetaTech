# -*- coding:utf-8 -*-

import time
import random
import threading


def foo(x):
    counter = 0
    while counter < 5:
        print(x, counter)
        counter += 1
        time.sleep(random.random())


def multi_thread(thread_num):
    # 创建线程
    thread_list = []
    for i in range(thread_num):
        p = threading.Thread(target=foo, args=('foo_{}'.format(i),))
        thread_list.append(p)
    # 开启线程
    for p in thread_list:
        p.start()
    # 等待线程执行结束
    for p in thread_list:
        p.join()


if __name__ == '__main__':
    thread_num = 3
    multi_thread(thread_num)
