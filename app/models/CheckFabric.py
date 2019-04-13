from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean, Unicode
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.config import engine

base = declarative_base()

session = sessionmaker(bind = engine)

ses = session()

# 机台表
class InspectHdr(base):
    __tablename__ = 'pbCommonDataHalfInspectHdr'
    id = Column(Integer, primary_key = True, autoincrement = True)
    sGroupNo = Column(String(40), nullable = True)
    sCardNo = Column(String(40), nullable = True)
    sCreator = Column(String(40), nullable = True)
    tCreateTime = Column(DateTime, nullable = True)
    sUpdateMan = Column(String(40), nullable = True)
    tUpdateTime = Column(DateTime, nullable = True)
    uemEquipmentGUID = Column(Unicode, nullable = True)
    upsWorkFlowCardGUID = Column(Unicode, nullable = True)
    upsWorkFlowCardInputGUID = Column(Unicode, nullable = True)
    
    def __str__(self):
        return self.id

# 工段表
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

# 工段表
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
        
if __name__ == '__main__':
    base.metadata.create_all(engine)