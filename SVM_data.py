# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 15:15:16 2018

@author: nelson
"""

#import numpy as np
#import re
import pandas as pd
from sklearn.preprocessing import StandardScaler
data_all=pd.read_csv('data_manage.csv',dtype='unicode',usecols=['M_TR_CARDSCHEME_ID','M_TR_CURRENCY','M_TR_AMOUNT','M_CARDTYPE','M_TR_CARDBIN',
                                                                'M_TR_RISK_RESULT','M_CI_OS','M_CI_IPCOUNTRY','M_MS_SHOPPER_FACTOR',
                                                                 'M_ISREVIEW','M_ISFRAUD_CB','M_CI_RESOLUTION','M_ISBLACKLIST','M_CI_ZIPCODE'])


#==============================================================================
#数据预处理
#cardbin去空值
data_all['M_TR_CARDBIN']=data_all['M_TR_CARDBIN'].fillna('valuefill')
cardbin_index=data_all[(data_all.M_TR_CARDBIN=='valuefill')].index.tolist()
data_all=data_all.drop(cardbin_index)
#风控结果去空值
data_all['M_TR_RISK_RESULT']=data_all['M_TR_RISK_RESULT'].fillna('valuefill')
risk_index=data_all[(data_all.M_TR_RISK_RESULT=='valuefill')].index.tolist()
data_all=data_all.drop(risk_index)
#OS去空值
data_all['M_CI_OS']=data_all['M_CI_OS'].fillna('valuefill')
os_index=data_all[(data_all.M_CI_OS=='valuefill')].index.tolist()
data_all=data_all.drop(os_index)
#支付方式去空值
#data_all['M_CI_PAYMENT_METHOD']=data_all['M_CI_PAYMENT_METHOD'].fillna('valuefill')
#paymethod_index=data_all[(data_all.M_CI_PAYMENT_METHOD=='valuefill')].index.tolist()
#data_all=data_all.drop(paymethod_index)
#平台去空值
#data_all['M_CI_PLATFORM']=data_all['M_CI_PLATFORM'].fillna('valuefill')
#platform_index=data_all[(data_all.M_CI_PLATFORM=='valuefill')].index.tolist()
#data_all=data_all.drop(platform_index)
#IP国家去空值
data_all['M_CI_IPCOUNTRY']=data_all['M_CI_IPCOUNTRY'].fillna('valuefill')
ipcountry_index=data_all[(data_all.M_CI_IPCOUNTRY=='valuefill')].index.tolist()
data_all=data_all.drop(ipcountry_index)
#购物者级别去空值
#data_all['M_CI_SHOPPERLEVEL']=data_all['M_CI_SHOPPERLEVEL'].fillna('valuefill')
#shopperlevel_index=data_all[(data_all.M_CI_SHOPPERLEVEL=='valuefill')].index.tolist()
#data_all=data_all.drop(shopperlevel_index)
#分辨率去空值
data_all['M_CI_RESOLUTION']=data_all['M_CI_RESOLUTION'].fillna('valuefill')
resolution_index=data_all[(data_all.M_CI_RESOLUTION=='valuefill')].index.tolist()
data_all=data_all.drop(resolution_index)
#黑名单去空值
data_all['M_ISBLACKLIST']=data_all['M_ISBLACKLIST'].fillna('valuefill')
blacklist_index=data_all[(data_all.M_ISBLACKLIST=='valuefill')].index.tolist()
data_all=data_all.drop(blacklist_index)

#进行one-hot编码
#oht_coding=pd.get_dummies(data_all[['M_TR_CURRENCY','M_CARDTYPE','M_TR_RISK_RESULT','M_CI_OS','M_CI_PAYMENT_METHOD','M_CI_IPCOUNTRY','M_CI_PLATFORM']])
#data_all=data_all.drop(data_all[['M_TR_CURRENCY','M_CARDTYPE','M_TR_RISK_RESULT','M_CI_OS','M_CI_PAYMENT_METHOD','M_CI_IPCOUNTRY','M_CI_PLATFORM']],axis=1)
#data_all=pd.concat([data_all,oht_coding],axis=1)



#购物者级别：非正常的数字的去除
#tmp=data_all['M_CI_SHOPPERLEVEL']
#tmp= tmp.apply(lambda x: False if len(x)>3 else True) #正常的值都是100以内,因此剔除3位数以上的
#data_all=data_all[tmp]

#包含NAN的值去除
data_all=data_all.dropna(axis=0,how='any')

#用字典方法将类别类型的数据改为数字
D_currency={}
D_currency_iter=0

D_cardtype={}
D_cardtype_iter=0

D_risk={}
D_risk_iter=0

D_os={}
D_os_iter=0

#D_paymethod={}
#D_paymethod_iter=0

D_ipcountry={}
D_ipcountry_iter=0


#D_platform={}
#D_platform_iter=0

D_resolution={}
D_resolution_iter=0
a=data_all[['M_TR_CURRENCY','M_CARDTYPE','M_TR_RISK_RESULT','M_CI_OS','M_CI_IPCOUNTRY','M_CI_RESOLUTION']]
for i in range(0,len(data_all)):
    if a.iloc[i]['M_TR_CURRENCY'] in D_currency:
        a.iloc[i]['M_TR_CURRENCY']=D_currency.get(a.iloc[i]['M_TR_CURRENCY'])
    else:
        D_currency[a.iloc[i]['M_TR_CURRENCY']]=D_currency_iter #加入新字典
        a.iloc[i]['M_TR_CURRENCY']=D_currency.get(a.iloc[i]['M_TR_CURRENCY'])
        D_currency_iter+=1
    if a.iloc[i]['M_CARDTYPE'] in D_cardtype:
        a.iloc[i]['M_CARDTYPE']=D_cardtype.get(a.iloc[i]['M_CARDTYPE'])
    else:
        D_cardtype[a.iloc[i]['M_CARDTYPE']]=D_cardtype_iter #加入新字典
        a.iloc[i]['M_CARDTYPE']=D_currency.get(a.iloc[i]['M_CARDTYPE'])
        D_cardtype_iter+=1
    if a.iloc[i]['M_TR_RISK_RESULT'] in D_risk:
        a.iloc[i]['M_TR_RISK_RESULT']=D_risk.get(a.iloc[i]['M_TR_RISK_RESULT'])
    else:
        D_risk[a.iloc[i]['M_TR_RISK_RESULT']]=D_risk_iter #加入新字典
        a.iloc[i]['M_TR_RISK_RESULT']=D_risk.get(a.iloc[i]['M_TR_RISK_RESULT'])
        D_risk_iter+=1
    if a.iloc[i]['M_CI_OS'] in D_os:
        a.iloc[i]['M_CI_OS']=D_os.get(a.iloc[i]['M_CI_OS'])
    else:
        D_os[a.iloc[i]['M_CI_OS']]=D_os_iter #加入新字典
        a.iloc[i]['M_CI_OS']=D_os.get(a.iloc[i]['M_CI_OS'])
        D_os_iter+=1 
#    if a.iloc[i]['M_CI_PAYMENT_METHOD'] in D_paymethod:
#        a.iloc[i]['M_CI_PAYMENT_METHOD']=D_paymethod.get(a.iloc[i]['M_CI_PAYMENT_METHOD'])
#    else:
#        D_paymethod[a.iloc[i]['M_CI_PAYMENT_METHOD']]=D_paymethod_iter #加入新字典
#        a.iloc[i]['M_CI_PAYMENT_METHOD']=D_paymethod.get(a.iloc[i]['M_CI_PAYMENT_METHOD'])
#        D_paymethod_iter+=1 
    if a.iloc[i]['M_CI_IPCOUNTRY'] in D_ipcountry:
        a.iloc[i]['M_CI_IPCOUNTRY']=D_ipcountry.get(a.iloc[i]['M_CI_IPCOUNTRY'])
    else:
        D_ipcountry[a.iloc[i]['M_CI_IPCOUNTRY']]=D_ipcountry_iter #加入新字典
        a.iloc[i]['M_CI_IPCOUNTRY']=D_ipcountry.get(a.iloc[i]['M_CI_IPCOUNTRY'])
        D_ipcountry_iter+=1 
#    if a.iloc[i]['M_CI_PLATFORM'] in D_platform:
#        a.iloc[i]['M_CI_PLATFORM']=D_platform.get(a.iloc[i]['M_CI_PLATFORM'])
#    else:
#        D_platform[a.iloc[i]['M_CI_PLATFORM']]=D_platform_iter #加入新字典
#        a.iloc[i]['M_CI_PLATFORM']=D_platform.get(a.iloc[i]['M_CI_PLATFORM'])
#        D_platform_iter+=1 
    if a.iloc[i]['M_CI_RESOLUTION'] in D_resolution:
        a.iloc[i]['M_CI_RESOLUTION']=D_resolution.get(a.iloc[i]['M_CI_RESOLUTION'])
    else:
        D_resolution[a.iloc[i]['M_CI_RESOLUTION']]=D_resolution_iter #加入新字典
        a.iloc[i]['M_CI_RESOLUTION']=D_resolution.get(a.iloc[i]['M_CI_RESOLUTION'])
        D_resolution_iter+=1 
data_all[['M_TR_CURRENCY','M_CARDTYPE','M_TR_RISK_RESULT','M_CI_OS','M_CI_IPCOUNTRY','M_CI_RESOLUTION']]=a        

#包含NAN的值去除
data_all=data_all.dropna(axis=0,how='any')

#数据类型转换
data_all[['M_MS_SHOPPER_FACTOR','M_ISREVIEW','M_ISFRAUD_CB','M_ISBLACKLIST']]=data_all[['M_MS_SHOPPER_FACTOR','M_ISREVIEW','M_ISFRAUD_CB','M_ISBLACKLIST']].astype('float')

#归一化
ss=StandardScaler()
scale_features=['M_TR_CARDSCHEME_ID','M_TR_AMOUNT','M_TR_CARDBIN','M_TR_CURRENCY','M_CARDTYPE','M_TR_RISK_RESULT','M_CI_OS','M_CI_IPCOUNTRY','M_CI_RESOLUTION','M_MS_SHOPPER_FACTOR','M_ISREVIEW']
data_all[scale_features]=ss.fit_transform(data_all[scale_features])

