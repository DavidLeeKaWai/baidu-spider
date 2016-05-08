# -*- coding: utf-8 -*-
from selenium import webdriver
import urllib
import time
import datetime
import platform
import os

def get_indexurl(keyword):
    searching_url = 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&rsp=1&word=keywords&oq=keyoq'
    searching_url = searching_url.replace('keywords',keyword)
    searching_url = searching_url.replace('keyoq',keyword)
    url = repr(searching_url)
    url = url[1:len(url)]
    url = url.replace('\\x','%')
    print url
    return url

def get_imgURL(URL):
    xpath = '//div[@id="imgid"]/div/ul/li'
    img_url_dic = {}
    js = 'window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);'
    try:
        driver = webdriver.PhantomJS()
        driver.set_window_size(160000000, 90000000, windowHandle='current')
        driver.get(URL)

    except:
        print "Can't open the driver, please try again later!"
        os._exit(1)
    start = datetime.datetime.now()
    if platform.system() == 'Windows':
        cls_cmd = 'cls'
    else:
        if platform.system() == 'Linux':
            cls_cmd = 'clear'
    for i in [6, 5, 4, 3, 2, 1]:
        time.sleep(1)

        k = os.system(cls_cmd)
        print 'Img URL grabbing will be start in ', i, '(s)'
    m = 0
    while True:
        driver.execute_script(js)
        time.sleep(1)
        for element in driver.find_elements_by_xpath(xpath):
            img_url = element.get_attribute('data-objurl')
            if img_url is not None and not img_url_dic.has_key(img_url):
                start = datetime.datetime.now()
                m += 1
                img_url_dic[img_url] = ''
                print m, img_url
                try:
                    file = open('img_url', 'a')
                    file.write(img_url + '\n')
                    file.close()
                except:
                    print 'Can\'t operate the file in saving no.%d URL' % m
        end = datetime.datetime.now()
        if (end - start).seconds > 60:
            break
        driver.execute_script(js)
    print 'done!'
    driver.close()

def save_imge(keyword):
    timeout = 60
    f = open('img_url', 'r')
    m = 0
    BASE_DIR = os.path.dirname(__file__)
    os.mkdir(os.path.join(BASE_DIR, keyword))
    os.chdir(os.path.join(BASE_DIR, keyword))
    for line in f:
        m += 1
        print 'saving No.', m, 'photo, url: ', line
        try:
            urllib.urlretrieve(line, str(m) + '.jpg')
        except:
            print 'Can not download No.%d photo\n' % m
            f = open('download_status.log', 'a')
            f.write('Can not download No.%d photo\n' % m)
            f.close()
        if m % 100 == 0:
            time.sleep(4)

if __name__ == '__main__':
    keyword = raw_input('Please input key word:')
    get_imgURL(get_indexurl(keyword))
    cmd = raw_input('Do you want to save the image?(Y/N)')
    if cmd == 'Y':
        save_imge(keyword)