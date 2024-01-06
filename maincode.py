# coding=utf-8
"""
爬取百度图片的高清原图

"""
import re
import sys
import urllib
import os
import matplotlib.pyplot as plt#图表显示
import requests
import face5#人脸检测
import number#数据
import cv2
import savemysql

def get_onepage_urls(onepageurl):
    if not onepageurl:
        print('执行结束')
        return [], ''
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        fanye_url = ''
        return pic_urls, fanye_url
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    fanye_urls = re.findall(re.compile(r'<a href="(.*)" class="n">下一页</a>'), html, flags=0)
    fanye_url = 'http://image.baidu.com' + fanye_urls[0] if fanye_urls else ''
    return pic_urls, fanye_url


def down_pic(pic_urls, localPath):
    if not os.path.exists(localPath):  # 所有图片
        os.mkdir(localPath)
    if not os.path.exists('e:/project/allface/'):  # 所有脸
        os.mkdir('e:/project/allface/')
    if not os.path.exists('e:/project/allpeo/'):  # 所有相关人员的第一张脸
        os.mkdir('e:/project/allpeo/')
    """给出图片链接列表, 下载图片"""
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=15)
            string = str(i + 1) + '.jpg'
            with open(localPath + '%d.jpg' % i, 'wb')as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            number.COUNT_C += 1
            continue
        #识别
        try:
            num=face5.faceClasify(localPath,str(i))
            if num > 0:
                number.COUNT_A += 1
            elif num ==0:#没有人脸
                number.COUNT_B += 1
            else: #没有主角脸
                number.COUNT_D +=1
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            number.COUNT_C += 1
            continue


if __name__ == '__main__':
    keyword = input("请输入需要爬取的人物：")
    url_init_first = r'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1497491098685_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&ctd=1497491098685%5E00_1519X735&word='
    url_init = url_init_first + urllib.parse.quote(keyword, safe='/')
    all_pic_urls = []
    onepage_urls, fanye_url = get_onepage_urls(url_init)
    all_pic_urls.extend(onepage_urls)

    fanye_count = 1  # 图片所在页数，下载完后调整这里就行
    while 1:
        onepage_urls, fanye_url = get_onepage_urls(fanye_url)
        fanye_count += 1
        print('第%s页' % fanye_count)
        if fanye_url == '' and onepage_urls == []:
            break
        all_pic_urls.extend(onepage_urls)


    down_pic(list(set(all_pic_urls)), 'e:/project/%s/' % fanye_count)  # 保存位置也可以修改

    for i in range(len(number.FACE_NUM)):
        print("picture"+str(i)+":"+str(number.FACE_NUM[i]))
        savemysql.save(number.FACE_NUM[i],( r'e:/project/allpeo/%s.jpg')% str(i+1))

    #显示图表
    print("成功下载图片数为：")
    print(number.COUNT_A)
    print("图片数据错误数为：")
    print(number.COUNT_B)
    print("图片数据无关数为：")
    print(number.COUNT_D)
    print("下载图片失败数为：")
    print(number.COUNT_C)
    labels = 'Successful Download', 'Wrong Picture', 'Failed Download','Inrelevant Picture'
    sizes = [number.COUNT_A, number.COUNT_B, number.COUNT_C, number.COUNT_D]
    # 设置分离的距离，0表示不分离
    explode = (0.1, 0, 0,0)
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    # Equal aspect ratio 保证画出的图是正圆形
    plt.axis('equal')
    plt.show()


