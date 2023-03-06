# -*- coding:utf-8 -*-

import re

# 1. 别名：(?P<name>re)
p = re.compile(r'(?P<qq_mail>\d+?@qq.com)')
t = p.search('123456@qq.com')
print([t.groupdict(), t.group(), t.groups()])

# 2. 非贪婪模式(*? +? {n,}?)
p = re.compile(r'a.*d')
print('贪婪模式:', p.search('asdssssd'))
p1 = re.compile(r'a.*?d')
print('非贪婪模式', p1.search('asdssssd'))

# 3. 子表达式 (re)
p = re.compile(r'(ad)|(ds)')
t = 'sfsadsfsdfsdfcdsfdsf'
for i in p.finditer(t):
    print(i.groups())

# 4. 反向引用 \number
p = re.compile(r'[ ]+(\w+)+[ ]+\1')
print(p.search('ax bc ax ax cd'))

# 5. 向前查看 肯定(?=) 否定(?!)
p = re.compile(r'.+(?=:)')
print(p.search('https:www.baidu.com'))

# 6. 向后查看 肯定(?<=) 否定(?<!)
p = re.compile(r'(?<=\$)[0-9.]+')
print(p.search('abc: $123.456'))

# 7. 条件匹配 ?
p = re.compile(r'(\d{5})(?(1)-\d{4})')
print(p.search('12345-1234'))
