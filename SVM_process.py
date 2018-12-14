# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:57:21 2018

@author: nelson
"""

from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import model_selection
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
from collections import Counter #查看标签；类别
from imblearn.over_sampling import SMOTE
#==============================================================================
#SVM分类器
x=pd.concat([data_all.iloc[0:200000,0:10],data_all.iloc[0:200000,12]],axis=1)
y=data_all.iloc[0:200000,11]
#数据不平衡imblearn算法，解决某个类别数据量少的问题
smo = SMOTE(random_state=42)
x_smo, y_smo = smo.fit_sample(x, y)
#训练集与测试集划分
x_train, x_test, y_train, y_test = model_selection.train_test_split(x_smo, y_smo, random_state=3, train_size=0.6)
#训练svm分类器
#clf = svm.SVC(C=0.1, kernel='linear', decision_function_shape='ovr')
clf = svm.SVC(C=0.1, kernel='rbf', decision_function_shape='ovr')
clf.fit(x_train, y_train.ravel())
#计算SVC分类器的准确率
y_hat = clf.predict(x_test)
print("svm accuracy_score",accuracy_score(y_test, y_hat)) #准确率

conf_mat = confusion_matrix(y_test, y_hat) #混淆矩阵
print(conf_mat)
print("svm classification report")
print(classification_report(y_test, y_hat))