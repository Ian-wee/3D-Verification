# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 08:35:49 2018

@author: nelson
"""

from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

#x1=pd.concat([data_all.iloc[0:700000,0:2],data_all.iloc[0:700000,3:10]],axis=1)
#x=pd.concat([x1,data_all.iloc[0:700000,11]],axis=1)
#y=data_all.iloc[0:700000,10]
x1=pd.concat([data_all.iloc[:1000000,0:2],data_all.iloc[:1000000,3:10]],axis=1)
x=pd.concat([x1,data_all.iloc[:1000000,11]],axis=1)
y=data_all.iloc[:1000000,10]
#数据不平衡imblearn算法，解决某个类别数据量少的问题
smo = SMOTE(random_state=42,ratio=0.4)
x_smo, y_smo = smo.fit_sample(x, y)

#x_train=x_smo
#y_train=y_smo


#测试集选择
x_test1=pd.concat([data_all.iloc[1200000:1632432,0:2],data_all.iloc[1200000:1632432,3:10]],axis=1)
x_test=pd.concat([x_test1,data_all.iloc[1200000:1632432,11]],axis=1)
y_test=data_all.iloc[1200000:1632432,10]



#训练模型，限制树的最大深度4
clf=DecisionTreeClassifier(criterion='entropy',max_depth=4)
#拟合模型
clf.fit(x_train,y_train)

y_pred=clf.predict(x_test)

#交叉验证
#scores = cross_val_score(clf, x_smo, y_smo, cv=10)
#scores.mean()

# 评估模型
print("DT accuracy_score",accuracy_score(y_test, y_pred)) #准确率
conf_mat = confusion_matrix(y_test, y_pred) #混淆矩阵
print(conf_mat)
print("DT classification report")
print(classification_report(y_test, y_pred))


#对判断为欺诈拒付的订单，根据其国家3D成功率权衡是否开启3D
index=[]
for i in range(0,len(y_pred)):
    if(y_pred[i]==1.0):
        index.append(1200000+i)
    i+=1
data_all2=data_all.iloc[index]
