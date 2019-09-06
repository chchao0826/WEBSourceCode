# -*-coding:utf-8-*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.config import engine

base = declarative_base()
session = sessionmaker(bind=engine)
ses = session()


# 预排主表 机台表
class PlanHdr(base):
    __tablename__ = 'pbCommonDataProductionSchedulingHDR'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sEquipmentNo = Column(String(40), nullable=True)
    sEquipmentName = Column(String(40), nullable=True)
    sType = Column(String(40), nullable=True)

    def __str__(self):
        return self.id


# 预排子表 工卡表
class PlanDtl(base):
    __tablename__ = 'pbCommonDataProductionSchedulingDTL'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nHDRID = Column(Integer, nullable=True)
    nRowNumber = Column(Integer, nullable=True)
    tCreateTime = Column(DateTime, nullable=True)
    tUpdateTime = Column(DateTime, nullable=True)
    uppTrackJobGUID = Column(String(100), nullable=True)

    def __str__(self):
        return self.id


# 生管预排
class Plan(base):
    __tablename__ = 'pbCommonDataProductionScheduling'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sType = Column(String(40), nullable=True)
    nRowNumber = Column(Integer, nullable=True)
    uppTrackJobGUID = Column(String(40), nullable=True)
    tUpdateTime = Column(DateTime, nullable=True)
    sLabel = Column(String(40), nullable=True)

    def __str__(self):
        return self.id


# 判断数据是否存在生管预排表中
def IsInPMCPlan(uppTrackJobGUID):
    for i in ses.query(Plan).filter(Plan.uppTrackJobGUID == uppTrackJobGUID).all():
        return True


# 生管数据更新
def UpdateDtl_PMC(data):
    # 更新Dtl数据
    nRowNumber = data['nRowNumber']
    uppTrackJobGUID = data['uppTrackJobGUID']
    sLabel = data['sLabel']
    print(sLabel)
    target = ses.query(Plan).filter(Plan.uppTrackJobGUID == uppTrackJobGUID).first()
    target.nRowNumber = nRowNumber
    target.sLabel = sLabel
    ses.commit()
    ses.close()


# 生管数据插入
def InsertDtl_PMC(data):
    # 插入数据
    sType = data['sType']
    nRowNumber = data['nRowNumber']
    uppTrackJobGUID = data['uppTrackJobGUID']
    sLabel = data['sLabel']
    InsertDtl = Plan(sType=sType, nRowNumber=nRowNumber, uppTrackJobGUID=uppTrackJobGUID, sLabel=sLabel)
    ses.add(InsertDtl)
    ses.commit()
    ses.close()


# POST数据更新
def PMCPostData(data):
    for i in data:
        uppTrackJobGUID = i['uppTrackJobGUID']
        print(uppTrackJobGUID)
        # sType = i['sType']
        # nRowNumber = i['nRowNumber']
        # bIsUrgent = i['bIsUrgent']
        if IsInPMCPlan(uppTrackJobGUID) == True:
            UpdateDtl_PMC(i)
            print('更新')
        else:
            InsertDtl_PMC(i)
            print('插入')
    return 'abc'


# 查询机台号
def GetEquipment(sType):
    ReturnList = []
    for i in ses.query(PlanHdr).filter(PlanHdr.sType == sType).all():
        Dict = {
            'ID': i.id,
            'sEquipmentNo': i.sEquipmentNo,
            'sEquipmentName': i.sEquipmentName,
        }
        ReturnList.append(Dict)
    return ReturnList


# 定型排单
# 插入数据
def InsertDtl(data):
    # 插入数据
    nRowNumber = data['nRowNumber']
    nHDRID = data['nHDRID']
    tCreateTime = data['tTime']
    uppTrackJobGUID = data['uppTrackJobGUID']
    InsertDtl = PlanDtl(nRowNumber=nRowNumber, nHDRID=nHDRID, uppTrackJobGUID=uppTrackJobGUID, tCreateTime=tCreateTime, tUpdateTime=tCreateTime)
    ses.add(InsertDtl)
    ses.commit()
    ses.close()


# 更新数据
def UpdateDtl(data):
    nRowNumber = data['nRowNumber']
    nHDRID = data['nHDRID']
    tUpdateTime = data['tTime']
    uppTrackJobGUID = data['uppTrackJobGUID']
    target = ses.query(PlanDtl).filter(PlanDtl.uppTrackJobGUID == uppTrackJobGUID).first()
    target.nRowNumber = nRowNumber
    target.nHDRID = nHDRID
    target.tUpdateTime = tUpdateTime
    ses.commit()
    ses.close()


# 定型预排表中是否存在数据
def IsInDXPlan(uppTrackJobGUID):
    # 按照卡号查询预排表
    iFlag = False
    for i in ses.query(PlanDtl).filter(PlanDtl.uppTrackJobGUID == uppTrackJobGUID).all():
        iFlag = True
    return iFlag


# 定型 POST 数据
def DXPostdata(data):
    for i in data:
        uppTrackJobGUID = i['uppTrackJobGUID']
        if IsInDXPlan(uppTrackJobGUID) == True:
            UpdateDtl(i)
            print('定型预排更新数据')
        else:
            InsertDtl(i)
            print('定型预排插入数据')
    return 'DX POST'


# 定型预排删除
def DeleteDXPlan(data):
    uppTrackJobGUID = data['uppTrackJobGUID']
    target = ses.query(PlanDtl).filter(PlanDtl.uppTrackJobGUID == uppTrackJobGUID).first()
    ses.delete(target)
    ses.commit()
    ses.close()


def GetDtlData():
    # 查到预排表 得到子表中机台的最大预排数量
    ReturnList = []
    equipmentList = []
    nBigID = 0
    for i in ses.query(PlanDtl).order_by(PlanDtl.nRowNumber):
        Dict = {
            'ID': i.id,
            'uppTrackJobGUID': i.uppTrackJobGUID,
            'nHDRID': i.nHDRID,
        }
        Dict2 = {
            'nHDRID': i.nHDRID,
        }
        ReturnList.append(Dict)

        if Dict2 not in equipmentList:
            equipmentList.append(Dict2)
        nBigID = i.id

    for i in range(1, 6):
        Dict3 = {
            'nHDRID': i,
        }
        if Dict3 not in equipmentList:
            nBigID += 1
            Dict4 = {
                'ID': nBigID,
                'uppTrackJobGUID': '空机台',
                'nHDRID': i,
            }
            ReturnList.append(Dict4)
    return ReturnList










def DeleteDtl(data):
    # 删除数据
    uppTrackJobGUID = data['uppTrackJobGUID']
    target = ses.query(PlanDtl).filter(
        PlanDtl.uppTrackJobGUID == uppTrackJobGUID).first()
    ses.delete(target)
    ses.commit()
    ses.close()


def OperationalData(data):
    # 操作数据
    uppTrackJobGUID = data['uppTrackJobGUID']
    iFlag = IsHaveCard(uppTrackJobGUID)
    if iFlag:
        UpdateDtl(data)
    else:
        InsertDtl(data)


def IsHaveCard_PMC(uppTrackJobGUID):
    # 以下生管预排整理
    iFlag = False
    for i in ses.query(Plan).filter(Plan.uppTrackJobGUID == uppTrackJobGUID).all():
        iFlag = True
    return iFlag





def UpdateLabel_PMC_True(uppTrackJobGUID):
    # 更新标签
    nMax = 0
    for i in ses.query(Plan).filter(Plan.sLabel == '#FFA54F').all():
        # print('----------------')
        # print(i.nRowNumber)
        if i.nRowNumber != None:
            if nMax <= i.nRowNumber:
                nMax = i.nRowNumber

    target = ses.query(Plan).filter(
        Plan.uppTrackJobGUID == uppTrackJobGUID).first()
    nMax += 1
    target.sLabel = '#FFA54F'
    target.nRowNumber = nMax

    for i in ses.query(Plan).filter(Plan.sLabel != '#FFA54F').all():
        target = ses.query(Plan).filter(
            Plan.uppTrackJobGUID == i.uppTrackJobGUID).first()
        target.nRowNumber = nMax
        nMax += 1

    ses.commit()
    ses.close()


def UpdateLabel_PMC_False(uppTrackJobGUID):
    # 更新标签
    target = ses.query(Plan).filter(
        Plan.uppTrackJobGUID == uppTrackJobGUID).first()
    target.sLabel = '#FFF'
    ses.commit()
    ses.close()


def DeleteData(uppTrackJobGUID):
    # 取消预排
    target = ses.query(Plan).filter(
        Plan.uppTrackJobGUID == uppTrackJobGUID).first()
    ses.delete(target)
    ses.commit()
    ses.close()


def getMaxNumber(sType):
    # 查找当前最大序号
    MaxNumber = 0
    print(sType)
    print(MaxNumber)
    print('**************'*20)
    for i in ses.query(Plan).filter(Plan.sType == sType).all():
        # print('-------------')
        # print(i.nRowNumber)
        if i.nRowNumber != None:
            if MaxNumber <= i.nRowNumber:
                MaxNumber = i.nRowNumber
                # print('*******'*20)
                # print(MaxNumber)
    return MaxNumber


if __name__ == '__main__':
    base.metadata.create_all(engine)
