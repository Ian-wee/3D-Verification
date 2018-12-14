# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 11:29:44 2018

@author: nelson
"""

#import cx_Oracle
import pandas as pd
import math
import re
import numpy as np
#==============================================================================
#数据库直接连接方法，速度较慢
# username="data"
# userpwd="data2017pwd"
# host="192.168.0.139"
# port=1521
# dbname="ORCL"
# dsn=cx_Oracle.makedsn(host, port, dbname)
# db=cx_Oracle.connect(username, userpwd, dsn) 
# sql_select="SELECT m_tr_no,m_ms_shopper_factor,m_ci_shopperlevel,m_isblacklist,m_ci_platform,"\
#          +"m_ci_payment_method,m_tr_cardbin,m_ci_ipcountry,m_ci_ipcity FROM data_manage WHERE rownum < 200000" #读取data_manage表格数据
# data_all = pd.read_sql(sql_select,db)
# #print(data_all.columns) 
# #print(data_all['M_ISBLACKLIST'],data_all["M_CI_IPCITY"])
# print(data_all.size)
#==============================================================================
def calcul_bin_black(cardbin,data):
   count=0
   for i in range(0,len(data)):
     flag=0
     card_no=(data.iloc[i]['BV_VALUE'])[0:6]
     if '*' in card_no: #判断是否存在*号
         card_no=(data.iloc[i]['BV_VALUE'])[0:4] #卡号中间有*符号，进行截取，否则报错
         flag=1
     tmp= re.match(card_no,str(cardbin)) #正则字符串匹配
     if tmp is None: #如果是空查找结果则退出循环
         continue
     elif len(tmp.group(0)) == 6 and flag == 0: #case 1:卡号显示前6位，并且6位卡BIN都匹配到
       # print('1')
        count+=1
     elif len(tmp.group(0)) == 4 and flag == 1: #case 2:卡号显示前4位，并且4位卡BIN都匹配到
       # print('0.8')
        count+=0.8
   return count
def country_city_cb(country,city,data):
    result=[]
    data_country_city=data[['M_CI_IPCOUNTRY','M_CI_IPCITY','M_ISCHARGEBACK','M_TR_STATUS']][data.M_CI_IPCOUNTRY==country] #dataframe的列筛选,按范围大的国家维度进行筛选即可
    country_success=0 #IP国家成功订单
    country_cb=0 #IP国家失败订单
    city_success=0 #IP城市成功订单
    city_cb=0 #IP城市失败订单
    for i in  range(0,len(data_country_city)):
        if data_country_city.iloc[i]['M_TR_STATUS']==1: #国家成功交易的订单
            country_success+=1
            if data_country_city.iloc[i]['M_ISCHARGEBACK']==1: #国家发生拒付
                country_cb+=1
        if data_country_city.iloc[i]['M_CI_IPCITY']==city:
            if data_country_city.iloc[i]['M_TR_STATUS'] ==1 :#城市成功交易订单
                city_success+=1
                if data_country_city.iloc[i]['M_ISCHARGEBACK']==1: #城市发生拒付
                    city_cb+=1
    if country_success==0: #成功订单数为0的情况予以区别
        country_cb_rate=np.nan
    else:
        country_cb_rate=round( (float(country_cb)/float(country_success)) , 5 )#结果保留五位小数
    result.append(country_cb_rate) #加入result中
    if city_success==0:#成功订单数为0的情况予以区别
        city_cb_rate=np.nan
    else:
        city_cb_rate=round((float(city_cb)/float(city_success)),5)#结果保留五位小数
    result.append(city_cb_rate) #加入result中
    return result
def plat_method_cb(platform,paymethod,data):
    result=[]
    data_platform_paymethod=data.loc[(data['M_CI_PLATFORM']==platform)|(data['M_CI_PAYMENT_METHOD']==paymethod)]#dataframe选取特定列，选取特定列值等于platform,paymethod
    platform_success=0 #平台成功订单
    platform_cb=0 #平台失败订单
    paymethod_success=0 #支付方式成功订单
    paymethod_cb=0 #支付方式失败订单
    for i in range (0,len(data_platform_paymethod)):
        if data_platform_paymethod.iloc[i]['M_CI_PLATFORM']==platform:
            if data_platform_paymethod.iloc[i]['M_TR_STATUS']==1: #平台交易成功订单
                platform_success+=1
                if data_platform_paymethod.iloc[i]['M_ISCHARGEBACK']==1: #平台发生拒付
                    platform_cb+=1
        if data_platform_paymethod.iloc[i]['M_CI_PAYMENT_METHOD']==paymethod:
            if data_platform_paymethod.iloc[i]['M_TR_STATUS']==1: #支付方式交易成功订单
                paymethod_success+=1
                if data_platform_paymethod.iloc[i]['M_ISCHARGEBACK']==1:#支付方式发生拒付
                    paymethod_cb+=1
    if platform_success==0: #成功订单数为0的情况予以区别
        platform_cb_rate=np.nan
    else:
        platform_cb_rate=round( (float(platform_cb)/float(platform_success)) , 5 ) #结果保留五位小数
    result.append(platform_cb_rate)
    if paymethod_success ==0: #成功订单数为0的情况予以区别
        paymethod_cb_rate=np.nan
    else:
        paymethod_cb_rate=round( (float(paymethod_cb)/float(paymethod_success)) , 5 )
    result.append(paymethod_cb_rate)
    return result
def cardbin_cb(cardbin,data):
    data_cardbin=data[['M_ISCHARGEBACK','M_TR_STATUS']][data.M_TR_CARDBIN==cardbin] #列筛选+选取卡BIN等于cardbin的行数据
    cardbin_success=0
    cardbin_cb=0
    for i in range(0,len(data_cardbin)):
        if data_cardbin.iloc[i]['M_TR_STATUS']==1: #卡BIN号对应交易成功订单
            cardbin_success+=1
            if data_cardbin.iloc[i]['M_ISCHARGEBACK']==1: #卡BIN号对应交易发生拒付
                cardbin_cb+=1
    if cardbin_success==0:
        cardbin_rate=np.nan
    else:
        cardbin_rate=round( (float(cardbin_cb)/float(cardbin_success)) , 5 )
    return cardbin_rate
data_all=pd.read_csv('data_manage.csv',usecols=['M_TR_NO','M_MS_SHOPPER_FACTOR','M_CI_PLATFORM','M_CI_PAYMENT_METHOD','M_TR_CARDBIN','M_CI_IPCOUNTRY','M_CI_IPCITY','M_ISCHARGEBACK','M_TR_STATUS','M_TR_REQ_3D_FLAG'])
black_list=pd.read_csv('black_element.csv') #读取黑名单表
black_total=len(black_list) #黑名单总记录数
#权重总和为100
standard=9*(1.846/100)+21*0+15*0.015+15*0.015+22*0.015+9*0.015+9*0.015 #用户信用再除以100，使得和其他指标达到同一个量级
#print(black_list.columns)
#print(data_df.shape)
#print(data_df.columns)
#print(type(data_df['M_MS_SHOPPER_FACTOR'].iat[0:]))
#data_all[['M_TR_CARDBIN']]=data_all[['M_TR_CARDBIN']].astype('float64')
#user_factor=data_all['M_MS_SHOPPER_FACTOR'].irow(-1) #用户信用系数
#card_bin=data_all['M_TR_CARDBIN'].tail(100) #卡BIN号
selected_data=data_all.tail(5) #选取末尾订单
for i in range(0,len(selected_data)):
    if math.isnan(selected_data.iloc[i]['M_TR_CARDBIN']): #如果卡BIN号为空，则不进行高危检测算法
        print("Trade：",selected_data.iloc[i]['M_TR_NO'],"has no cardbin number!")
    else:
        print("进行高危检测算法ing")
        user_factor=selected_data.iloc[i]['M_MS_SHOPPER_FACTOR'] #用户信用系数
        print('user_factor:',user_factor)
        black_bin=calcul_bin_black(selected_data.iloc[i]['M_TR_CARDBIN'],black_list) #卡BIN号对应的黑名单数量
        black_rate=round( (float(black_bin)/float(black_total)) , 5 ) #卡BIN号对应的黑名单数/黑名单记录总数
        print('black_carbin_rate:',black_rate)
        #IP所在城市、国家对应的拒付率
        location_related_rate=country_city_cb(selected_data.iloc[i]['M_CI_IPCOUNTRY'],selected_data.iloc[i]['M_CI_IPCITY'],data_all)
        print('city:',location_related_rate[1],'country:',location_related_rate[0])
        #平台、支付方式所对应的拒付率
        merchant_related_rate=plat_method_cb(selected_data.iloc[i]['M_CI_PLATFORM'],selected_data.iloc[i]['M_CI_PAYMENT_METHOD'],data_all)
        print('platform:',merchant_related_rate[0],'paymethod:',merchant_related_rate[1])
        #卡BIN号所对应的拒付率
        cardbin_rate=cardbin_cb(selected_data.iloc[i]['M_TR_CARDBIN'],data_all)
        print('cardbin_rate',cardbin_rate)
#==============================================================================
        factor_transform=round((user_factor/100),5) #用户信用系数转换
        if math.isnan(merchant_related_rate[0]):#平台对应的拒付率不存在(该平台的第一笔交易)的情况
            overall_result=11*factor_transform+23*black_rate+11*location_related_rate[1]+11*location_related_rate[0]+17*merchant_related_rate[1]+25*cardbin_rate
        else:
            overall_result=9*factor_transform+21*black_rate+9*location_related_rate[1]+9*location_related_rate[0]+15*merchant_related_rate[0]+15*merchant_related_rate[1]+22*cardbin_rate
        print('overall_result:',overall_result)
        if overall_result > standard: #如果超过了standard的评价标准的值，就会开启3D验证
            print('需要进行3D验证')
            data_all.iloc[-(2-i)]['M_TR_REQ_3D_FLAG']=1 #修改字段值