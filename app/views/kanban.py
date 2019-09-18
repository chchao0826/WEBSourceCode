# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.sql.kanban import equipmentStatusSQL, storeStatusSQL, WorkingStatusSQL, JSInformationSQL

import re


base = declarative_base()
# 236
session = sessionmaker(bind=engine_253)
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
    equipmentStatus = equipmentStatusSQL()
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
    # connect.close()
    return TJ_eq, MM_eq, Dye_eq1, Dye_eq2, Dye_eq3, Dye_eq4, Dye_eq5, Dye_eq6, PB_eq, DB_eq, TS_eq, FB_eq, SX_eq, DX_eq1, DX_eq2, DJ_eq, YB_eq


# 仓库状态
def StoreStatus():
    FPStore = []
    STAStore = []
    STCStore = []
    storeStatus = storeStatusSQL()
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
    WorkingProcedureStatus = WorkingStatusSQL()
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
            sPerinner = str(row[1]) + '%'
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


# 研发看板sql执行
def JSData(*args):
    sVarArgs = ''.join(args)
    cursor = connect.cursor()
    JSInformation = JSInformationSQL(sVarArgs)
    print(sVarArgs)
    print(JSInformation)
    cursor.execute(JSInformation)
    row = cursor.fetchone()
    allDataList = []
    salesGroupList = []
    SalesGroupList2 = []
    SalesGroupList_value = []
    WoringList = []
    WoringList_value = []
    SalesList = []
    SalesList_value = []
    sWorkingProcedureList = []
    sPageList = []
    nPageNumber = 1
    a = 0
    while row:
        borderColor = ''
        if row[9] == '加急':
            borderColor = '#FF0000'
        elif row[10] != None:
            borderColor = '#111111'
        else:
            borderColor = '#'
        sKanBanRemark = str(row[10]).replace(' ', '')
        # 页码
        if a == 6:
            a = 0
            nPageNumber += 1
        # print('nPageNumber' + str(nPageNumber))
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
            'ID': row[11],
            'nSaleGroupCount' : row[12],
            'nSaleCount':row[13],
            'sWorkingProcedureName2': row[14],
            'nWorkingProcedureCount': row[15],
            'sSalesNo': row[16],
            'sSalesGroupNo': row[17],
            'sWorkingProcedureNo': row[18],
            'nPageNumber' : nPageNumber,
        }

        allDataList.append(dDict)

        # 业务课别的数量
        salesGroupDict ={
            'sSalesGroupNo': dDict['sSalesGroupNo'],
            'sSalesGroupName': dDict['sSalesGroupName'],
            'nSaleGroupCount': dDict['nSaleGroupCount'],
        }
        if salesGroupDict not in salesGroupList:
            salesGroupList.append(salesGroupDict)

        # 工段的数量
        sWorkingDict = {
            'sWorkingProcedureNo': dDict['sWorkingProcedureNo'],
            'sWorkingProcedureName': dDict['sWorkingProcedureName2'],
            'nWorkingProcedureCount': dDict['nWorkingProcedureCount'],
        }
        if sWorkingDict not in sWorkingProcedureList:
            sWorkingProcedureList.append(sWorkingDict)

        # 传入业务课别
        if sVarArgs == dDict['sSalesGroupNo']:
            SalesDict = {
                'sSalesGroupNo' : dDict['sSalesGroupNo'],
                'sSalesGroupName' : dDict['sSalesGroupName'],
                'nSaleGroupCount' : dDict['nSaleGroupCount'],
            }
            if SalesDict not in SalesGroupList2:
                SalesGroupList2.append(SalesDict)
            if dDict not in SalesGroupList_value:
                SalesGroupList_value.append(dDict)

        # 传入工序名称        
        elif sVarArgs == dDict['sWorkingProcedureNo']:
            WoringDict = {
                'sWorkingProcedureName2' : dDict['sWorkingProcedureName2'],
                'sWorkingProcedureNo' : dDict['sWorkingProcedureNo'],
                'nWorkingProcedureCount' : dDict['nWorkingProcedureCount'],
            }
            if WoringDict not in WoringList:
                WoringList.append(WoringDict)
            if dDict not in WoringList_value:
                WoringList_value.append(dDict)

        # 传入业务员
        elif sVarArgs == dDict['sSalesNo']:
            SalesDict = {
                'sSalesNo' : dDict['sSalesNo'],
                'sSalesName' : dDict['sSalesName'],
                'nSaleCount' : dDict['nSaleCount'],
            }
            if SalesDict not in SalesList:
                SalesList.append(SalesDict)
            if dDict not in SalesList_value:
                SalesList_value.append(dDict)
        a += 1



        row = cursor.fetchone()
    cursor.close()
    return allDataList, salesGroupList, SalesGroupList2, SalesGroupList_value, WoringList, WoringList_value, SalesList, SalesList_value, nPageNumber, sWorkingProcedureList
