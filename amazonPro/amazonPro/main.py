import time
import os
import threading
import re
import datetime

order_list = []


def start(condition):
    # 多线程启动爬虫
    global order_list
    try:
        condition.acquire()
        order = order_list.pop()
        time.sleep(1)
        condition.notify()
    finally:
        condition.release()
        t = int(order[1])
        order1 = 'scrapy crawl amazon -a kw="' + order[0] + '"'
        while True:
            os.system(order1)
            os.rename("%s.txt" % order[0], str(datetime.datetime.now().date()) + '-%s.txt' % order[0])
            print(str(datetime.datetime.now()) + '---' + order[0])
            time.sleep(t)


def main():
    condition = threading.Condition()
    threads = []
    # 读取关键词及间隔时间
    with open("./conf.txt", 'r', encoding='utf-8') as fp:
        text = fp.readlines()
    thread_num = len(text)
    for txt in text:
        txt = re.split(',|\n', string=txt)[:2]
        order_list.append(txt)
    # 启动多线程，每一个线程负责一个爬虫
    for _ in range(thread_num):
        spider_thread = threading.Thread(target=start, args=(condition,))
        threads.append(spider_thread)
        spider_thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
