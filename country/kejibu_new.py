from selenium import webdriver
import requests
import re
import time
import chardet
import urllib.request
from bs4 import BeautifulSoup as beautiful
import xlwt
import os


#国家科学技术部


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}
file_ad = '../政府政策公告信息/测试/'
#获取动态网页源码,参数为分页面url
def getHtml_move(url):
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
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
    html = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(html)
    chard = chardit1['encoding']
    html_req = requests.get(url)
    html_req.encoding = chard
    html_str = html_req.text
    return html,chard,html_str

#获取正文标题、附件信息，并下载附件，参数为分页面url，网页编码格式
def get_ctitle(html_str):    #无
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
    # print(file_infos)
    f1 = re.compile('href="(.*?)"')
    f2 = re.compile('">(.*?)</a>')
    file_names = []
    for each in file_infos:
        # file_href = each['href']
        file_href = re.findall(f1, str(each))[0]
        file_name = re.findall(f2, str(each))[0]
        # print(file_href,file_name)
        if file_name == '':
            continue
        if re.findall('http',file_href):
            pass
        else:
            file_href ='http://www.miit.gov.cn/' + file_href.split('../')[-1]
        # print(file_href)
        file_loc = file_ad + file_name
        download_file(file_href,file_loc)
        file_names.append(file_name)
    return ctitle,file_names

#获取附件信息
def get_file(html_str,href):
    # print(href)
    bsObj = beautiful(html_str, "html.parser")
    #获取附件信息,并下载
    file_infos = bsObj.find_all("a", {"href": re.compile(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$')})
    file_names = []
    for each in file_infos:
        file_href = each['href']
        file_adds = file_href.split('.')[-1]
        file_name = each.text
        href_add = href.replace(href.split('/')[-1], '')
        # print(file_href)
        if file_name == '':
            continue
        if re.findall(file_adds,file_name):
            pass
        else:
            file_name = file_name + '.' + file_adds
        if re.findall('http',file_href):
            newfile_href = file_href
            # print('1:',newfile_href)
        elif '/u/' in file_href:
            newfile_href = 'http://service.most.gov.cn' + file_href
            # print('2:',newfile_href)
        elif re.findall('/.*?/',file_href):
            newfile_href = 'http://www.most.gov.cn/' + file_href.replace('../','')
            # print('3:',newfile_href)
        elif './' in file_href:
            newfile_href =href_add + file_href.replace('./','')
            # print('4:',newfile_href)
        else:
            newfile_href = file_href
            # print('5:',newfile_href)
        # print(newfile_href,file_name)
        file_name = file_name.replace('/','或')
        while file_name in os.listdir(file_ad):
            file_name = file_name.rstrip('.'+file_adds)+'~.'+file_adds
        file_loc = file_ad + file_name
        download_file(newfile_href,file_loc)
        file_names.append(file_name)
    file_diff = sorted(set(file_names), key=file_names.index)
    return file_diff

#保存为html文件，并获取保存后的html文件全称（**.html）
def saveHtml(html_save, html_content):
    #    注意windows文件命名的禁用符，比如 /
    html_name = file_ad+html_save.replace('/', '_') + ".html"
    with open(html_name, "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(html_content)
    return html_name


#保存附件
def download_file(file_href,file_loc):
    r = requests.get(file_href, stream=True, headers=headers)
    # download started
    with open(file_loc, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

# 保存到excel表
def save_excel(worksheet, row, title,ctitle, html_name, source1,source2, date, complete_href, file_names):
    # 写入一行
    i = 0
    content = [ctitle, "", source1, source2,date, complete_href, ""]
    for each_header in content:
        worksheet.write(row, i, each_header)
        i += 1
    # 向excel表插入html文件超链接
    link = 'HYPERLINK("%s";"%s")' % (html_name, str(title))
    worksheet.write(row, 1, xlwt.Formula(link))
    # 向excel表插入附件超链接
    x = 6
    for down_name in file_names:
        # print(down_name)
        file_loc = file_ad + down_name
        link = 'HYPERLINK("%s";"%s")' % (file_loc, down_name)
        worksheet.write(row, x, xlwt.Formula(link))
        x = x + 1
        # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com

#国家科技部通知通告    静态网页
def tztg_url(row,worksheet,url,href_bloom):
    source1 = '国家科技部'
    source2 = '通知通告'
    print("栏目：", source2)
    chref_list = []
    req = requests.get(url)
    # 获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    item_list = soup.find_all('td', {'class': 'STYLE30'})
    # print(item_list)
    for item in item_list:
        href = re.findall('href="(.*?)"', str(item))[0]
        title = re.findall('target="_blank">(.*?)</a>', str(item))[0]
        date = re.findall('</a>\((.*?)\)', str(item))[0]
        # print(href,title,date)
        if '../' in href:
            complete_href = 'http://www.most.gov.cn/' + href.replace('../', '')
        elif './' in href:
            complete_href = url + href.replace('./', '')
        else:
            complete_href = href
        # print(complete_href)
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            print("该页面已存在")
            continue
        else:
            #获取静态网页源码
            html,chard,html_str = getHtml_quiet(complete_href)
            #保存为html文件
            html_name = saveHtml(title, html)
            #获取附件（在分页面获取的）
            file_names = get_file(html_str,complete_href)
            # 保存到excel表
            save_excel(worksheet, row, title,title, html_name, source1,source2, date, complete_href, file_names)
            row = row + 1
    return row,chref_list

#国家科技部科技部工作    静态网页
def kjbgz_url(row,worksheet,url,href_bloom):
    source1 = '国家科技部'
    source2 = '科技部工作'
    print("栏目：", source2)
    chref_list = []
    req = requests.get(url)
    # 获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    item_list = soup.find_all('td', {'class': 'STYLE30'})
    # print(item_list)
    for item in item_list:
        href = re.findall('href="(.*?)"', str(item))[0]
        title = re.findall('target="_blank">(.*?)</a>', str(item))[0]
        date = re.findall('</a>\((.*?)\)', str(item))[0]
        # print(href,title,date)
        if '../' in href:
            complete_href = 'http://www.most.gov.cn/' + href.replace('../', '')
        elif './' in href:
            complete_href = url + href.replace('./', '')
        else:
            complete_href = href
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            print("该页面已存在")
            continue
        else:
            #获取静态网页源码
            html,chard,html_str = getHtml_quiet(complete_href)
            #保存为html文件
            html_name = saveHtml(title, html)
            #获取附件（在分页面获取的）
            file_names = get_file(html_str,complete_href)
            # 保存到excel表
            save_excel(worksheet, row, title,title, html_name, source1,source2, date, complete_href, file_names)
            row = row + 1
    return row,chref_list

#国家科技部政府信息公开   静态加载
def xxgk_url(row,worksheet,url,href_bloom):
    source1 = '国家科技部'
    source2 = '政府信息公开'
    print("栏目：", source2)
    chref_list = []
    req = requests.get(url)
    # 获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    item_list = soup.find_all('a', {'class': 'STYLE30'})
    date_list = re.findall('<B>发布日期:</B> (.*?)</td>', req.text)
    # print(len(item_list))
    for i in range(len(item_list)):
        item = item_list[i]
        href = item['href']
        title = item.text
        date = date_list[i]
        if '../' in href:
            complete_href = 'http://www.most.gov.cn/mostinfo/xinxifenlei/' + href.replace('../', '')
        # elif './' in href:
        #     complete_href = 'http://www.most.gov.cn/mostinfo/' + href.replace('./', '')
        else:
            complete_href = href
        # print(complete_href, title, date)
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            print("该页面已存在")
            continue
        else:
            html, chard, html_str = getHtml_quiet(complete_href)
            html_name = saveHtml(title, html)
            #获取附件（在分页面获取的）
            file_names = get_file(html_str,complete_href)
            save_excel(worksheet, row, title, title, html_name, source1,source2, date, complete_href, file_names)
            row = row + 1
    return row,chref_list

#国家科技部科技计划  静态网页
def kjjh_url(row,worksheet,url,href_bloom):
    source1 = '国家科技部'
    source2 = '科技计划'
    print("栏目：", source2)
    chref_list = []
    req = requests.get(url)
    # 获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    item_list = soup.find_all('a', {'target': '_blank'})  # target="_blank"
    date_list = soup.find_all('div', {'class': 'time'})
    # print(len(item_list))
    for i in range(len(item_list)):
        item = item_list[i]
        href = item['href']
        title = item.text
        date = date_list[i].text
        if '../' in href:
            complete_href = 'http://www.most.gov.cn/' + href.replace('../', '')
        elif './' in href:
            complete_href = 'http://www.most.gov.cn/kjjh/' + href.replace('./', '')
        else:
            complete_href = href
        # print(complete_href, title, date)
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            print("该页面已存在")
            continue
        else:
            html, chard, html_str = getHtml_quiet(complete_href)
            html_name = saveHtml(title, html)
            # 获取附件（在分页面获取的）
            file_names = get_file(html_str, complete_href)
            save_excel(worksheet, row, title, title, html_name, source1,source2, date, complete_href, file_names)
            row = row + 1
    return row,chref_list

#国家科技部科技政策动态  静态网页
def kjzcdt_url(row,worksheet,url,href_bloom):
    source1 = '国家科技部'
    source2 = '科技政策动态'
    print("栏目：",source2)
    chref_list = []
    req = requests.get(url)
    # 获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    item_list = soup.find_all('a', {'target': '_blank'})  # target="_blank"
    # print(len(item_list))
    # print(date_list)
    for i in range(len(item_list)):
        item = item_list[i]
        href = item['href']
        title = item.text.split('(')[0]
        date = item.text.split('(')[-1][:-1]
        if '../' in href:
            complete_href = 'http://www.most.gov.cn/' + href.replace('../', '')
        elif './' in href:
            complete_href = 'http://www.most.gov.cn/kjzc/kjzcgzdt/' + href.replace('./', '')
        else:
            complete_href = href
        # print(complete_href, title, date)
        chref_list.append(complete_href)
        if complete_href in href_bloom:
            print("该页面已存在")
            continue
        else:
            html, chard, html_str = getHtml_quiet(complete_href)
            html_name = saveHtml(title, html)
            # 获取附件（在分页面获取的）
            file_names = get_file(html_str, complete_href)
            save_excel(worksheet, row, title, title, html_name, source1,source2, date, complete_href, file_names)
            row = row + 1
    return row ,chref_list

# def main(row ,worksheet,href_bloom):
#     href_list = []
#     #国家科技部通知通告
#     url1 = 'http://www.most.gov.cn/tztg/'
#     row,chref_list = tztg_url(row, worksheet, url1,href_bloom)
#     href_list.extend(chref_list)
#     #国家科技部科技部工作
#     url2 = 'http://www.most.gov.cn/kjbgz/'
#     row,chref_list = kjbgz_url(row,worksheet,url2,href_bloom)
#     href_list.extend(chref_list)
#     #国家科技部政府信息公开
#     url3 = 'http://www.most.gov.cn/mostinfo/xinxifenlei/zjgx/index.htm'
#     row,chref_list = xxgk_url(row, worksheet, url3,href_bloom)
#     href_list.extend(chref_list)
#     #国家科技部科技计划
#     url4 = 'http://www.most.gov.cn/kjjh/'
#     row,chref_list = kjjh_url(row,worksheet,url4,href_bloom)
#     href_list.extend(chref_list)
#     #国家科技部科技政策动态
#     url5 = 'http://www.most.gov.cn/kjzc/kjzcgzdt/'
#     row,chref_list = kjzcdt_url(row,worksheet,url5,href_bloom)
#     href_list.extend(chref_list)
#     print(row)
#     return row,href_list







