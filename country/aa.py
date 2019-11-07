# # x = []
# # x = x.extend(['aa'])
# # print(x)
# # import time
# # from pybloomfilter import BloomFilter
# # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# # print("当前时间为：",current_time )
# # href_bloom = BloomFilter(100000, 0.1, 'all_href.bloom')
#
# # x=['~.doc','~~.doc','~~~.doc']
# # file_name = '~.doc'
# # file_adds = 'doc'
# # print(file_name.rstrip('.' + file_adds))
# # while file_name in x:
# #     file_name = file_name.rstrip('.' + file_adds) + '~.' + file_adds
# # print(file_name)
#
# import requests
# import re
# import urllib.request
# import chardet
# from bs4 import BeautifulSoup as beautiful
# from pybloomfilter import BloomFilter
#
# href_bloom = BloomFilter.open('all_href.bloom')
# url = 'http://www.gdstc.gov.cn/zwgk/tzgg/index@1.htm'
# source1 = '广东省科学技术厅'
# source2 = '通知公告'
# print("栏目：", source2)
# chref_list = []
# req = requests.get(url)
# # 获取网页编码格式
# response = urllib.request.urlopen(url).read()
# chardit1 = chardet.detect(response)
# chardit = chardit1['encoding']
# print("编码格式" + chardit)
# # 获取分页面url
# req.encoding = chardit1['encoding']
# soup = beautiful(req.text, 'lxml')
# td = soup.find('td', {'align': 'center'})
# href_list = re.findall('<a class="main" href="(.*?)" target="_blank">(.*?)</a></td><td align="right" width="80">(.*?)</td>', str(td))
# for i in range(len(href_list)):
#     date = href_list[i][-1]
#     href = 'http://www.gdstc.gov.cn' + href_list[i][0]
#     down_href = href.rstrip(href.split('/')[-1])
#     title = href_list[i][1]
#     print(href,title,date)
# # for item in item_list:
# #     href = re.findall('href="(.*?)"', str(item))[0]
# #     title = re.findall('target="_blank">(.*?)</a>', str(item))[0]
# #     date = re.findall('</a>\((.*?)\)', str(item))[0]
# #     print(href,title,date)
#     # if '../' in href:
#     #     complete_href = 'http://www.most.gov.cn/' + href.replace('../', '')
#     # elif './' in href:
#     #     complete_href = url + href.replace('./', '')
#     # else:
#     #     complete_href = href
#     # print(complete_href)

# import os
# import time
# #创建文件夹
# def mkdir(path):
#     folder = os.path.exists(path)
#     if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
#         os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
#         print("---  new folder...  ---")
#         print("---  OK  ---")
#
#     else:
#         print("---  There is this folder!  ---")
#
#
# ProgramStarttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# #创建文件夹调用
# file_ad1 = "/home/260199/爬虫/爬虫数据/政府公告/政府政策公告信息"+str(ProgramStarttime)+"/国家超链接/"
# mkdir(file_ad1)  # 调用函数
import re
complete_href = 'http://www.most.gov.cn/mostinfo/xinxifenlei/zfwzndbb/201805/P020180521574636090470.pdf'
if re.search(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$',complete_href):
    print(True)
else:
    print(False)