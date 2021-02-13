# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:48:10 2021

@author: LiChengyi
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page_content(request_url):
    # 得到页面的内容
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(request_url,headers=headers,timeout= 10)
    content = html.text

    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
#    soup = BeautifulSoup(content, 'html.parser')
    return soup


def analysis(soup):
    
    # 找到完整的投诉信息框
    temp = soup.find('div',class_='tslb_b')
 
    # 创建DataFrame
    df = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', \
                               'problem','datetime','status'])

    #找出所有的tr，即行
    tr_list = temp.find_all('tr')
    
    for tr in tr_list:
        temp={}
        td_list = tr.find_all('td')
        # 如果没有td,就是表头(th)
        if len(td_list) > 0:
            # 投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态
            id, brand, car_model, type, desc, problem, datetime, status = \
                td_list[0].text,td_list[1].text,td_list[2].text,td_list[3].text, td_list[4].text, \
                    td_list[5].text,td_list[6].text,td_list[7].text    
           # print(id,brand,car_model,type,desc,problem,datetime,status)

            temp['id']= id
            temp['brand']= brand
            temp['car_model']= car_model
            temp['type']= type
            temp['desc']= desc
            temp['problem']= problem
            temp['datetime'] = datetime
            temp['status']= status
            # 注意基础代码
            df = df.append(temp, ignore_index=True)
    return df

# 创建DataFrame
result = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', \
                               'problem','datetime','status'])

# 请求URL
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'
page_num = 5

for i in range(page_num):
    #拼接当前的页面URL
    request_url = base_url + str( i + 1) + '.shtml'
    #得到soup解析
    soup = get_page_content(request_url)
    #通过soupe解析，得到当前页的dataframe
    df = analysis(soup)
    result = result.append(df)
    #time.sleep(1)
    
# print(result)
#result.to_csv('car_complain.csv',index=False)
result.to_excel('car_complain.xlsx',index=False)