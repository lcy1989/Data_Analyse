import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from efficient_apriori import apriori
import time

# 设置最大显示行数
pd.set_option('max_columns', None)

# header=None，不将第一行作为head
data = pd.read_csv('./Market_Basket_Optimisation.csv', header = None) 
# shape为(7501,20)
print(data.shape)



# ——————————使用efficient_apriori工具包————————————
print('_'*30+'方法1：使用efficient_apriori工具包'+'_'*30)
start = time.time()
# 将所有数据存放到transactions中
transactions = []
# 按照行进行遍历
for i in range(0, data.shape[0]):
    # 建立空list，记录每一行的Transaction
    temp = []
    # 按照列进行遍历
    for j in range(0, data.shape[1]):
        if str(data.values[i, j]) != 'nan':
            temp.append(str(data.values[i, j]))
    transactions.append(temp)
# print(transactions)

# 挖掘频繁项集和频繁规则
# 这里需要手工调试最小支持度和最小置信度的取值
frequent_itemsets1, rules1 = apriori(transactions, min_support=0.05,  min_confidence=0.2)
print("频繁项集：", frequent_itemsets1)
print("关联规则：", rules1)
end = time.time()
print("用时：", end-start)

    
# ——————————采用mlxtend.frequent_patterns工具包________
print('_'*30+'采用mlxtend.frequent_patterns工具包'+'_'*30)
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
pd.options.display.max_columns=100
start = time.time()

# 对数据进行one-hot编码。   由于原数据只有商品名，需要进行数据处理，
# 1、创建一个空的DataFrame
df = pd.DataFrame()
df['TransactionID'] = range(1,data.shape[0]+1)
df['Items'] = range(1,data.shape[0]+1)

# 2、把data每一行的商品名合并成 df的Items列
for i in range(0,data.shape[0]):
    df.loc[i,'Items'] = data.loc[i,:].str.cat(sep='/')

# 3、用get dummies进行one-hot编码    
df_hot_encoded = df.drop('Items',1).join(df.Items.str.get_dummies('/'))
df_hot_encoded.set_index(['TransactionID'],inplace=True)   

# 挖掘频繁项集和频繁规则
frequent_itemsets2 = apriori(df_hot_encoded, min_support=0.05, use_colnames=True)
frequent_itemsets2 = frequent_itemsets2.sort_values(by="support" , ascending=False) 
print('-'*20, '频繁项集', '-'*20)
print("频繁项集：", frequent_itemsets2)

rules2 = association_rules(frequent_itemsets2, metric="confidence", min_threshold=0.2)
rules2 = rules2.sort_values(by="lift" , ascending=False) 
print('-'*20, '关联规则', '-'*20)
print("关联规则：", rules2)

end = time.time()
print("用时：", end-start)









