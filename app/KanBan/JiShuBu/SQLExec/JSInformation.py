# -*-coding:utf-8-*-
# 技术部看板


from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect

from app.KanBan.JiShuBu.SQL.JSInformation import JSInformationSQL


import re


base = declarative_base()
# 236
session = sessionmaker(bind=engine)
ses = session()


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
            'nSaleGroupCount': row[12],
            'nSaleCount': row[13],
            'sWorkingProcedureName2': row[14],
            'nWorkingProcedureCount': row[15],
            'sSalesNo': row[16],
            'sSalesGroupNo': row[17],
            'sWorkingProcedureNo': row[18],
            'nPageNumber': nPageNumber,
        }

        allDataList.append(dDict)

        # 业务课别的数量
        salesGroupDict = {
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
                'sSalesGroupNo': dDict['sSalesGroupNo'],
                'sSalesGroupName': dDict['sSalesGroupName'],
                'nSaleGroupCount': dDict['nSaleGroupCount'],
            }
            if SalesDict not in SalesGroupList2:
                SalesGroupList2.append(SalesDict)
            if dDict not in SalesGroupList_value:
                SalesGroupList_value.append(dDict)

        # 传入工序名称
        elif sVarArgs == dDict['sWorkingProcedureNo']:
            WoringDict = {
                'sWorkingProcedureName2': dDict['sWorkingProcedureName2'],
                'sWorkingProcedureNo': dDict['sWorkingProcedureNo'],
                'nWorkingProcedureCount': dDict['nWorkingProcedureCount'],
            }
            if WoringDict not in WoringList:
                WoringList.append(WoringDict)
            if dDict not in WoringList_value:
                WoringList_value.append(dDict)

        # 传入业务员
        elif sVarArgs == dDict['sSalesNo']:
            SalesDict = {
                'sSalesNo': dDict['sSalesNo'],
                'sSalesName': dDict['sSalesName'],
                'nSaleCount': dDict['nSaleCount'],
            }
            if SalesDict not in SalesList:
                SalesList.append(SalesDict)
            if dDict not in SalesList_value:
                SalesList_value.append(dDict)
        a += 1

        row = cursor.fetchone()
    cursor.close()
    return allDataList, salesGroupList, SalesGroupList2, SalesGroupList_value, WoringList, WoringList_value, SalesList, SalesList_value, nPageNumber, sWorkingProcedureList
