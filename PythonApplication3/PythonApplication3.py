# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 13:31:50 2018

@author: zhang
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import os

sns.set_style("whitegrid")
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

def sub_plt(x,y,labelname,filename,ylabel,xrange):
    plt.show()
    for i in range(0,len(y[1])):
        if i == 0:
            plt.plot(x,y[:,i],label=labelname[i],linewidth=2.0)
        elif i == 1:
            plt.plot(x,y[:,i],label=labelname[i],linestyle='--',linewidth=2.0)
        elif i == 2:
            plt.plot(x,y[:,i],label=labelname[i],linestyle='-.',linewidth=2.0)
        elif i == 3:
            plt.plot(x,y[:,i],label=labelname[i],linestyle=':',linewidth=2.0)
        elif i >= 4:
            plt.plot(x,y[:,i],label=labelname[i],linestyle='-.',linewidth=1.2)
    plt.grid(True)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim([0,max(x)])
    if not xrange == 0:
        plt.xlim([0,xrange])
    plt.xlabel('时间/s',fontsize=15)
    plt.ylabel(ylabel,fontsize=15)
    plt.legend(prop={'size':15},  loc='lower right')
    if len(y[1])>3:
        plt.legend(loc='lower right',prop={'size':11})
    plt.savefig(filename,bbox_inches='tight',pad_inches=0.00)

def mkdir(path):
    floder = os.path.exists(path)
    if not floder:
        os.makedirs(path)
    return

def import_data(filename,flag):
    data=[]
    if flag ==1:
        row=221
        col=21
    elif flag ==2:
        row=122
        col=10
        
    with open(filename,'r') as f:
        file_data = f.readlines()
    
    for i in range(0,len(file_data)-1-row):
        for j in range(0,col):
            temp=float(file_data[i+row].split()[j])
            data.append(temp)
    
    data=np.array(data)
    data=data.reshape(-1,col)
    return data

def yrange(y,flag):
    if flag in [1]:#流量，[416,46,27.8,17.6,8.5]
        y.max()-y.min()

def ppp(data,flag,filename):
    if flag == 1:
       name='环路流量'
       ylabel_name='流量/%(相对于417kg$\cdot$s$^{-1}$)'
       index=[1,2]
       legend_name=['环路1','环路2']
       p=data[:,index]/417.04*100#归一百分比
    elif flag == 2:
       name='热管段温度'
       ylabel_name='温度/$^\circ$C'
       index=[3,6]
       legend_name=['环路1','环路2']
       p=data[:,index]-273.15
    elif flag == 3:
        name='冷管段温度'
        ylabel_name='温度/$^\circ$C'
        index=[4,7]
        legend_name=['环路1','环路2']
        p=data[:,index]-273.15
    elif flag == 4:
        name='冷却剂平均温度'
        ylabel_name='温度/$^\circ$C'
        index=[5,8]
        legend_name=['环路1','环路2']
        p=data[:,index]-273.15
    elif flag == 5:
        name='稳压器压力'
        ylabel_name='压力/MPa'
        index=[9]
        legend_name=['稳压器']
        p=data[:,index]
    elif flag == 6:
        name='稳压器水位'
        ylabel_name='高度/%(相对于5.5m)'
        index=[10]
        legend_name=['稳压器']
        p=data[:,index]/5.5*100
    elif flag == 7:
        name='蒸汽流量'
        ylabel_name='流量/%(相对于40kg$\cdot$s$^{-1}$)'
        index=[11,12,13]
        legend_name=['SG1','SG2','给水']
        p=data[:,index]/40*100
    elif flag == 8:
        name='蒸汽温度'
        ylabel_name='温度/$^\circ$C'
        index=[14,15]
        legend_name=['SG1','SG2']
        p=data[:,index]-273.15
    elif flag == 9:
        name='SG水位'
        ylabel_name='高度/%(相对于额定的3.7m)'
        index=[16,17]
        legend_name=['SG1','SG2']
        p=data[:,index]/3.7*100
    elif flag == 10:
        name='蒸汽压力'
        ylabel_name='压力/MPa'
        index=[18,19,20]
        legend_name=['SG1','SG2','母管']
        p=data[:,index]
    elif flag == 11:
        name='SG功率'
        ylabel_name='功率/%(相对于75MW)'
        index=[1,2]
        legend_name=['SG1','SG2']
        p=data[:,index]/1e6/74.475*100
    elif flag == 12:
        name='反应堆功率'
        ylabel_name='功率/%(相对于150MW)'
        index=[3]
        legend_name=['反应堆']
        p=data[:,index]/150*100
    elif flag == 13:
        name='反应性'
        ylabel_name='反应性/$'
        legend_name=['总合','控制棒','温度']
        p=np.transpose(np.vstack((data2[:,5],data2[:,6],data2[:,5]-data2[:,6])))
    elif flag == 14:
        name='反应性(temp)'
        ylabel_name='反应性/$'
        legend_name=['总合','控制棒','燃料','冷却剂']
#       通过x修正温度反馈，以最终值时燃料、冷却剂反馈+控制棒=总和为准
        x=(data[-1,5]-data[-1,6])/((data[-1,7]-data[0,7])*-0.005+(data[-1,8]-data[0,8])*-0.08)
        print(x)
#        p=np.transpose(np.vstack((data[:,5],data[:,6],(data[:,7]-data[0,7])*-0.005*x,(data[:,8]-data[0,8])*-0.08*x)))
        p=np.transpose(np.vstack((data[:,5],data[:,6],(data[:,7]-data[0,7])*-0.005,(data[:,8]-data[0,8])*-0.08)))
    elif flag == 15:
        name='堆芯温度'
        ylabel_name='温度/$^\circ$C'
        index=[7]
        legend_name=['堆芯']
        p=data[:,index]-273.15
    else:
        print('Unexpected plot type. No plot created.')    
    mkdir(path)
    sub_plt(data[:,0]/8.6,p,legend_name,filename+'.pdf',ylabel_name,0)
    return p

 
def listdir(path,FP,Condition,num):
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.splitext(file_path)[1]=='.TXT':
            list_name.append(file_path)
    for l in list_name:
        if not re.search(str(FP)+'C'+str(Condition)+'_00'+str(num), l) == None:
            names=l
    data=import_data(names,num)
    return data

path='C:\\AppData\\relapdata\\p2'
mkdir(path+'\\figs')
for i1 in range(0,4) : # 功率水平（10，20，50，100）4个
    if i1 == 0:
        fp = 10
    elif i1 == 1:
        fp = 20
    elif i1 == 2:
        fp = 50
    elif i1 == 3:
        fp = 100
    for i2 in range(0,7): #工况（反应性0~-0.2，给水流量+10%，蒸汽阀门1~0.9，上充0.9167，下泄-0.9167，喷淋1.167，电热2.7e5）
        data1=listdir(path,fp,i2+1,1)
        data2=listdir(path,fp,i2+1,2)
        if fp == 100:
            if i2+1 in [1]:
                data1=data1[range(0,min(int(round((300*8.6/2))),len(data1[:,0]))),:]
                data2=data2[range(0,min(int(round((300*8.6/2))),len(data1[:,0]))),:]
            elif i2+1 in [2,3]:
                data1=data1[range(0,min(int(round((600*8.6/2))),len(data1[:,0]))),:]
                data2=data2[range(0,min(int(round((600*8.6/2))),len(data1[:,0]))),:]
        elif fp == 50:
            if i2+1 in [1]:
                data1=data1[range(0,min(int(round((300*8.6/2))),len(data1[:,0]))),:]
                data2=data2[range(0,min(int(round((300*8.6/2))),len(data1[:,0]))),:]
            elif i2+1 in [2]:
                data1=data1[range(0,min(int(round((600*8.6/2))),len(data1[:,0]))),:]
                data2=data2[range(0,min(int(round((600*8.6/2))),len(data1[:,0]))),:]
        elif fp == 10:
            if i2+1 in [1]:
                data1=data1[range(0,min(int(round((300*8.6/2))),len(data1[:,0]))),:]
                data2=data2[range(0,min(int(round((300*8.6/2))),len(data1[:,0]))),:]
            elif i2+1 in [3]:
                data1=data1[range(0,min(int(round((600*8.6/2))),len(data1[:,0]))),:]
                data2=data2[range(0,min(int(round((600*8.6/2))),len(data1[:,0]))),:]
        for i3 in range(0,15): #参数响应图14张
            if i3 < 10:
                ppp(data1,i3+1,path+'\\figs\\'+str(fp)+'c'+str(i2+1)+'_'+str(i3+1))
                plt.close('all')
            else:
                ppp(data2,i3+1,path+'\\figs\\'+str(fp)+'c'+str(i2+1)+'_'+str(i3+1))
                plt.close('all')