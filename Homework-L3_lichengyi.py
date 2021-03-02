# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 21:20:54 2021

@author: LiChengyi
"""


from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.cluster import KMeans, AgglomerativeClustering


df = pd.read_csv('car_data.csv',encoding='gbk')

# 简单的数据探索，确认不需要清洗
df.head()
df.info()
df.describe()


# 数据规范化到 [0,1] 空间
train_x = df[["人均GDP","城镇人口比重", "交通工具消费价格指数","百户拥有汽车量"]]
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
pd.DataFrame(train_x)


# 改进版K-Means 手肘法：自动估计划分为几组比较好
sse = []
N = 11
for n in range(1, N):
	# kmeans算法
	kmeans = KMeans(n_clusters=n)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, N)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()

# 自动估计手肘法的最佳分组数
# 把sse相邻元素的差值(即斜率），赋给temp
temp = []
for i in range(1,len(sse)):
    temp.append(sse[i-1]-sse[i])
# 把temp相邻元素的环比(即斜率变化率），赋给temp2
temp2 = []
for i in range(1,len(temp)):
    temp2.append((temp[i]-temp[i-1])/temp[i-1])

# 当temp2中首次出现绝对值<10%的数时，认为斜率已经变化不明显了，找到最佳分组数
for i in range(0,len(temp2)-1):
    if abs(temp2[i])<0.1:
        k=i+1
        break
    else:
        pass
    
# 以上算法判断 K=6是最佳分组
# 但是人工判断，K=5是最佳分组？  自动算法不合理？？

# 使用KMeans聚类
kmeans = KMeans(n_clusters=k)
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((df,pd.DataFrame(predict_y)+1),axis=1)
result.rename({0:u'聚类结果 K=%s' % k},axis=1,inplace=True)
print(result)
# 将结果导出到CSV文件中
result.to_csv("car_data_聚类后.csv",index=False,encoding='gbk')
print('结果已经完成聚类，并且保存为car_data_聚类后.csv')
