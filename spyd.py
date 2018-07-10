# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 21:05:35 2018

@author: GWT
"""

import requests
from bs4 import BeautifulSoup
#import json
import pandas as pd
import time
import random
import re

# 伪装头
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

#地区列表
diqu = ['dongcheng','xicheng','haidian']


#链家爬取
ljurl = 'https://bj.lianjia.com/ershoufang/'
houseInfo = []


for eachdiqu in diqu:
#获取地区最大页数
    url_diqu = ljurl + str(eachdiqu)
    res_diqu = requests.get(url_diqu,headers=headers).text
    soup_diqu = BeautifulSoup(res_diqu,'html.parser')
    housepages = soup_diqu.findAll('div',{'class':"page-box house-lst-page-box"})
    totalpage = int(re.findall('"totalPage":(.*?),"',str(housepages[0]),re.S)[0])
# 爬取每个地区的房屋信息
    for page in range(1,totalpage+1):
        url_diqupage = url_diqu+'pg%d/' %page
        district = eachdiqu
        res = requests.get(url_diqupage,headers=headers).text
        soup = BeautifulSoup(res,'html.parser')
        names= [i.text.split('/')[0].strip() for i in soup.select('.houseInfo')]
        houses= [i.text.split('/')[1].strip() for i in soup.select('.houseInfo')]
        lift = []
        for i in soup.select('.houseInfo'):
            if len(i.text.split('/'))==6:
                lift.append(i.text.split('/')[-1])
            else:
                lift.append(None)
        totalPrices= [i.text for i in soup.select('.totalPrice span') ]
        unitPrices= [i.text.lstrip('单价').rstrip('元/平米') for i in soup.select('.unitPrice span')]
        #每一页的信息拼接在列表中
        houseInfo.append(pd.DataFrame(dict(district = district,lift=lift, names=names,houses=houses,totalPrices =totalPrices,unitPrices =unitPrices))) 
        #循环等待，防止被杀
#        seconds = random.uniform(0.1,1)
#        time.sleep(seconds)
        print('爬完%s第%d页'%(eachdiqu,page))

# 把多页的list变成一个大的df，并保存为excel
housefile = pd.concat(houseInfo,ignore_index=True)
housefile.to_excel('C:/Users/GWT/pyfiles/lianjia/houseinfo.xlsx',index = False)


# 之前都是字符处理
import numpy as np
type(int(housefile['unitPrices'].tolist()[0]))

grouped = housefile['unitPrices'].groupby(housefile['district'])
grouped.size()
grouped.mean()



def towrite(df):
    housefile = pd.concat(df,ignore_index=True)
    housefile.to_excel('C:/Users/GWT/pyfiles/lianjia/houseinfo.xlsx',index = False)
    print('写好了')

def gethouseinfo(url):      
        res = requests.get(url,headers=headers).text
        soup = BeautifulSoup(res,'html.parser')
        names= [i.text.split('/')[0].strip() for i in soup.select('.houseInfo')]
        houses= [i.text.split('/')[1].strip() for i in soup.select('.houseInfo')]
        lift = []
        for i in soup.select('.houseInfo'):
            if len(i.text.split('/'))==6:
                lift.append(i.text.split('/')[-1])
            else:
                lift.append(None)
        totalPrices= [i.text for i in soup.select('.totalPrice span') ]
        unitPrices= [i.text.lstrip('单价').rstrip('元/平米') for i in soup.select('.unitPrice span')]
#        每一页的信息拼接在列表中
        houseInfo.append(pd.DataFrame(dict(lift=lift, names=names,houses=houses,totalPrices =totalPrices,unitPrices =unitPrices))) 
        print('爬完了')
#        towrite(houseInfo)
        #循环等待，防止被杀
#        seconds = random.uniform(0.1,1)
#        time.sleep(seconds)

#         return houseInfo
     
houseInfo = []
 
url = 'https://bj.lianjia.com/ershoufang/dongcheng/pg{}/'
urls = []
for i in range(1,20):
    urls.append(url.format(i))



gethouseinfo('https://bj.lianjia.com/ershoufang/dongcheng/pg1/')

from multiprocessing.dummy import Pool
import time

pool = Pool(4)
time1 = time.time()
result = pool.map(gethouseinfo,urls)
pool.close()
pool.join()
time2 = time.time()
print(str(time2-time1))


time3= time.time()
for i in urls:
    gethouseinfo(i)
time4 = time.time()
print(str(time4-time3))


towrite(houseInfo)



































