from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean, Unicode
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.config import engine, engine_253

base = declarative_base()

session = sessionmaker(bind = engine_253)

ses = session()

# 半成品验布HDR
class InspectHdr(base):
    __tablename__ = 'pbCommonDataHalfInspectHdr'
    id = Column(Integer, primary_key = True, autoincrement = True)
    sGroupNo = Column(String(40), nullable = True)
    sCardNo = Column(String(40), nullable = True)
    sEquipmentName = Column(String(40), nullable = True)
    sCreator = Column(String(40), nullable = True)
    tCreateTime = Column(DateTime, nullable = True)
    sUpdateMan = Column(String(40), nullable = True)
    tUpdateTime = Column(DateTime, nullable = True)
    uemEquipmentGUID = Column(Unicode, nullable = True)
    upsWorkFlowCardGUID = Column(Unicode, nullable = True)
    upsWorkFlowCardInputGUID = Column(Unicode, nullable = True)
    
    def __str__(self):
        return self.id

# 半成品验布DTL
class InspectDtl(base):
    __tablename__ = 'pbCommonDataHalfInspectDtl'
    id = Column(Integer, primary_key = True, autoincrement = True)
    tInspectTime = Column(DateTime, nullable = True)
    sFabricNo = Column(String(40), nullable = True)
    nLengthYard = Column(Integer, nullable = True)
    nLengthMeter = Column(Integer, nullable = True)
    nWeight = Column(Integer, nullable = True)
    nWidth = Column(Integer, nullable = True)
    sGrade = Column(String(40), nullable = True)
    sMainDefectName = Column(String(40), nullable = True)
    nDensity = Column(Integer, nullable = True)
    nGMWTLeft = Column(Integer, nullable = True)
    nGMWTInner = Column(Integer, nullable = True)
    nGMWTRight = Column(Integer, nullable = True)
    sRemark = Column(String(40), nullable = True)
    ipbCommonDataHalfInspectHdrID = Column(Integer, nullable = True)
    
    def __str__(self):
        return self.id

# 半成品验布疵点表
class InspectDefect(base):
    __tablename__ = 'pbCommonDataHalfInspectDefect'
    id = Column(Integer, primary_key = True, autoincrement = True)
    iNumber = Column(Integer, nullable = True)
    sDefectTypeName = Column(String(40), nullable = True)
    nScore = Column(Integer, nullable = True)
    nSite = Column(Integer, nullable = True)
    ipbCommonDataHalfInspectDtlID = Column(Integer, nullable = True)
    
    def __str__(self):
        return self.id

# 根据卡号返回HDR的ID
def ReturnHdrID(sCardNo):
    ReturnList = []
    for i in ses.query(InspectHdr).filter(InspectHdr.sCardNo == sCardNo).all():
        Dict = {
            'ID' : i.id,
            'sCardNo' : i.sCardNo
        }
        ReturnList.append(Dict)
    return ReturnList

# 根据验布时间返回Dtl的ID
def ReturnDtlID(tInspectTime):
    # print(tInspectTime)
    ReturnList = []
    for i in ses.query(InspectDtl).filter(InspectDtl.tInspectTime == tInspectTime).all():
        Dict = {
            'ID' : i.id,
            'tInspectTime' : i.tInspectTime
        }
        ReturnList.append(Dict)
        # print(ReturnList)
        return ReturnList


if __name__ == '__main__':
    base.metadata.create_all(engine)