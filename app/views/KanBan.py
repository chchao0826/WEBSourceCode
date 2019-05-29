# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine, connect
from app.sql.equipmentStatus import equipmentStatus
from app.sql.WorkingProcedureStatus import WorkingProcedureStatus
from app.sql.storeStatus import storeStatus
from app.sql.GetSample import GetSample
from app.sql.JSInformation import JSInformation
from app.sql.SchedulingZL_KanBan import ZLKanBanSQL

import re

base = declarative_base()
# 236
session = sessionmaker(bind=engine)
ses = session()


# 机台状态
def emStatus():
    # 执行SQL语句转为List-详细
    TJ_eq = []
    Dye_eq1 = []
    Dye_eq2 = []
    Dye_eq3 = []
    Dye_eq4 = []
    Dye_eq5 = []
    Dye_eq6 = []
    TS_eq = []
    SX_eq = []
    DX_eq1 = []
    DX_eq2 = []
    DJ_eq = []
    YB_eq = []
    MM_eq = []
    PB_eq = []
    DB_eq = []
    FB_eq = []
    cursor = connect.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(equipmentStatus)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sEquipmentNo': row[1],
            'sEquipmentName': row[2],
            'sStatusColor': row[8],
        }
        if row[1] in ('LDR03', 'LDR02', 'LDR01'):
            TJ_eq.append(dictVar)
        elif row[1] in ('HQ03'):
            MM_eq.append(dictVar)
        elif row[1] in ('E027', 'E030', 'E029'):
            Dye_eq1.append(dictVar)
        elif row[1] in ('E028', 'E031', 'E026', 'E025'):
            Dye_eq2.append(dictVar)
        elif row[1] in ('A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'C020'):
            Dye_eq3.append(dictVar)
        elif row[1] in ('B007', 'B008', 'B009', 'B010'):
            Dye_eq4.append(dictVar)
        elif row[1] in ('C015', 'C016', 'C017', 'C018', 'C019'):
            Dye_eq5.append(dictVar)
        elif row[1] in ('D021', 'D022', 'D023', 'D024'):
            Dye_eq6.append(dictVar)
        elif row[1] in ('HP01'):
            PB_eq.append(dictVar)
        elif row[1] in ('订边机'):
            DB_eq.append(dictVar)
        elif row[1] in ('LT03', 'LT02', 'LT01'):
            TS_eq.append(dictVar)
        elif row[1] in ('DR03'):
            FB_eq.append(dictVar)
        elif row[1] in ('LS01', 'LS02'):
            SX_eq.append(dictVar)
        elif row[1] in ('LB03', 'LB04', 'LB05'):
            DX_eq1.append(dictVar)
        elif row[1] in ('LB01', 'LB02'):
            DX_eq2.append(dictVar)
        elif row[1] in ('KJ04', 'KJ03', 'KJ02', 'KJ01'):
            DJ_eq.append(dictVar)
        elif row[1] in ('KI04', 'KI03', 'KI02', 'KI01'):
            YB_eq.append(dictVar)
        row = cursor.fetchone()
    cursor.close()

    print(DX_eq1)
    print(DX_eq2)
    # connect.close()
    return TJ_eq, MM_eq, Dye_eq1, Dye_eq2, Dye_eq3, Dye_eq4, Dye_eq5, Dye_eq6, PB_eq, DB_eq, TS_eq, FB_eq, SX_eq, DX_eq1, DX_eq2, DJ_eq, YB_eq

# 仓库状态
def StoreStatus():
    FPStore = []
    STAStore = []
    STCStore = []
    cursor = connect.cursor()
    cursor.execute(storeStatus)
    row = cursor.fetchone()
    sPerinner = ''
    sOutColor = ''
    sInnerColor = ''
    while row:

        if row[1] <= int(80):
            sPerinner = str(row[1]) + '%'
            sOutColor = 'progress-bar-success'
            sInnerColor = 'progress-bar-info'
        elif row[1] > int(80) and int(row[1]) <= int(100):
            sPerinner = str(row[1]) + '%'
            sOutColor = 'progress-bar-success'
            sInnerColor = 'progress-bar-warning'
        elif row[1] > int(100):
            sPerinner = '100%'
            sOutColor = 'progress-bar-warning'
            sInnerColor = 'progress-bar-danger'

        dictVar = {
            'sStoreName': row[0],
            'sPerinner': sPerinner,
            'sTDX': row[2],
            'sOutColor': sOutColor,
            'sInnerColor': sInnerColor,
        }
        if row[0] == '胚仓':
            FPStore.append(dictVar)
        elif row[0] == '成品仓AB':
            STAStore.append(dictVar)
        elif row[0] == '成品仓C':
            STCStore.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return FPStore, STAStore, STCStore

# 工段状态
def wpStatus():
    TJWip = []
    SXWip = []
    YDWip = []
    DyeWip = []
    CDWip = []
    BZWip = []
    cursor = connect.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(WorkingProcedureStatus)
    # 执行sql语句
    row = cursor.fetchone()
    while row:
        sPerinner = ''
        sPerOut = '100%'
        sOutColor = ''
        sInnerColor = ''

        if row[1] <= int(80):
            sPerinner = str(row[1]) + '%'
            sOutColor = 'progress-bar-success'
            sInnerColor = 'progress-bar-info'
        elif row[1] > int(80) and int(row[1]) <= int(100):
            sPerinner = str(row[1]) + '%'
            sOutColor = 'progress-bar-success'
            sInnerColor = 'progress-bar-warning'
        elif row[1] > int(100):
            sPerinner = '100%'
            sOutColor = 'progress-bar-danger'
            sInnerColor = 'progress-bar-warning'

        dictVar = {
            'sWorkingProcedureName': row[0],
            'sPerinner': sPerinner,
            'sPerOut': sPerOut,
            'sOutColor': sOutColor,
            'sInnerColor': sInnerColor,
            'sTDX': row[2],
        }
        if row[0] == '退卷':
            TJWip.append(dictVar)
        elif row[0] == '水洗':
            SXWip.append(dictVar)
        elif row[0] == '预定':
            YDWip.append(dictVar)
        elif row[0] == '染色':
            DyeWip.append(dictVar)
        elif row[0] == '成定型':
            CDWip.append(dictVar)
        elif row[0] == '包装':
            BZWip.append(dictVar)
        row = cursor.fetchone()

    cursor.close()
    return TJWip, SXWip, YDWip, DyeWip, CDWip, BZWip

# 取样看板sql执行
def DyeGetSample(*args):
    sEquipmentNo = ''.join(args)
    cursor = connect.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(GetSample)
    # 执行sql语句
    row = cursor.fetchone()
    dataList = []
    euipmentList = []
    activeRowNumber = 0
    maxRowNumber = 0
    minRowNumber = 1
    activeList = []
    prevList = []
    nextList = []
    minList = []
    sColor = ''
    while row:
        if re.match('超时', row[9], flags=1) is not None:
            sColor = '#DC143C'
        else:
            sColor = ''
        varDict = {
            'sEquipmentNo': row[0],
            'sCardNo': row[1],
            'nFactInputQty': row[2],
            'sColorNo': row[3],
            'sMaterialNo': row[4],
            'sRemark': row[5],
            'nNextCallTime': row[6],
            'nRowNumber': row[7],
            'sCustomerName': row[8],
            'sType': row[9],
            'tFactEndTime': row[10],
            'sColor': sColor,
        }
        DictEuipment = {
            'sEuipmentNo': row[0],
            'sColor': sColor
        }
        if sEquipmentNo == row[0]:
            activeRowNumber = row[7]
            activeList.append(varDict)
        if minRowNumber <= row[7]:
            minRowNumber = row[7]
        if maxRowNumber <= row[7]:
            maxRowNumber = row[7]
        euipmentList.append(DictEuipment)
        dataList.append(varDict)
        row = cursor.fetchone()
    cursor.close()
    for i in dataList:
        # 上一个机台
        if activeRowNumber - 1 == i['nRowNumber']:
            prevList.append(i)
        elif (activeRowNumber - 1) <= 0 and activeRowNumber != 1:
            if minRowNumber == i['nRowNumber']:
                prevList.append(i)
        # 下一个机台
        if activeRowNumber + 1 == i['nRowNumber']:
            nextList.append(i)
        elif activeRowNumber + 1 > maxRowNumber:
            if maxRowNumber == i['nRowNumber']:
                nextList.append(i)

        if minRowNumber == i['nRowNumber']:
            print(minRowNumber)
            minList.append(i)
    return dataList, euipmentList, activeList, prevList, nextList, minList

# 研发看板sql执行
def JSData(*args):
    sVarArgs = ''.join(args)
    cursor = connect.cursor()
    cursor.execute(JSInformation)
    row = cursor.fetchone()
    dataList = []
    sSalesGroupName = ''
    salesGroupList = []
    groupNameList = []
    salesList = []
    salesValueList = []
    sWorkingProcedureDataList = []
    sWorkingProcedureList = []
    while row:
        borderColor = ''
        if row[9] == 1:
            borderColor = '#FFFF00'
            print('1111')
            print('#FFFF00')
        elif row[10] != None:
            borderColor = '#FF0000'
        else :
            borderColor = '#FFFFFF'
        
        sKanBanRemark = row[10]
        if sKanBanRemark != None:
            sKanBanRemark = sKanBanRemark.replace(' ','')
            
        dDict = {
            'sSalesName': row[0],
            'sCardNo': row[1],
            'sMaterialNo': row[2],
            'tCardTime': row[3],
            'sWorkingProcedureName': row[4],
            'sTopColor': row[5],
            'sSalesGroupName': row[6],
            'tFactStartTime': row[7],
            'tFactEndTime': row[8],
            'borderColor': borderColor,
            'sKanBanRemark': sKanBanRemark,
            'ID': row[11]
        }
        # 部门列表
        if sSalesGroupName != row[6]:
            sSalesGroupName = row[6]
            salesGroupDict = {
                'sSalesGroupName': row[6],
                'nCount':row[12]
            }
            salesGroupList.append(salesGroupDict)
        dataList.append(dDict)

        sWorkingDict = {
            'sWorkingProcedureName':row[14],
            'nWorkingProcedureCount': row[15]
        }
        if sWorkingDict not in sWorkingProcedureList:
            sWorkingProcedureList.append(sWorkingDict)

        # 根据传入的部门
        if sVarArgs == row[6]:
            groupNameList.append(dDict)
            salesDict = {
                'sSalesName':row[0],
                'nSaleCount': row[13]
            }
            if salesDict not in salesList:
                salesList.append(salesDict)
        if sVarArgs == row[14]:
            sWorkingProcedureDataList.append(dDict)
        # 根据传入的人名建立LIST
        if sVarArgs == row[0]:
            salesValueList.append(dDict)
        row = cursor.fetchone()
    cursor.close()
    return dataList, salesGroupList, groupNameList, salesList, salesValueList, sWorkingProcedureList, sWorkingProcedureDataList

# 整理看板SQL
def ZLKanBanData():
    ReturnData = []
    sSQL = ZLKanBanSQL()
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sCardNo' : str(row[0]),
            'sEquipmentNo' : str(row[1]),
            'sColorNo' : str(row[2]),
            'sMaterialNo' : str(row[3]),
            'sWorkingProcedureName' : str(row[4]),
            'nTime' : str(row[5]),
            'nFactTime' : str(row[6]),
            'nFactInPutQty' : str(row[7]),
            'nSpeed' : str(row[8]),
            'nTemp' : str(row[9]),
            'sProductWidth' : str(row[10]),
            'sProductGMWT' : str(row[11]),
            'uppTrackJobGUID' : str(row[12]),
            'nRowNumber' : str(row[13]),
            'sCustomerName' : str(row[14]),
            'nPre': str(row[15]),
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData



if __name__ == '__main__':
    emStatus()
