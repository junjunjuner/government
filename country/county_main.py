# -*- coding:utf-8 -*-
#!~/anaconda3/bin/python
import os
import time
from pybloomfilter import BloomFilter
import datetime

import xlwt

import fagaiwei
import kejibu
import gongxinbu
import guowuyuan
import caizhengbu
import zhujianbu
import gdkejiting
import gdjinxinwei
import gdshangwu
import gdfagaiwei
import gdzhujianting
import zhgongxinju
import zhfagaiju
import zhzhujianju

#创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")

    else:
        print("---  There is this folder!  ---")


if __name__ == '__main__':
    ProgramStarttime = datetime.datetime.now()
    try:
        #创建文件夹调用
        file_ad1 = "/home/260199/爬虫/爬虫数据/政府公告/政府政策公告信息" + str(ProgramStarttime) + "/国家超链接/"
        mkdir(file_ad1)  # 调用函数

        all_href = []
        href_bloom = BloomFilter.open('/home/260199/爬虫/爬虫代码/政策公告/government/country/all_href.bloom')

        #创建excel表并编辑表头
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('国家级政府公告', cell_overwrite_ok=True)
        header = [u'标题', u'正文', u'发布部门',u'所在栏目', u'栏目类别',u'发布日期',u'爬取时间', u'政策链接', u'附件']
        i = 0
        # 写表头
        for each_header in header:
            worksheet.write(0, i, each_header)
            i += 1
        row = 1
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("国家工信部 数据开始收集，请稍等...")
        row,href_list = gongxinbu.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("国家科技部 数据开始收集，请稍等...")
        row,href_list = kejibu.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("国家发展改革委 数据开始收集，请稍等...")
        row,href_list = fagaiwei.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("国务院 数据开始收集，请稍等...")
        row,href_list = guowuyuan.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("国家财政部 数据开始收集，请稍等...")
        row,href_list = caizhengbu.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("国家住建部 数据开始收集，请稍等...")
        row,href_list = zhujianbu.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("广东省科学技术厅 数据开始收集，请稍等...")
        row,href_list = gdkejiting.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("广东省经济和信息化委员会 数据开始收集，请稍等...")
        row,href_list = gdjinxinwei.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("广东省商务厅 数据开始收集，请稍等...")
        row,href_list = gdshangwu.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("广东省发展和改革委员会 数据开始收集，请稍等...")
        row,href_list = gdfagaiwei.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("广东省住房和城乡建设厅 数据开始收集，请稍等...")
        row,href_list = gdzhujianting.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("珠海市科技和工业信息化局 数据开始收集，请稍等...")
        row,href_list = zhgongxinju.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("珠海市发展和改革局 数据开始收集，请稍等...")
        row,href_list = zhfagaiju.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("珠海市住房和城乡规划建设局 数据开始收集，请稍等...")
        row,href_list = zhzhujianju.main(row,worksheet,href_bloom,file_ad1,ProgramStarttime)
        all_href.extend(href_list)
        print("当前时间为：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("本次收集数据"+str(row-1)+"条")

        # href_bloom = BloomFilter(100000, 0.1, '/home/260199/爬虫/爬虫代码/政策公告/government/country/all_href.bloom')
        # href_bloom.update(all_href)
        print("布隆过滤器当前（运行后）长度为：",len(href_bloom))

        workbook.save("/home/260199/爬虫/爬虫数据/政府公告/政府政策公告信息" + str(ProgramStarttime)+"/政府政策公告.xlsx")
        with open('/home/260199/爬虫/爬虫代码/政策公告/government/country/success.txt', 'a') as file:
            file.write('\nsuccess ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        # href_bloom = BloomFilter(100000, 0.1, '/home/260199/爬虫/爬虫代码/政策公告/government/country/all_href_copy.bloom')
        # href_bloom.update(all_href)
    except Exception as e:
        print('最外层：',e)
        with open('/home/260199/爬虫/爬虫代码/政策公告/government/country/success.txt', 'a') as file:
            file.write('\nFail ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            file.write('报错原因为:'+str(e))