# -*- coding:utf-8 -*-
#!~/anaconda3/bin/python
import os
import re
import time
import urllib.request
from io import BytesIO

import bson.binary
import chardet
import requests
import xlwt
from bs4 import BeautifulSoup as beautiful
from selenium import webdriver
import datetime
import conf
from pymongo import ASCENDING, DESCENDING
import random

#国家住建部


headers = {
    'User-Agent': random.choice(conf.user_agent)
}
# file_ad = '../政府政策公告信息/国家超链接/'

# 插入数据库
def insertFile(source1,source2,source3,ctitle,date,complete_href,ProgramStarttime,html_name,file_names,img_names,css_names,file_ad):
    coll = conf.coll
    dit = {'department': source1, "column": source2, "category": source3, "title": ctitle, "PublishedDate": date,
           "Crawllink": complete_href, "ProgramStarttime": ProgramStarttime}
    # article,file,file_name
    with open(html_name, 'rb') as file:
        article = BytesIO(file.read())
        dit.setdefault("article", bson.binary.Binary(article.getvalue()))
    i = 0
    for downfile in file_names:
        i = i + 1
        filesave = file_ad + downfile
        with open(filesave, 'rb') as file:
            file_one = BytesIO(file.read())
        key1 = "file" + str(i)
        key2 = "file_name" + str(i)
        if len(bson.binary.Binary(file_one.getvalue())) > 16793598:
            print(complete_href + " 附件过大 " + filesave)
            if filesave.split('.')[-1] == 'pdf':
                with open("/home/260199/爬虫/爬虫数据/政府公告/long_attention.pdf", 'rb') as file:
                    file_one = BytesIO(file.read())
            else:
                file_one = BytesIO(b"Attachment is too large to download")
        dit.setdefault(key1, bson.binary.Binary(file_one.getvalue()))
        dit.setdefault(key2, downfile)
    img_list = []
    for img_name in img_names:
        imgsave  = file_ad + img_name
        with open(imgsave,'rb') as img:
            img_one = BytesIO(img.read())
        img_list.append(bson.binary.Binary(img_one.getvalue()))
    dit.setdefault('imges', img_list)
    css_list = []
    for css_name in css_names:
        csssave = file_ad + css_name
        with open(csssave,'rb') as css:
            css_one = BytesIO(css.read())
        css_list.append(bson.binary.Binary(css_one.getvalue()))
    dit.setdefault('css',css_list)
    coll.save(dit)
    # coll.create_index([("PublishedDate", ASCENDING)])

#获取动态网页源码,参数为分页面url
def getHtml_move(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("window-size=1024,768")
    options.add_argument("--no-sandbox")
    # options.add_argument('disable-infobars')
    driver = webdriver.Chrome('/home/260199/chrome/chromedriver', chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    time.sleep(3)
    html_str = driver.page_source
    driver.quit()
    # html = urllib.request.urlopen(url).read()
    html = bytes(html_str, encoding="utf8")        #转码
    return html,html_str

#获取静态网页源码,参数为分页面url
def getHtml_quiet(url):
    time.sleep(random.randint(5,10))
    req = urllib.request.Request(url,headers=headers)
    html = urllib.request.urlopen(req).read()
    chardit1 = chardet.detect(html)
    chard = chardit1['encoding']
    # html_req = requests.get(url)
    # html_req.encoding = chard
    # html_str = html_req.text
    html_str = html.decode(chard,'ignore')
    return html,chard,html_str

#获取正文标题、附件信息，并下载附件，参数为分页面url，网页编码格式
def get_ctitle(html_str,href,file_ad):
    bsObj = beautiful(html_str, "html.parser")
    #获取正文标题
    try:
        ctitle = bsObj.find('h1', {'id': 'con_title'}).text
    except:
        try:
            ctitle = bsObj.find('span', {'class': 'titleFont'}).text
        except:
            ctitle = None
    #获取附件信息,并下载
    file_infos = bsObj.find_all("a", {"href": re.compile(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$')})
    file_names = []
    for each in file_infos:
        file_href = each['href']
        file_adds = file_href.split('.')[-1]
        file_name = each.text
        if re.findall(file_adds,file_name):
            pass
        else:
            file_name = file_name + '.' + file_adds
        if re.findall('http',file_href):
            pass
        elif re.findall('/*/',file_href):
            file_href = 'http://www.mohurd.gov.cn' + file_href
        else:
            href_add = href.replace(href.split('/')[-1], '')
            file_href =href_add + file_href
        # print(file_href,file_name)
        file_name = file_name.replace('/','或')
        while file_name in os.listdir(file_ad):
            file_name = file_name.rstrip('.'+file_adds)+'~.'+file_adds
        file_loc = file_ad + file_name
        try:
            download_file(file_href,file_loc)
        except:
            continue
        file_names.append(file_name)
    file_diff = sorted(set(file_names),key=file_names.index)
    # # 获取图片信息,并下载
    # img_infos = bsObj.find_all("img", {"src": re.compile(r'.jpg$|.png$')})
    # img_names = []
    # for each in img_infos:
    #     img_href = each['src']
    #     # 附件后缀
    #     img_adds = img_href.split('.')[-1]
    #     img_name = img_href.split('/')[-1]
    #     if re.findall(img_adds, img_name):
    #         pass
    #     else:
    #         img_name = img_name + '.' + img_adds
    #     if re.findall('http', img_href):
    #         pass
    #     elif re.findall('/.*/', img_href):
    #         img_href = 'http://www.mohurd.gov.cn' + img_href
    #     else:
    #         href_add = href.replace(href.split('/')[-1], '')
    #         img_href = href_add + img_href[2:]
    #     print(img_href)
    #     img_loc = file_ad + img_name
    #     try:
    #         download_file(img_href, img_loc)
    #     except Exception as e:
    #         print("下载图片出现问题：", e)
    #         continue
    #     img_names.append(img_name)
    # 获取css文件信息,并下载
    css_infos = bsObj.find_all("link", {"type": "text/css", "href": re.compile(r'.css$')})
    css_names = []
    for each in css_infos:
        css_href = each['href'].replace('../', '')
        # 附件后缀
        css_adds = css_href.split('.')[-1]
        css_name = css_href.replace('..', '').replace('/', '_')
        if re.findall(css_adds, css_name):
            pass
        else:
            css_name = css_name + '.' + css_adds
        if re.findall('http', css_href):
            pass
        elif re.findall('/.*/', css_href):
            css_href = 'http://www.mohurd.gov.cn/' + css_href
        else:
            href_add = href.replace(href.split('/')[-1], '')
            css_href = href_add + css_href
        css_loc = file_ad + css_name
        try:
            download_file(css_href, css_loc)
        except Exception as e:
            print("下载css文件出现问题:", e)
            continue
        css_names.append(css_name)
    img_names = []
    return ctitle,file_diff, img_names, css_names


#获取附件信息
def get_file(html_str,href,file_ad):
    # print(href)
    bsObj = beautiful(html_str, "html.parser")
    #获取附件信息,并下载
    file_infos = bsObj.find_all("a", {"href": re.compile(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$')})
    file_names = []
    for each in file_infos:
        file_href = each['href']
        file_adds = file_href.split('.')[-1]
        file_name = each.text
        if re.findall(file_adds,file_name):
            pass
        else:
            file_name = file_name + '.' + file_adds
        if re.findall('http',file_href):
            pass
        elif re.findall('/*/',file_href):
            file_href = 'http://www.mohurd.gov.cn' + file_href
        else:
            href_add = href.replace(href.split('/')[-1], '')
            file_href =href_add + file_href
        # print(file_href,file_name)
        file_name = file_name.replace('/','或')
        while file_name in os.listdir(file_ad):
            file_name = file_name.rstrip('.'+file_adds)+'~.'+file_adds
        file_loc = file_ad + file_name
        try:
            download_file(file_href,file_loc)
        except:
            continue
        file_names.append(file_name)
    file_diff = sorted(set(file_names),key=file_names.index)
    # # 获取图片信息,并下载
    # img_infos = bsObj.find_all("img", {"src": re.compile(r'.jpg$|.png$')})
    # img_names = []
    # for each in img_infos:
    #     img_href = each['src']
    #     # 附件后缀
    #     img_adds = img_href.split('.')[-1]
    #     img_name = img_href.split('/')[-1]
    #     if re.findall(img_adds, img_name):
    #         pass
    #     else:
    #         img_name = img_name + '.' + img_adds
    #     if re.findall('http', img_href):
    #         pass
    #     elif re.findall('/.*/', img_href):
    #         img_href = 'http://www.mof.gov.cn' + img_href
    #     else:
    #         href_add = href.replace(href.split('/')[-1], '')
    #         img_href = href_add + img_href[2:]
    #     print(img_href)
    #     img_loc = file_ad + img_name
    #     try:
    #         download_file(img_href, img_loc)
    #     except Exception as e:
    #         print("下载图片出现问题：", e)
    #         continue
    #     img_names.append(img_name)
    # 获取css文件信息,并下载
    css_infos = bsObj.find_all("link", {"type": "text/css", "href": re.compile(r'.css$')})
    css_names = []
    for each in css_infos:
        css_href = each['href']
        if '../' in css_href:
            css_href = '/'+css_href.replace('../','')
        # 附件后缀
        css_adds = css_href.split('.')[-1]
        css_name = css_href.replace('..', '').replace('/', '_')
        if re.findall(css_adds, css_name):
            pass
        else:
            css_name = css_name + '.' + css_adds
        if re.findall('http', css_href):
            pass
        elif re.findall('/.*/', css_href):
            css_href = 'http://www.mof.gov.cn' + css_href
        else:
            href_add = href.replace(href.split('/')[-1], '')
            css_href = href_add + css_href
        css_loc = file_ad + css_name
        try:
            download_file(css_href, css_loc)
        except Exception as e:
            print("下载css文件出现问题:", e)
            continue
        css_names.append(css_name)
    img_names = []
    return file_diff, img_names, css_names


#保存为html文件，并获取保存后的html文件全称（**.html）
def saveHtml(html_save, html_content,file_ad):
    #    注意windows文件命名的禁用符，比如 /
    try:
        html_name = file_ad+html_save.replace('/', '_') + ".html"
        with open(html_name, "wb") as f:
            #   写文件用bytes而不是str，所以要转码
            f.write(html_content)
    except:
        html_name = file_ad+html_save.replace('/', '_')[:20] + ".html"
        with open(html_name, "wb") as f:
            #   写文件用bytes而不是str，所以要转码
            f.write(html_content)
    return html_name


#保存附件
def download_file(file_href,file_loc):
    time.sleep(random.randint(3,5))
    r = requests.get(file_href, stream=True, headers=headers,timeout = 5)
    # download started
    with open(file_loc, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

# 保存到excel表
def save_excel(worksheet, row, title,ctitle, html_name, source1,source2,source3, date,ProgramStarttime, complete_href, file_names,img_names,css_names,file_ad):
    # 写入一行
    i = 0
    content = [ctitle, "", source1, source2,source3,date,ProgramStarttime, complete_href, ""]
    for each_header in content:
        worksheet.write(row, i, each_header)
        i += 1
    # 向excel表插入html文件超链接
    link = 'HYPERLINK("%s";"%s")' % (html_name, str(title))
    worksheet.write(row, 1, xlwt.Formula(link))
    # 向excel表插入附件超链接
    x = 8
    for down_name in file_names:
        # print(down_name)
        file_loc = file_ad + down_name
        link = 'HYPERLINK("%s";"%s")' % (file_loc, down_name)
        worksheet.write(row, x, xlwt.Formula(link))
        x = x + 1
        # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com
    for img_name in img_names:
        img_loc = file_ad +img_name
        link = 'HYPERLINK("%s";"%s")' % (img_loc, img_name)
        worksheet.write(row, x, xlwt.Formula(link))
        x = x + 1
    for css_name in css_names:
        css_loc = file_ad +css_name
        link = 'HYPERLINK("%s";"%s")' % (css_loc, css_name)
        worksheet.write(row, x, xlwt.Formula(link))
        x = x + 1

#国家住建部信息公开    静态网页
def xxgk_url(row,worksheet,url,href_bloom,file_ad,ProgramStarttime):
    source1 = '住建部'
    source2 = '信息公开'
    source3 = '通知公告'
    print("网站：", source1 + '  ' + source2 + ' ' + url)
    chref_list = []
    time.sleep(random.randint(10,20))
    # 获取网页编码格式
    reqt = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(reqt).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req = response.decode(chardit,'ignore')
    # req.encoding = chardit1['encoding']
    soup = beautiful(req, 'lxml')
    item_list = soup.find_all('tr', {'class': 'item'})
    alitem_list = soup.find_all('tr', {'class': 'alitem'})
    al_list = item_list + alitem_list
    for al in al_list:
        al = str(al).replace('\n', '').replace('\r', '')
        # 获取完整链接、正文完整标题、正文标题、发布日期
        complete_href = re.findall('<a href="(.*?)" message=', al)[0]
        ctitle = re.findall('&amp;&amp;(.*?)" onmousemove=', al)[0].replace('&amp;', '')
        title = re.findall('target="_blank">(.*?)</a>', al)[0]
        date = re.findall('<td>(.*?)</td>', al)[0]
        date = date.replace('.', '-').replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            continue
        elif re.search(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$', complete_href):
            print("正在采集：", complete_href)
            href_adds = complete_href.split('.')[-1]
            title = ctitle + '.' + href_adds
            title = title.replace('/', '或')
            html_name = file_ad + title
            download_file(complete_href, html_name)
            file_names = []
            img_names  = []
            css_names = []
            # 插入数据库
            insertFile(source1, source2, source3, title, date, complete_href, ProgramStarttime, html_name, file_names,img_names,css_names,
                       file_ad)
            href_bloom.update([complete_href])
            # 保存到excel表
            save_excel(worksheet, row, title, title, html_name, source1, source2, source3, date, ProgramStarttime,
                       complete_href, file_names,img_names,css_names, file_ad)
        else:
            print("正在采集：", complete_href)
            #获取静态网页源码
            html,chard,html_str = getHtml_quiet(complete_href)
            # 保存为html文件
            html_name = saveHtml(title, html,file_ad)
            #获取附件（在分页面获取的）
            file_names,img_names,css_names = get_file(html_str,complete_href,file_ad)
            #插入数据库
            insertFile(source1, source2, source3, title, date, complete_href, ProgramStarttime, html_name, file_names,img_names,css_names,file_ad)
            href_bloom.update([complete_href])
            # 保存到excel表
            save_excel(worksheet, row, title, ctitle, html_name, source1, source2, source3, date, ProgramStarttime,complete_href, file_names,img_names,css_names, file_ad)
            row = row + 1
    return row,chref_list

#国家住建部政策发布   静态网页
def wjfb_url(row,worksheet,url,href_bloom,file_ad,ProgramStarttime):
    source1 = '住建部'
    source2 = '政策发布'
    source3 = '政策法规'
    print("网站：", source1 + '  ' + source2 + ' ' + url)
    chref_list = []
    # 获取网页编码格式
    time.sleep(random.randint(10,20))
    reqt = urllib.request.Request(url,headers = headers)
    response = urllib.request.urlopen(reqt).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req = response.decode(chardit,'ignore')
    # req.encoding = chardit1['encoding']
    soup = beautiful(req, 'lxml')
    item_list = soup.find_all('td', {'style': 'text-align:left;'})
    date_list = soup.find_all('td', {'style': 'width:86px;text-align:left; color:#ABABAB;'})
    for i in range(len(item_list)):
        item = str(item_list[i])
        #获取完整链接、正文标题、发布日期
        complete_href = re.findall('<a href="(.*?)"', item)[0]
        title = re.findall('>(.*?)</a>', item)[0]
        date = re.findall('>\[(.*?)\]</td>', str(date_list[i]))[0]
        date = date.replace('.', '-').replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            continue
        elif re.search(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$', complete_href):
            print("正在采集：", complete_href)
            href_adds = complete_href.split('.')[-1]
            title = title + '.' + href_adds
            title = title.replace('/', '或')
            html_name = file_ad + title
            download_file(complete_href, html_name)
            file_names = []
            img_names = []
            css_names = []
            # 插入数据库
            insertFile(source1, source2, source3, title, date, complete_href, ProgramStarttime, html_name, file_names,img_names,css_names,
                       file_ad)
            href_bloom.update([complete_href])
            # 保存到excel表
            save_excel(worksheet, row, title, title, html_name, source1, source2, source3, date, ProgramStarttime,
                       complete_href, file_names,img_names,css_names, file_ad)
        else:
            print("正在采集：", complete_href)
            #获取静态网页源码
            html,chard,html_str = getHtml_quiet(complete_href)
            # 保存为html文件
            html_name = saveHtml(title, html,file_ad)
            #获取附件（在分页面获取的）
            file_names,img_names,css_names = get_file(html_str,complete_href,file_ad)
            #插入数据库
            insertFile(source1, source2, source3, title, date, complete_href, ProgramStarttime, html_name, file_names,img_names,css_names,file_ad)
            href_bloom.update([complete_href])
            # 保存到excel表
            save_excel(worksheet, row, title, title, html_name, source1, source2, source3, date, ProgramStarttime,complete_href, file_names,img_names,css_names, file_ad)
            row = row + 1
    return row,chref_list




def main(row,worksheet,href_bloom,file_ad1,ProgramStarttime):
    href_list = []
    try:
        url1 = 'http://ginfo.mohurd.gov.cn/'
        row,chref_list = xxgk_url(row,worksheet,url1,href_bloom,file_ad1,ProgramStarttime)
        href_list.extend(chref_list)
    except Exception as e:
        print(e)
    try:
        url2 = 'http://www.mohurd.gov.cn/wjfb/index.html'
        row,chref_list = wjfb_url(row,worksheet,url2,href_bloom,file_ad1,ProgramStarttime)
        href_list.extend(chref_list)
    except Exception as e:
        print(e)
    print(row)
    return row,href_list





