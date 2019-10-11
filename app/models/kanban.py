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
class DXKanBan(base):
    __tablename__ = 'pbCommonDataDXKanBan'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sEquipmentNo = Column(String(40), nullable=True)
    sCardNo = Column(String(40), nullable=True)
    sWorkingProcedureName = Column(String(40), nullable=True)
    tFactStartTime = Column(DateTime, nullable=True)
    tFactEndTime = Column(DateTime, nullable=True)
    nRowNumber = Column(Integer, nullable=True)
    sColorNo = Column(String(40), nullable=True)
    sMaterialNo = Column(String(40), nullable=True)
    nQty = Column(Numeric(18,2), nullable=True)
    sCustomerName = Column(String(40), nullable=True)
    sProductWidth = Column(String(40), nullable=True)
    nProductGMWT = Column(String(40), nullable=True)
    nPSSpeed = Column(Numeric(18,2), nullable=True)
    nSESpeed = Column(Numeric(18,2), nullable=True)
    nPSTemp = Column(Numeric(18,2), nullable=True)
    nSETemp = Column(Numeric(18,2), nullable=True)
    sType = Column(String(40), nullable=True)
    nPer = Column(Numeric(18,2), nullable=True)
    uppTrackJobGUID = Column(String(40), nullable=True)
    def __str__(self):
        return self.id


# 定型看板图表
class DXKanBan_chart(base):
    __tablename__ = 'pbCommonDataDXKanBanChart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sEquipmentNo = Column(String(100), nullable=True)
    sCardNo = Column(String(100), nullable=True)
    nRowNumber = Column(Integer, nullable=True)
    nMinss = Column(Numeric(18,2), nullable=True)
    nHeight = Column(Numeric(18,2), nullable=True)
    sBackColor = Column(String(100), nullable=True)
    uppTrackJobGUID = Column(Numeric(18,2), nullable=True)
    bIsShow = Column(Boolean, nullable=True)
    def __str__(self):
        return self.id


# 判断数据是否存在生管预排表中
def DXKanBanData():
    ReturnList = []
    for i in ses.query(DXKanBan).filter(1 == 1).order_by(DXKanBan.sEquipmentNo, DXKanBan.nRowNumber):
        sDict = {
            'ID' : i.id,
            'sEquipmentNo' : i.sEquipmentNo,
            'sCardNo' : i.sCardNo,
            'sWorkingProcedureName' : i.sWorkingProcedureName,
            'sColorNo' : i.sColorNo,
            'nQty' : i.nQty,
            'sMaterialNo' : i.sMaterialNo,
            'sCustomerName' : i.sCustomerName,
            'sProductWidth' : i.sProductWidth,
            'nProductGMWT' : i.nProductGMWT,
            'nPSSpeed' : i.nPSSpeed,
            'nSESpeed' : i.nSESpeed,
            'nPSTemp' : i.nPSTemp,
            'nSETemp' : i.nSETemp,
            'sType' : i.sType,
            'nPer' : i.nPer,
            'uppTrackJobGUID' : i.uppTrackJobGUID,
            'nRowNumber' : i.nRowNumber,
        }
        ReturnList.append(sDict)
    return ReturnList


# 定型看板山积图数据
def DXKanBanChartData():
    ReturnList = []
    for i in ses.query(DXKanBan_chart).filter(DXKanBan_chart.bIsShow == 1).order_by(DXKanBan_chart.sEquipmentNo, DXKanBan_chart.nRowNumber):
        sDict = {
            'ID' : i.id,
            'sEquipmentNo' : i.sEquipmentNo,
            'sCardNo' : i.sCardNo,
            'nRowNumber' : i.nRowNumber,
            'nMinss' : i.nMinss,
            'nHeight' : i.nHeight,
            'sBackColor' : i.sBackColor,
            'uppTrackJobGUID' : i.uppTrackJobGUID,
        }
        ReturnList.append(sDict)
    return ReturnList


