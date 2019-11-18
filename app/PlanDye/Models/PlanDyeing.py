# -*-coding:utf-8-*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey, DateTime, Numeric, String, Boolean
from sqlalchemy.orm import sessionmaker, relationship, query
from flask import Flask, render_template, request
from app.config import engine


base = declarative_base()



# 预排主表 机台表
class PlanDyeDTL(base):
    __tablename__ = 'pbCommonDataProductionSchedulingDyeingDTL'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nHDRID = Column(Integer, nullable=True)
    nRowNumber = Column(Integer, nullable=True)
    tUpdateTime = Column(DateTime, nullable=True)

    def __str__(self):
        return self.id


# 更新Dtl数据
def UpdateDtl_PMC(data):

    session = sessionmaker(bind=engine)
    ses = session()

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

