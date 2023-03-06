# -*- coding:utf-8 -*-


def consumer():
    print('consumer >>>')
    while True:
        value = yield   #接收send发送的数据
        if value != 'END':
            print('consumer {}'.format(value))
        else:
            break
    yield 'game over!'

def producer():
    con = consumer()
    value = next(con)
    while True:
        if not value:
            x = input('please enter a number:')
            value = con.send(x)
        else:
            print('producer finish')
            break
    con.close()


if __name__ == "__main__":
    producer()
