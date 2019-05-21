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
    sCardNo = Column(String(40),nullable = True)
    nHDRID = Column(Integer,nullable = True)
    nRowNumber = Column(Integer,nullable = True)
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

# 查到预排主表 获得机台号
def GetDtlData():
    # print(tInspectTime)
    ReturnList = []
    equipmentList = []
    nBigID = 0

    for i in ses.query(ProductionSchedulingDTL).order_by(ProductionSchedulingDTL.nRowNumber):
        Dict = {
            'ID' : i.id,
            'sCardNo' : i.sCardNo,
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
            'sCardNo' : '空机台',
            'nHDRID' : i,
            }
            ReturnList.append(Dict4)
    return ReturnList


# 按照卡号查询预排表
def IsHaveCard(sCardNo):
    iFlag = False
    for i in ses.query(ProductionSchedulingDTL).filter(ProductionSchedulingDTL.sCardNo == sCardNo).all():
        iFlag = True
        # print(i)
        # print('-----------------')
    return iFlag

# 更新Dtl数据
def UpdateDtl(data):
    nRowNumber = data['nRowNumber']
    sCardNo = data['sCardNo']
    nHDRID = data['nHDRID']

    target = ses.query(ProductionSchedulingDTL).filter(ProductionSchedulingDTL.sCardNo == sCardNo).first()
    target.nRowNumber = nRowNumber
    target.nHDRID = nHDRID
    ses.commit()
    ses.close()

def InsertDtl(data):
    nRowNumber = data['nRowNumber']
    sCardNo = data['sCardNo']
    nHDRID = data['nHDRID']
    InsertDtl = ProductionSchedulingDTL(nRowNumber=nRowNumber, sCardNo=sCardNo, nHDRID=nHDRID)
    ses.add(InsertDtl)
    ses.commit()
    ses.close()


if __name__ == '__main__':
    base.metadata.create_all(engine)
