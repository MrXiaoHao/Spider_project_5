import requests
from requests.exceptions import RequestException
import os
import time
from lxml import etree

headers ={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

#获取tag页面
def get_html(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200 :
            return response.text
        else:
            print("请求主页面出错")
            return None
    except RequestException:
        get_html(url)
#解析tag页面，并且获得图片集url地址
def parse_html(html):
    # parttern = re.compile('.*?<ul class="pic-model clearfix".*?<a href="(.*?)".*?</a>.*?</ul>.*?',re.S)
    # urls  = re.findall(parttern,html)
    # print(urls)
    content = etree.HTML(html)
    links = content.xpath('//div/ul[@class="pic-model clearfix"]')
    for link in links:
        pic_url = link.xpath("./li/p/a/@href")
        for url in pic_url:
            yield url

#获取图片集的html
def get_pic_html(pic_url):
    try:
        response = requests.get(pic_url,headers = headers)
        if response.status_code == 200 :
            return response.text
        else:
            print("请求详情图片页面出错")
    except RequestException:
        get_pic_html(pic_url)

#解析图片集的每张图片，获取对应图片链接地址
def parse_pic_html(pic_html):
    pic_content = etree.HTML(pic_html)

    pic_links = pic_content.xpath('//div/div/div[@class="album-list-box"]')
    #pic_links = pic_content.xpath('*//ul[@class="clearfix"]')
    for pic_link in pic_links:
        pics = pic_link.xpath('./div/ul/li/a/img/@big_pic')
        #pics = pic_link.xpath('./li/a/img/@src')
        for pic in pics:
            yield pic

    pic_linkss = pic_content.xpath('//div/div/div[@class="l2"]')
    for pics_link in pic_linkss:
        picss = pics_link.xpath('./div/ul/li/a/img/@bigpic')
        for picc in picss:
            yield picc
#下载图片到指定位置目录
def down_pic(pic_list):
    if not os.path.exists('bizhi'):
        os.mkdir('bizhi')
    pic = requests.get(pic_list)
    img = pic.content
    print(pic_list)
    img_name = "bizhi/"+ str(time.time()) + ".jpg"
    try:
        with open(img_name, "wb") as f:
            f.write(img)
            print("下载完成")
    except Exception as e:
        print(e)

def main():
    print("*"*50)
    print("美女  明星  帅哥  女生  动漫  汽车  游戏  卡通  王者荣耀")
    print("*" * 50)
    tag = input("请输入需要爬取图片的类别：")
    page =1
    for page in range (1,51):
        print("正在打印:"+str((page))+ "页")
        url = "https://www.bizhizu.cn/shouji/tag-"
        start_url= url + str(tag) + "/" + str(page) +".html"
        print(start_url)
        html = get_html(start_url)
        urls = parse_html(html)
        for url in urls:
            pic_html = get_pic_html(url)
            #print(pic_html)
            pic_list = parse_pic_html(pic_html)
            for pic_url in pic_list:
                # print(pic_url)
                down_pic(pic_url)
        page += 1


if __name__ == '__main__':
        main()
