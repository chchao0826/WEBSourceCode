from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.config import engine

base = declarative_base()

session = sessionmaker(bind = engine)

ses = session()

# 预排主表 机台表
class ProductionSchedulingHDR(base):
    __tablename__ = 'pbCommonDataProductionSchedulingHDR'
    id = Column(Integer, primary_key = True, autoincrement = True)
    sEquipmentNo = Column(String(40),nullable = True)
    sEquipmentName = Column(String(40),nullable = True)
    sType = Column(String(40),nullable = True)
    
    def __str__(self):
        return self.id

# 预排子表 工卡表
class ProductionSchedulingDTL(base):
    __tablename__ = 'pbCommonDataProductionSchedulingDTL'
    id = Column(Integer, primary_key = True, autoincrement = True)
    nHDRID = Column(Integer,nullable = True)
    nRowNumber = Column(Integer,nullable = True)
    tCreateTime = Column(DateTime,nullable = True)
    tUpdateTime = Column(DateTime,nullable = True)
    uppTrackJobGUID = Column(String(40),nullable = True)
    def __str__(self):
        return self.id

# 生管预排
class ProductionScheduling(base):
    __tablename__ = 'pbCommonDataProductionScheduling'
    id = Column(Integer, primary_key = True, autoincrement = True)
    sType = Column(String(40),nullable = True)
    nRowNumber = Column(Integer,nullable = True)
    uppTrackJobGUID = Column(String(40),nullable = True)
    tUpdateTime = Column(DateTime,nullable = True)
    sLabel = Column(String(40),nullable = True)

    def __str__(self):
        return self.id

# 查到预排主表 获得机台号
def GetEquipment(sType):
    # print(tInspectTime)
    ReturnList = []
    for i in ses.query(ProductionSchedulingHDR).filter(ProductionSchedulingHDR.sType == sType).all():
        Dict = {
            'ID' : i.id,
            'sEquipmentNo' : i.sEquipmentNo,
            'sEquipmentName' : i.sEquipmentName,
        }
        ReturnList.append(Dict)
        # print(ReturnList)
    return ReturnList

# 查到预排表 得到子表中机台的最大预排数量
def GetDtlData():
    # print(tInspectTime)
    ReturnList = []
    equipmentList = []
    nBigID = 0

    for i in ses.query(ProductionSchedulingDTL).order_by(ProductionSchedulingDTL.nRowNumber):
        Dict = {
            'ID' : i.id,
            'uppTrackJobGUID' : i.uppTrackJobGUID,
            'nHDRID' : i.nHDRID,
        }
        Dict2 = {
            'nHDRID':i.nHDRID,
        }
        ReturnList.append(Dict)

        if Dict2 not in equipmentList:
            equipmentList.append(Dict2)
        nBigID = i.id
    
    for i in range(1,6):
        Dict3 = {
            'nHDRID' : i,
        }
        if Dict3 not in equipmentList:
            nBigID += 1
            Dict4 = {
            'ID' : nBigID,
            'uppTrackJobGUID' : '空机台',
            'nHDRID' : i,
            }
            ReturnList.append(Dict4)
    return ReturnList

# 按照卡号查询预排表
def IsHaveCard(uppTrackJobGUID):
    iFlag = False
    for i in ses.query(ProductionSchedulingDTL).filter(ProductionSchedulingDTL.uppTrackJobGUID == uppTrackJobGUID).all():
        iFlag = True
        # print(i)
        # print('-----------------')
    return iFlag

# 更新Dtl数据
def UpdateDtl(data):
    nRowNumber = data['nRowNumber']
    nHDRID = data['nHDRID']
    tUpdateTime = data['tTime']
    uppTrackJobGUID = data['uppTrackJobGUID']
    target = ses.query(ProductionSchedulingDTL).filter(ProductionSchedulingDTL.uppTrackJobGUID == uppTrackJobGUID).first()
    target.nRowNumber = nRowNumber
    target.nHDRID = nHDRID
    target.tUpdateTime = tUpdateTime
    ses.commit()
    ses.close()

# 插入数据
def InsertDtl(data):
    nRowNumber = data['nRowNumber']
    nHDRID = data['nHDRID']
    tCreateTime = data['tTime']
    uppTrackJobGUID = data['uppTrackJobGUID']
    InsertDtl = ProductionSchedulingDTL(nRowNumber=nRowNumber, nHDRID=nHDRID, uppTrackJobGUID = uppTrackJobGUID, tCreateTime = tCreateTime, tUpdateTime = tCreateTime)
    ses.add(InsertDtl)
    ses.commit()
    ses.close()

# 操作数据
def OperationalData(data):
    uppTrackJobGUID = data['uppTrackJobGUID']
    iFlag = IsHaveCard(uppTrackJobGUID)
    if iFlag:
        UpdateDtl(data)
    else:
        InsertDtl(data)

# ---------------
# 以下生管预排整理
def IsHaveCard_PMC(uppTrackJobGUID):
    iFlag = False
    for i in ses.query(ProductionScheduling).filter(ProductionScheduling.uppTrackJobGUID == uppTrackJobGUID).all():
        iFlag = True
        # print(i)
        # print('-----------------')
    return iFlag

# 更新Dtl数据
def UpdateDtl_PMC(data):
    nRowNumber = data['nRowNumber']
    uppTrackJobGUID = data['uppTrackJobGUID']
    tUpdateTime = data['tUpdateTime']
    target = ses.query(ProductionScheduling).filter(ProductionScheduling.uppTrackJobGUID == uppTrackJobGUID).first()
    target.nRowNumber = nRowNumber
    target.tUpdateTime = tUpdateTime
    ses.commit()
    ses.close()

# 插入数据
def InsertDtl_PMC(data):
    sType = data['sType']
    nRowNumber = data['nRowNumber']
    uppTrackJobGUID = data['uppTrackJobGUID']
    tUpdateTime = data['tUpdateTime']
    sLabel = data['sLabel']
    InsertDtl = ProductionScheduling(sType=sType, nRowNumber=nRowNumber, uppTrackJobGUID = uppTrackJobGUID, tUpdateTime = tUpdateTime, sLabel = sLabel)
    ses.add(InsertDtl)
    ses.commit()
    ses.close()

# 更新标签
def UpdateLabel_PMC_True(uppTrackJobGUID):
    nMax = 0
    for i in ses.query(ProductionScheduling).filter(ProductionScheduling.sLabel == '#FFA54F').all():
        # print('----------------')
        # print(i.nRowNumber)
        if i.nRowNumber != None:
            if nMax <= i.nRowNumber:
                nMax = i.nRowNumber
    
    target = ses.query(ProductionScheduling).filter(ProductionScheduling.uppTrackJobGUID == uppTrackJobGUID).first()
    nMax += 1
    target.sLabel = '#FFA54F'
    target.nRowNumber = nMax

    for i in ses.query(ProductionScheduling).filter(ProductionScheduling.sLabel != '#FFA54F').all():
        target = ses.query(ProductionScheduling).filter(ProductionScheduling.uppTrackJobGUID == i.uppTrackJobGUID).first()
        target.nRowNumber = nMax
        nMax += 1

    ses.commit()
    ses.close()

# 更新标签
def UpdateLabel_PMC_False(uppTrackJobGUID):
    target = ses.query(ProductionScheduling).filter(ProductionScheduling.uppTrackJobGUID == uppTrackJobGUID).first()
    target.sLabel = '#FFF'
    ses.commit()
    ses.close()

# 取消预排
def DeleteData(uppTrackJobGUID):
    target = ses.query(ProductionScheduling).filter(ProductionScheduling.uppTrackJobGUID == uppTrackJobGUID).first()
    ses.delete(target)
    ses.commit()
    ses.close()

# 查找当前最大序号
def getMaxNumber(sType):
    MaxNumber = 0
    print(sType)
    print(MaxNumber)
    print('**************'*20)
    for i in ses.query(ProductionScheduling).filter(ProductionScheduling.sType == sType).all():
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
