# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 14:36:36 2018

@author: nelson
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
data_all=pd.read_csv('../data_manage.csv',dtype='unicode',usecols=['M_TR_CURRENCY','M_SETTLEMENT_AMOUNT','M_TR_CARDSCHEME_ID','M_CARDTYPE',
                                                                   'M_TR_CARDBIN','M_CI_IPCOUNTRY','M_CI_IPCITY',
                                                                   'M_MS_SHOPPER_FACTOR','M_PAY_DURATION','M_CI_PLATFORM','M_ISFRAUD_CB','M_TR_DATETIME'])

#M_TR_CURRENCY无空值
#data_all['M_TR_CURRENCY']=data_all['M_TR_CURRENCY'].fillna('valuefill')
#currency_index=data_all[(data_all.M_TR_CURRENCY=='valuefill')].index.tolist()
#data_all=data_all.drop(currency_index)

#M_SETTLEMENT_AMOUNT空值121190条，是同一个商户的，可以去掉
data_all['M_SETTLEMENT_AMOUNT']=data_all['M_SETTLEMENT_AMOUNT'].fillna('0')
settlement_index=data_all[(data_all.M_SETTLEMENT_AMOUNT=='0')].index.tolist()
data_all=data_all.drop(settlement_index)

#CARDSCHEME_ID无空值
#data_all['M_TR_CARDSCHEME_ID']=data_all['M_TR_CARDSCHEME_ID'].fillna('0')
#cardscheme_index=data_all[(data_all.M_TR_CARDSCHEME_ID=='0')].index.tolist()

#M_CARDTYPE类型用1,2,3...表示，若有空值则用'NoType'填充
data_all['M_CARDTYPE']=data_all['M_CARDTYPE'].fillna('NoType')
cardtype_index=data_all[(data_all.M_CARDTYPE=='NoType')].index.tolist()


#M_TR_CARDBIN号空值有609952条，用'00000000'填充
data_all['M_TR_CARDBIN']=data_all['M_TR_CARDBIN'].fillna('00000000')
cardbin_index=data_all[(data_all.M_TR_CARDBIN=='00000000')].index.tolist()

#M_CI_IPCOUNTRY空值3001条，用'NoIpcountry'填充
data_all['M_CI_IPCOUNTRY']=data_all['M_CI_IPCOUNTRY'].fillna('NoIpcountry')
ipcountry_index=data_all[(data_all.M_CI_IPCOUNTRY=='NoIpcountry')].index.tolist()

#M_CI_TIMEZONE 空值253953条，由于类型太不统一（有数字有字符串），因此先不用这个列
#data_all['M_CI_TIMEZONE']=data_all['M_CI_TIMEZONE'].fillna('No')
#timezone_index=data_all[(data_all.M_CI_TIMEZONE=='No')].index.tolist()

#M_CI_IPCITY 空值 229554条 用'NoIpcity'填充
data_all['M_CI_IPCITY']=data_all['M_CI_IPCITY'].fillna('NoIpcity')
ipcity_index=data_all[(data_all.M_CI_IPCITY=='NoIpcity')].index.tolist()

#M_MS_SHOPPER_FACTOR空值1336
data_all['M_MS_SHOPPER_FACTOR']=data_all['M_MS_SHOPPER_FACTOR'].fillna('1')
shopperfactor_index=data_all[(data_all.M_MS_SHOPPER_FACTOR=='1')].index.tolist()

#M_PAY_DURATION  用均值填充
duration_mean=189475.5410296823 #求得的均值
data_all['M_PAY_DURATION']=data_all['M_PAY_DURATION'].fillna(duration_mean)
payduration_index=data_all[(data_all.M_PAY_DURATION ==duration_mean)].index.tolist()

#data_tmp=data_all[['M_PAY_DURATION']]
#data_tmp['M_PAY_DURATION']=data_tmp['M_PAY_DURATION'].astype(float)
#data_tmp=data_tmp.drop(payduration_index)
#duration_mean=data_tmp['M_PAY_DURATION'].mean()

#M_CI_PLATFORM　空值40W多 用'NoPlatform'填充
data_all['M_CI_PLATFORM']=data_all['M_CI_PLATFORM'].fillna('NoPlatform')
platform_index=data_all[(data_all.M_CI_PLATFORM=='NoPlatform')].index.tolist()

#M_ISFRAUD_CB 无空值
#data_all['M_ISFRAUD_CB']=data_all['M_ISFRAUD_CB'].fillna('NoCB')
#cb_index=data_all[(data_all.M_ISFRAUD_CB=='NoCB')].index.tolist()



#用字典方法将类别类型的数据改为数字
D_currency={}
D_currency_iter=0

D_cardtype={}
D_cardtype_iter=0

D_ipcountry={}
D_ipcountry_iter=0

D_ipcity={}
D_ipcity_iter=0

D_platform={}
D_platform_iter=0

a=data_all[['M_TR_CURRENCY','M_CARDTYPE','M_CI_IPCOUNTRY','M_CI_IPCITY','M_CI_PLATFORM']]
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
        a.iloc[i]['M_CARDTYPE']=D_cardtype.get(a.iloc[i]['M_CARDTYPE'])
        D_cardtype_iter+=1
    if a.iloc[i]['M_CI_IPCOUNTRY'] in D_ipcountry:
        a.iloc[i]['M_CI_IPCOUNTRY']=D_ipcountry.get(a.iloc[i]['M_CI_IPCOUNTRY'])
    else:
        D_ipcountry[a.iloc[i]['M_CI_IPCOUNTRY']]=D_ipcountry_iter #加入新字典
        a.iloc[i]['M_CI_IPCOUNTRY']=D_ipcountry.get(a.iloc[i]['M_CI_IPCOUNTRY'])
        D_ipcountry_iter+=1 
    if a.iloc[i]['M_CI_IPCITY'] in D_ipcity:
        a.iloc[i]['M_CI_IPCITY']=D_ipcity.get(a.iloc[i]['M_CI_IPCITY'])
    else:
        D_ipcity[a.iloc[i]['M_CI_IPCITY']]=D_ipcity_iter #加入新字典
        a.iloc[i]['M_CI_IPCITY']=D_ipcity.get(a.iloc[i]['M_CI_IPCITY'])
        D_ipcity_iter+=1 
    if a.iloc[i]['M_CI_PLATFORM'] in D_platform:
        a.iloc[i]['M_CI_PLATFORM']=D_platform.get(a.iloc[i]['M_CI_PLATFORM'])
    else:
        D_platform[a.iloc[i]['M_CI_PLATFORM']]=D_platform_iter #加入新字典
        a.iloc[i]['M_CI_PLATFORM']=D_platform.get(a.iloc[i]['M_CI_PLATFORM'])
        D_platform_iter+=1 
data_all[['M_TR_CURRENCY','M_CARDTYPE','M_CI_IPCOUNTRY','M_CI_IPCITY','M_CI_PLATFORM']]=a

#归一化
ss=StandardScaler()
scale_features=['M_TR_CURRENCY','M_SETTLEMENT_AMOUNT','M_TR_CARDSCHEME_ID','M_CARDTYPE','M_TR_CARDBIN','M_CI_IPCOUNTRY','M_CI_IPCITY','M_MS_SHOPPER_FACTOR','M_PAY_DURATION','M_CI_PLATFORM']
data_all[scale_features]=ss.fit_transform(data_all[scale_features])

#数据类型转换
data_all[['M_TR_CURRENCY', 'M_SETTLEMENT_AMOUNT', 'M_TR_CARDSCHEME_ID', 'M_CARDTYPE', 'M_TR_CARDBIN', 'M_CI_IPCOUNTRY', 'M_CI_PLATFORM', 'M_CI_IPCITY','M_MS_SHOPPER_FACTOR', 'M_PAY_DURATION','M_ISFRAUD_CB']]=data_all[['M_TR_CURRENCY', 'M_SETTLEMENT_AMOUNT', 'M_TR_CARDSCHEME_ID', 'M_CARDTYPE', 'M_TR_CARDBIN', 'M_CI_IPCOUNTRY', 'M_CI_PLATFORM', 'M_CI_IPCITY','M_MS_SHOPPER_FACTOR', 'M_PAY_DURATION','M_ISFRAUD_CB']].astype('float')