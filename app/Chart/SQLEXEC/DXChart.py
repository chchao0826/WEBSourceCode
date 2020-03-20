# -*- coding: utf-8 -*-

from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine, connect, connect_253
from app.Chart.SQL.DXDoneSql import DXDoneSql, DXTop3Sql


def DXDone():
    ReturnData = []
    sSql = DXDoneSql()
    cursor = connect.cursor()
    cursor.execute(sSql)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sEquipmentNo': row[0],
            'nFinish': row[1],
            'nNotFinish': row[2],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


def DXTop3():
    ReturnData = []
    sSql = DXTop3Sql()
    cursor = connect.cursor()
    cursor.execute(sSql)
    row = cursor.fetchone()
    getData = []
    nNabnorNumber = 0
    nStateNumber = 0
    nStartUpNumber = 0
    while row:
        sType = row[2]
        dictVar = {
            'sType': sType,
            'sRemark': row[3],
            'sEquipmentNo':  row[4],
            'nCount': row[5],
        }
        if sType == 'abnormal':
            nNabnorNumber += 1
        elif sType == 'state':
            nStateNumber += 1
        elif sType == 'startUp':
            nStartUpNumber += 1
        getData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return getData, nNabnorNumber, nStateNumber, nStartUpNumber


def TidyData(getData, nNumber, sDataType):
    sLabels = []
    sData = []
    sEquipmentNoVar = ''
    ReturnData = []
    print('===============')
    print(getData)
    print('=======23121========')
    print(nNumber)
    varNumber = 0
    dictVar = {}
    for i in getData:
        sType = i['sType']
        sRemark = i['sRemark']
        sEquipmentNo = i['sEquipmentNo']
        nCount = i['nCount']
        print(i)
        if sType == sDataType:
            if sEquipmentNoVar == '':
                sEquipmentNoVar = sEquipmentNo
            if sEquipmentNoVar != sEquipmentNo:
                dictVar = {
                    'sType': sType,
                    'sEquipmentNo': sEquipmentNoVar,
                    'Labels': sLabels,
                    'Data': sData,
                }
                sLabels = []
                sData = []
                ReturnData.append(dictVar)
                sEquipmentNoVar = sEquipmentNo
            varNumber += 1
            if varNumber == nNumber:
                dictVar = {
                    'sType': sType,
                    'sEquipmentNo': sEquipmentNoVar,
                    'Labels': sLabels,
                    'Data': sData,
                }
                print(dictVar)
                ReturnData.append(dictVar)
                sLabels = []
                abnorData = []
            sLabels.append(sRemark)
            sData.append(nCount)
    return ReturnData

def ReturnDXTop3Data():
    returnData = DXTop3()
    getData = returnData[0]
    nNabnorNumber = returnData[1]
    nStateNumber = returnData[2]
    nStartUpNumber = returnData[3]
    abnormalData = TidyData(getData, nNabnorNumber, 'abnormal')
    StateData = TidyData(getData, nStateNumber, 'state')
    StartUpData = TidyData(getData, nStartUpNumber, 'startUp')
    
    print(abnormalData)
    print(StateData)
    print(StartUpData)
    return abnormalData, StateData, StartUpData
