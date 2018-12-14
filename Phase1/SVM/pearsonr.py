from scipy.stats import pearsonr

from matplotlib import pyplot as plt


#每个特征值和预测结果的皮尔森相关系数
print ("M_TR_CURRENCY",pearsonr(data_all.iloc[:,0],data_all.iloc[:,11]))
print ("M_TR_AMOUNT",pearsonr(data_all.iloc[:,1],data_all.iloc[:,11]))
print ("M_TR_CARDSCHEME_ID",pearsonr(data_all.iloc[:,2],data_all.iloc[:,11]))
print ("M_CARDTYPE",pearsonr(data_all.iloc[:,3],data_all.iloc[:,11]))
print ("M_TR_CARDBIN",pearsonr(data_all.iloc[:,4],data_all.iloc[:,11]))
print ("M_TR_RISK_RESULT",pearsonr(data_all.iloc[:,5],data_all.iloc[:,11]))
print ("M_CI_IPCOUNTRY",pearsonr(data_all.iloc[:,6],data_all.iloc[:,11]))
print ("M_CI_OS",pearsonr(data_all.iloc[:,7],data_all.iloc[:,11]))
print ("M_CI_RESOLUTION",pearsonr(data_all.iloc[:,8],data_all.iloc[:,11]))
print ("M_MS_SHOPPER_FACTOR",pearsonr(data_all.iloc[:,9],data_all.iloc[:,11]))
print ("M_ISREVIEW",pearsonr(data_all.iloc[:,12],data_all.iloc[:,11]))


#画图展示
y=[]
for i in range(0,10):
    t=(pearsonr(data_all.iloc[:,i],data_all.iloc[:,11] ))[0]
    y.append(round(t,4))
t=(pearsonr(data_all.iloc[:,12],data_all.iloc[:,11] ))[0]
y.append(round(t,4))
x= ['1','2','3','4','5','6','7','8','9','10','11']

index=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
index=[float(c)+1 for c in index]
rects=plt.bar(range(len(y)), y, color='rgby')
plt.ylim(ymax=0.03, ymin=-0.03)
plt.ylabel("pearsonr")
plt.xlabel("features")
plt.xticks(index, x)
for rect in rects:
    height = rect.get_height()
#    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')
plt.show()