# -*-coding:utf-8-*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean, and_
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.config import engine


base = declarative_base()
session = sessionmaker(bind=engine)
ses = session()


# 预排主表 机台表
class PlanDyeDTL(base):
    __tablename__ = 'pbCommonDataProductionSchedulingDyeingDTL'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nHDRID = Column(Integer, nullable=True)
    nRowNumber = Column(Integer, nullable=True)
    tUpdateTime = Column(DateTime, nullable=True)
    sType = Column(String, nullable=True)
    bUsable = Column(Boolean, nullable=True)

    def __str__(self):
        return self.id


# 更新Dtl数据
def UpdateDtl_PMC(data):

    ID = data['id']
    nHDRID = data['nHDRID']
    nRowNumber = data['nRowNumber']
    tUpdateTime = data['tUpdateTime']

    target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
    target.nHDRID = nHDRID
    target.nRowNumber = nRowNumber
    target.tUpdateTime = tUpdateTime
    print('==============更新成功===========')
    ses.commit()
    ses.close()


# 更新洗缸
def UpdateXG_PMC(data):
    ID = data['id']
    nHDRID = data['nHDRID']
    nRowNumber = data['nRowNumber']
    tUpdateTime = data['tUpdateTime']
    sType = data['sCardNo']
    target = ses.query(PlanDyeDTL).filter(PlanDyeDTL.id == ID).first()
    if target != None:
        print('=========洗缸更新=========')
        target.nHDRID = nHDRID
        target.nRowNumber = nRowNumber
        target.tUpdateTime = tUpdateTime
        target.sType = sType
    else:
        print('=========洗缸插入=========')
        InsertDtl = PlanDyeDTL(nHDRID=nHDRID, nRowNumber=nRowNumber, tUpdateTime=tUpdateTime, sType=sType, bUsable = 1)
        ses.add(InsertDtl)
    ses.commit()
    ses.close()


# 洗缸不可用
def IsHaveXG(nHDRID):
    returnData = []
    for i in ses.query(PlanDyeDTL).filter(and_(PlanDyeDTL.nHDRID == nHDRID, PlanDyeDTL.bUsable == 1)).order_by(PlanDyeDTL.id):
        if i.sType == '洗缸':
            sDict = {
                'nHDRID' : str(i.nHDRID),
                'sType' : i.sType,
            }
            returnData.append(sDict)
    return returnData

# 删除洗缸数据
def DeleteXG_PMC(data):
    nHDRID = data['nHDRID']
    sType = data['sType']
    print('==================')
    print(nHDRID)
    print(sType)

    target = ses.query(PlanDyeDTL).filter(and_(PlanDyeDTL.nHDRID == nHDRID, PlanDyeDTL.sType == sType, PlanDyeDTL.bUsable == 1)).first()

    target.bUsable = 0

    ses.commit()
    ses.close()



    


