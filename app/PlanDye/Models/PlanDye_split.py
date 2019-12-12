# -*-coding:utf-8-*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean, and_
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.PlanDye.Models.PlanDyeing import PlanDyeDTL
from app.config import engine


base = declarative_base()
session = sessionmaker(bind=engine)
ses = session()


# 通过机台找到所有确认的数据
def GetCheckData(nHDRID):
    sIDList = []
    for i in ses.query(PlanDyeDTL).filter(and_(PlanDyeDTL.nHDRID == nHDRID, PlanDyeDTL.bISCheck == 1)).all():
        sIDList.append(i.id)
    return sIDList


# 更新信息去除确认信息
def UpdateCheckFalse(ID):
    target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
    target.bISCheck = False
    ses.commit()
    ses.close()


# 更新信息增加确认信息, 更新序号, 机台号
def UpdateCheckTrue(data):
    print('----------------更新-------------')
    print(data)
    print('------------更新成功-----------')
    ID = data['ID']
    nHDRID = data['nHDRID']
    nRowNumber = data['nRowNumber']
    tUpdateTime = data['tUpdateTime']
    # sType = data['sCardNo']
    target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
    target.nHDRID = nHDRID
    target.nRowNumber = nRowNumber
    target.tUpdateTime = tUpdateTime
    target.bISCheck = 1
    ses.commit()
    ses.close()


# 数据库中的资料不在POST列表中
def POSTNotInSqlData(nHDRID, Data):
    SqlData = GetCheckData(nHDRID)
    for a in SqlData:
        print(a)
        print(Data)
        if str(a) not in Data:
            print(a)
            print('====================')
            UpdateCheckFalse(a)


# 更新数据
def UpdateDtl_Split(data):
    sHDRIDList = []
    nHDRID = ''
    for i in data:
        nHDRID = i['nHDRID']
        if nHDRID not in sHDRIDList:
            sHDRIDList.append(nHDRID)
        # 确定信息更新
        UpdateCheckTrue(i)
    for i in sHDRIDList:
        DataList = []
        for a in data:
            if i == a['nHDRID']:
                DataList.append(a['ID'])
        # 取消信息更新
        POSTNotInSqlData(i, DataList)


# 得到该机台最大的nRowNumber
def GetMaxNumber(nHDRID):
    nMaxNumber = 0
    for i in ses.query(PlanDyeDTL).filter(and_(PlanDyeDTL.nHDRID == nHDRID, PlanDyeDTL.bISCheck == 1)).all():
        if i.nRowNumber > nMaxNumber:
            nMaxNumber = i.nRowNumber
    return nMaxNumber


# 下方数据往上更新 预排数据
def InsertDtl_Split(data):
    nEquipmentID = ''
    for i in data:
        ID = i['ID']
        nHDRID = i['nHDRID']
        nRowNumber = i['nRowNumber']
        tUpdateTime = i['tUpdateTime']
        nMaxNumber = -1
        if nEquipmentID != nHDRID:
            nEquipmentID = nHDRID
            nMaxNumber = GetMaxNumber(nHDRID)
        print(nRowNumber)
        print(nMaxNumber)
        nRowNumber = int(nRowNumber) + int(nMaxNumber)
        print(nRowNumber)
        target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
        target.nHDRID = nHDRID
        target.nRowNumber = nRowNumber
        target.tUpdateTime = tUpdateTime
        target.bISCheck = 1
        ses.commit()
        ses.close()


# 上方的数据往下放置, 取消预排数据
def DeleteDtl_Split(data):
    print('===============')
    print(data)
    for i in data:
        ID = i['ID']
        nHDRID = i['nHDRID']
        tUpdateTime = i['tUpdateTime']
        iFlag = IsXG(ID)
        if iFlag == False:
            target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
            target.nHDRID = nHDRID
            target.tUpdateTime = tUpdateTime
            target.bISCheck = 0
            ses.commit()
            ses.close()


# 判断删除的ID是否为洗缸,如果取消洗缸则进行删除 bUsable = 0
def IsXG(ID):
    iFlag = False
    for i in ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).all():
        sType = i.sType
        if sType.find('洗缸') != -1:
            iFlag = True
            target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
            target.bUsable = 0
            target.bISCheck = 0
            ses.commit()
            ses.close()
    return iFlag



# 判断洗缸的序号
def SearchXG(nHDRID):
    returnData = []
    for i in ses.query(PlanDyeDTL).filter(and_(PlanDyeDTL.nHDRID == nHDRID, PlanDyeDTL.bISCheck == 1)).order_by(PlanDyeDTL.nRowNumber.desc()).all():
        sType = i.sType
        if sType == None:
            sType = ''
        if sType.find('洗缸') != -1:
            sDict = {
                'ID': i.id,
                'nHDRID': i.nHDRID,
                'nRowNumber': i.nRowNumber,
                'sType': i.sType,
            }
            returnData.append(sDict)
    return returnData


# 插入洗缸
def UpdataXGMain(data):
    for i in data:
        nHDRID = i['nHDRID']
        sEquipmentNo = i['sEquipmentNo']
        nRowNumber = i['nRowNumber']
        tUpdateTime = i['tUpdateTime']
        SearchXGData = SearchXG(nHDRID)
        if SearchXGData != []:
            UpdateXG_PMC(SearchXGData, nHDRID, nRowNumber,
                         tUpdateTime, sEquipmentNo)
        else:
            sType = sEquipmentNo + '_洗缸_1'
            InsertXG_PMC(nHDRID, nRowNumber, tUpdateTime, sType)

    return 'a123'


# 更新洗缸
def UpdateXG_PMC(SearchXGData, nHDRID, nRowNumber, tUpdateTime, sEquipmentNo):
    print('=======数据库中有资料进行更新==========')
    sType = ''
    for i in SearchXGData:
        if i['nRowNumber'] > nRowNumber:
            sTypeList = str(i['sType']).split('_')

            sType2 = sTypeList[0] + '_' + sTypeList[1] + \
                '_' + str((int(sTypeList[2]) + 1))
            sType = i['sType']
            print(sType2)
            print(i['ID'])
            print('=========洗缸更新=========')
            target = ses.query(PlanDyeDTL).filter(
                PlanDyeDTL.id == i['ID']).first()
            target.sType = sType2
            ses.commit()
            ses.close()

    print('==========插入更新后的数据===========')
    InsertXG_PMC(nHDRID, nRowNumber, tUpdateTime, sType)

    return '更新洗缸完成'


# 插入洗缸
def InsertXG_PMC(nHDRID, nRowNumber, tUpdateTime, sType):
    print('============插入洗缸=============')
    InsertDtl = PlanDyeDTL(nHDRID=nHDRID, nRowNumber=nRowNumber,
                           tUpdateTime=tUpdateTime, sType=sType, bUsable=1, bISCheck=1)
    ses.add(InsertDtl)
    ses.commit()
    ses.close()
