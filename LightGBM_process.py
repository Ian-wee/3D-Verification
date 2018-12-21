# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 10:20:28 2018

@author: nelson
"""

 
 
import lightgbm as lgb
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

x1=pd.concat([data_all.iloc[0:500000,0:2],data_all.iloc[0:500000,3:10]],axis=1)
x=pd.concat([x1,data_all.iloc[0:500000,11]],axis=1)
y=data_all.iloc[0:500000,10]
#数据不平衡imblearn算法，解决某个类别数据量少的问题
smo = SMOTE(random_state=42)
x_smo, y_smo = smo.fit_sample(x, y)

x_train=x_smo
y_train=y_smo


#测试集选择
#x_test1=pd.concat([data_all.iloc[500000:1632432,0:2],data_all.iloc[500000:1632432,3:10]],axis=1)
#x_test=pd.concat([x_test1,data_all.iloc[500000:1632432,11]],axis=1)
#y_test=data_all.iloc[500000:1632432,10]

x_test1=pd.concat([data_all2.iloc[:,0:2],data_all2.iloc[:,3:10]],axis=1)
x_test=pd.concat([x_test1,data_all2.iloc[:,11]],axis=1)
y_test=data_all2.iloc[:,10]


# 创建成lgb特征的数据集格式
lgb_train = lgb.Dataset(x_train, y_train.ravel()) # 将数据保存到LightGBM二进制文件将使加载更快
lgb_eval = lgb.Dataset(x_test,y_test, reference=lgb_train)  # 创建验证数据


# 回归参数
#params = {
#    'task': 'train',
#    'boosting_type': 'gbdt',  # 设置提升类型
#    'objective': 'regression', # 目标函数
##    'num_class':2,
#    'metric': {'l2','auc'},  # 评估函数
#    'num_leaves': 31,   # 叶子节点数
#    'learning_rate': 0.05,  # 学习速率
#    'feature_fraction': 0.9, # 建树的特征选择比例
#    'bagging_fraction': 0.8, # 建树的样本采样比例
#    'bagging_freq': 5,  # k 意味着每 k 次迭代执行bagging
#    'verbose': 1# <0 显示致命的, =0 显示错误 (警告), >0 显示信息
#}
 
print('Start training...')
#分类器参数
params = {'boosting_type': 'gbdt',
          'objective': 'multiclass',
          'nthread': -1,
          'silent': True,#是否打印信息，默认False
          'learning_rate': 0.1,
          'num_leaves': 80,
          'max_depth': 5,
          'max_bin': 127,
          'subsample_for_bin':50000,
          'subsample': 0.8,
          'subsample_freq': 1,
          'colsample_bytree': 0.8,
          'reg_alpha': 1,
          'reg_lambda': 0,
          'min_split_gain': 0.0,
          'min_child_weight': 1,
          'min_child_samples': 20,
          'scale_pos_weight': 1}
          
estimator=lgb.sklearn.LGBMClassifier(n_estimators=2000 , seed=3)
estimator.fit(x_train, y_train.ravel())

# 训练 cv and train
#gbm = lgb.train(params,lgb_train,num_boost_round=20,valid_sets=lgb_eval,early_stopping_rounds=5) # 训练数据需要参数列表和数据集
 
#print('Save model...') 
 
#gbm.save_model('model.txt')   # 训练后保存模型到文件
 
print('Start predicting...')
# 预测数据集
#y_pred = gbm.predict(x_test, num_iteration=gbm.best_iteration) #如果在训练期间启用了早期停止，可以通过best_iteration方式从最佳迭代中获得预测
y_pred = estimator.predict(x_test)

#结果处理
#for i in range(0,len(y_pred)):
#    if y_pred[i]>0.50:
#        y_pred[i]=1
#    else:
#        y_pred[i]=0
#    i+=1

# 评估模型
print("lightGBM accuracy_score",accuracy_score(y_test, y_pred)) #准确率
conf_mat = confusion_matrix(y_test, y_pred) #混淆矩阵
print(conf_mat)
print("lightGBM classification report")
print(classification_report(y_test, y_pred))
