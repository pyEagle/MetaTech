# -*- coding:utf-8 -*-

import time
import datetime

from dateutil.relativedelta import relativedelta


# 1.时间戳转时间
print(datetime.datetime.fromtimestamp(1487760447.27658))
 
# 2.时间戳转时间格式
print(datetime.datetime.fromtimestamp(1487760447.27658).strftime('%Y-%m-%d %H:%M:%S'))

# 3.字符串时间转换成时间
s = "2015-06-15 14:00:00"
t = datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

# 4.时间转成字符串时间
t = datetime.datetime.now()
s = t.strftime('%Y-%m-%d %H:%M:%S')

# 5.时间转换成时间戳
now = datetime.datetime.now()
print(time.strftime('%s')) # for python2.x
print(datetime.datetime.timestamp(now)) # for python3.x

# 6.向前/向后若干天
now = datetime.datetime.now()
delay_days = 5
print(now-datetime.timedelta(days=delay_days)) # 相差 delay_days
print(now-relativedelta(months=delay_months)) # 相差delay_months

# 7.两个时间点相差日期
date1 = datetime.datetime.strptime('2011-08-15 12:00:00', '%Y-%m-%d %H:%M:%S')
date2 = datetime.datetime.strptime('2012-02-15', '%Y-%m-%d')
date_delta = relativedelta(date1, date2)
print(date_delta.years, date_delta.months, date_delta.weeks, date_delta.days)
