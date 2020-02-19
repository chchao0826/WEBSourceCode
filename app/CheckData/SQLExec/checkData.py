# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.CheckData.SQL.checkData import JSSearchDataSQL

import re


base = declarative_base()
# 236
session = sessionmaker(bind=engine)
ses = session()


# 研发数据对比执行
def JSSearchData(*args):
    print(args)
    sWorkingProcedureName = args[0]
    sMaterialNoList = args[1]
    # print(sWorkingProcedureName)
    # print(sMaterialNoList)
    sMaterialNo1 = ''
    sMaterialNo2 = ''
    sMaterialNo3 = ''
    sMaterialNo4 = ''
    sMaterialNo5 = ''
    sMaterialNo6 = ''
    sMaterialNo7 = ''
    sMaterialNo8 = ''
    sMaterialNo9 = ''

    varList0 = []
    varList1 = []
    varList2 = []
    varList3 = []
    varList4 = []
    varList5 = []
    varList6 = []
    varList7 = []
    varList8 = []
    varList9 = []
    nNumber = 0
    for i in sMaterialNoList:
        if nNumber == 0:
            sMaterialNo1 = i
        elif nNumber == 1:
            sMaterialNo2 = i
        elif nNumber == 2:
            sMaterialNo3 = i
        elif nNumber == 3:
            sMaterialNo4 = i
        elif nNumber == 4:
            sMaterialNo5 = i
        elif nNumber == 5:
            sMaterialNo6 = i
        elif nNumber == 6:
            sMaterialNo7 = i
        elif nNumber == 7:
            sMaterialNo8 = i
        elif nNumber == 8:
            sMaterialNo9 = i
        nNumber += 1                  

    sSQL = JSSearchDataSQL(sWorkingProcedureName, sMaterialNo1, sMaterialNo2, sMaterialNo3, sMaterialNo4, sMaterialNo5, sMaterialNo6, sMaterialNo7, sMaterialNo8, sMaterialNo9)
    cursor = connect.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(sSQL)
    print(sSQL)
    # 执行sql语句
    row = cursor.fetchone()
    varList0 = []
    varList1 = []
    varList2 = []
    varList3 = []
    varList4 = []
    varList5 = []
    varList6 = []
    varList7 = []
    varList8 = []
    varList9 = []
    returnList = []
    while row:
        print('3222222222222222222222222222')
        print(row)
        print(len(row))
        varList0.append(row[0])
        varList1.append(row[1])
        varList2.append(row[2])
        varList3.append(row[3])
        if len(row) >= 5:
            print('==============5')
            varList4.append(row[4])
        if len(row) >= 6:
            print('==============6')
            varList5.append(row[5])
        if len(row) >= 7:
            print('==============7')
            varList6.append(row[6])
        if len(row) >= 8:
            print('==============8')
            varList7.append(row[7])                                 
        if len(row) >= 9:
            print('==============9')
            varList8.append(row[8])
        if len(row) >= 10:
            print('==============10')
            varList9.append(row[9])        
        row = cursor.fetchone()
    cursor.close()

    nNumber = len(varList0)
    print('==========1212121=========3232')
    print(varList0)
    print(len(varList0))
    print('==========q3212121=========3232')
    if nNumber == 1:
        for i in range(9):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('')
    elif nNumber == 2:
        for i in range(8):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('')     
    elif nNumber == 3:
        for i in range(7):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('') 
    elif nNumber == 4:
        for i in range(6):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('')       
    elif nNumber == 5:
        for i in range(5):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('')                  
    elif nNumber == 6:
        for i in range(4):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('')
    elif nNumber == 7:
        for i in range(3):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('')    
    elif nNumber == 8:
        for i in range(2):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('') 
    elif nNumber == 9:
        for i in range(1):
            varList0.append('')
            varList1.append('')
            varList2.append('')
            varList3.append('')
            varList4.append('')
            varList5.append('')
            varList6.append('')
            varList7.append('')
            varList8.append('')
            varList9.append('') 

    returnList.append(varList0)
    returnList.append(varList1)
    returnList.append(varList2)
    returnList.append(varList3)
    returnList.append(varList4)
    returnList.append(varList5)
    returnList.append(varList6)
    returnList.append(varList7)
    returnList.append(varList8)
    returnList.append(varList9)    



    nNumber = len(returnList[0])
    # if nNumber == 1:
    #     returnList[0].


    print('-------------232323-----------')
    print(varList0)
    print('-------------212881-----------')
    print(returnList)
    print('-------------1299999-----------')

    return returnList




    # # 卡号列表 / 物料编号 / 手感号 / 来源名称 / LOT号 / 规格 / 表ID
    # sCardNoList = []
    # sMaterialNoList = []
    # sFellNoList = []
    # sSourceNameList = []
    # sMaterialLotList = []
    # sMaterialPropertyList = []
    # iIdenList = []
    # # 配检布 : 幅宽 / 码重 / 克重 / 纬密 /
    # nPRWidthList = []
    # nPRYardWeightList = []
    # nPRGMWTList = []
    # sPRWeftDensityList = []
    # # 沸缩 : 幅宽 / 码重 / 克重 / 纬密
    # nFSPRWidthList = []
    # nFSYardWeightList = []
    # nFSGMWTList = []
    # sFSWeftDensityList = []
    # # 水洗 : 机台名 / 速度 / 助剂 / 温度 / 幅宽 / 码重 / 纬密 / 克重
    # sSCMachineNoList = []
    # nSCSpeedList = []
    # sSCTensionList = []
    # nSCTempInList = []
    # nSCPRWidthList = []
    # nSCYardWeightList = []
    # sSCWeftDensityList = []
    # sSCGMWTList = []

    # # 预定 : 机台号 / 速度 / 温度 / 幅宽 / 幅宽设定 / 码重 / 纬密 / 克重
    # sPSMachineNooList = []
    # nPSSpeedoList = []
    # nPSTempList = []
    # sPSWidthoList = []
    # sPSWidthSetList = []
    # nPSYardWeightList = []
    # sPSWeftDensityList = []
    # sPSGMWTList = []

    # # 染色 : 机台 / 温度 / 温度设定 / 助剂 / 纬密 / 幅宽 / 克重 / 码重
    # sDYMachineNoList = []
    # nDYTempList = []
    # sDYVSTempAidList = []
    # sDYAidList = []
    # sDYWeftDensityList = []
    # nDYPRWidthList = []
    # sDYGMWTList = []
    # nDYYardWeightList = []

    # # 成定 : 机台号 / 速度 / 温度 / 助剂 / 幅宽设定 / 幅宽 / 纬密 / 克重
    # sSEMachineNoList = []
    # nSESpeedList = []
    # nSETempList = []
    # sSEAidRecipeList = []
    # sSEWidthSetList = []
    # sSEPRWidthList = []
    # sSEWeftDensityList = []
    # sSEGMWTList = []

    # for i in args[0]:
    #     print(i)
    #     sSQL = JSSearchDataSQL(i)
    #     cursor = connect.cursor()
    #     # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    #     cursor.execute(sSQL)
    #     # 执行sql语句
    #     row = cursor.fetchone()
    #     while row:
    #         sCardNoList.append(row[0])
    #         sMaterialNoList.append(row[1])
    #         sFellNoList.append(row[2])
    #         sSourceNameList.append(row[3])
    #         sMaterialLotList.append(row[4])
    #         sMaterialPropertyList.append(row[5])
    #         nPRWidthList.append(row[6])

    #         nPRYardWeightList.append(row[7])
    #         PRGMWTdict = {
    #             'nPRGMWTLeft': row[8],
    #             'nPRGMWTIn': row[9],
    #             'nPRGMWTRight': row[10],
    #         }
    #         nPRGMWTList.append(PRGMWTdict)
    #         sPRWeftDensityDict = {
    #             'sPRWeftDensityLeft': row[11],
    #             'sPRWeftDensityIn': row[12],
    #             'sPRWeftDensityRight': row[13],
    #         }
    #         sPRWeftDensityList.append(sPRWeftDensityDict)

    #         nFSPRWidthList.append(row[14])
    #         nFSYardWeightList.append(row[15])
    #         nFSGMWTDict = {
    #             'nFSGMWTLeft': row[16],
    #             'nFSGMWTIn': row[17],
    #             'nFSGMWTRight': row[18],
    #         }
    #         nFSGMWTList.append(nFSGMWTDict)
    #         sFSWeftDensityDict = {
    #             'sFSWeftDensityLeft': row[19],
    #             'sFSWeftDensityInList': row[20],
    #             'sFSWeftDensityRight': row[21],
    #         }
    #         sFSWeftDensityList.append(sFSWeftDensityDict)

    #         sSCMachineNoList.append(row[22])
    #         nSCSpeedList.append(row[23])
    #         sSCTensionList.append(row[24])

    #         nSCTempInList.append(row[25])
    #         nSCTempIn2List.append(row[26])
    #         nSCPRWidthList.append(row[27])
    #         nSCYardWeightList.append(row[28])

    #         sSCWeftDensityLeftList.append(row[29])
    #         sSCWeftDensityInoList.append(row[30])
    #         sSCWeftDensityRightoList.append(row[31])
    #         sSCGMWToList.append(row[32])
    #         sPSMachineNooList.append(row[33])
    #         nPSSpeedoList.append(row[34])
    #         nPSTemp2oList.append(row[35])
    #         nPSTemp3_7oList.append(row[36])
    #         nPSTemp8oList.append(row[37])
    #         sPSWidthoList.append(row[38])
    #         sPSWidthSetoList.append(row[39])
    #         nPSYardWeightoList.append(row[40])
    #         sPSWeftDensityRightoList.append(row[41])
    #         sPSWeftDensityInoList.append(row[42])
    #         sPSWeftDensityLeftoList.append(row[43])
    #         sPSGMWTList.append(row[44])
    #         sPSGMWTLeftList.append(row[45])
    #         sPSGMWTInList.append(row[46])
    #         sPSGMWTRightList.append(row[47])
    #         sDYMachineNoList.append(row[48])
    #         nDYTempList.append(row[49])
    #         sDYVSTempAidList.append(row[50])
    #         sDYAidList.append(row[51])
    #         sDYWeftDensityLeftList.append(row[52])
    #         sDYWeftDensityInList.append(row[53])
    #         sDYWeftDensityRightList.append(row[54])
    #         nDYPRWidthList.append(row[55])
    #         sDYGMWTList.append(row[56])
    #         sDYGMWTLeftList.append(row[57])
    #         sDYGMWTInList.append(row[58])
    #         sDYGMWTRightList.append(row[59])
    #         nDYYardWeightList.append(row[60])
    #         sSEMachineNoList.append(row[61])
    #         nSESpeedList.append(row[62])
    #         nSETempList.append(row[63])
    #         nSETemp2List.append(row[64])
    #         nSETemp3_7List.append(row[65])
    #         nSETemp8List.append(row[66])
    #         sSEAidRecipeList.append(row[67])
    #         sSEWidthSetList.append(row[68])
    #         sSEPRWidthList.append(row[69])
    #         sSEWeftDensityLeftList.append(row[70])
    #         sSEWeftDensityInList.append(row[71])
    #         sSEWeftDensityRightList.append(row[72])
    #         sSEGMWTList.append(row[73])
    #         sSEGMWTLeftList.append(row[74])
    #         sSEGMWTInList.append(row[75])
    #         sSEGMWTRightList.append(row[76])
    #         iIdenList.append(row[77])

    #         print(row[1])

    #         # ('E190100974', 'TSS32K014Q-L12', '12', '常熟凯成', '1', '成分:17.18%OP1 82.82%T', '166', '296', '199', '191', '190', '96', '38', None, '148', '358', '270', '255', '269', '119', '47', None, '2#', '20', None, None, None, '140', '276', '94', '37', None, '215', '4#', '16', '150', '180', '200', '180', '165', '168', None, None, '29.5-30', '84', '155', None, None, None, 'E25', '130', '45', 'STF-09：2G/L PR-9000：1%', '88', '34.5', None, '157', '186', None, None, None, '268', '1#', '15', '140', '140', '140', '140', '中浅色3303:5G/L+客供抗菌10-90:10G/L， 深色3303:10G/L+客供抗菌10-90:10G/L', '174', '159', None, '', '31.5', None, '165', '', '', '', 10725)
    #         row = cursor.fetchone()
    #     cursor.close()
    # return sCardNoList, sMaterialNoList, sFellNoList, sSourceNameList, sMaterialLotList, sMaterialPropertyList, nPRWidthList, nPRYardWeightList, nPRGMWTList, sPRWeftDensityList, nFSPRWidthList, nFSYardWeightList, nFSGMWTLeftList, nFSGMWTInList, nFSGMWTRightList, sFSWeftDensityLeftList,
    # sFSWeftDensityInList, sFSWeftDensityRightList, sSCMachineNoList, nSCSpeedList, sSCTensionList, nSCTempInList, nSCTempIn2List, nSCPRWidthList,
    # nSCYardWeightList, sSCWeftDensityLeftList, sSCWeftDensityInoList, sSCWeftDensityRightoList, sSCGMWToList, sPSMachineNooList, nPSSpeedoList,
    # nPSTemp2oList, nPSTemp3_7oList, nPSTemp8oList, sPSWidthoList, sPSWidthSetoList, nPSYardWeightoList, sPSWeftDensityRightoList, sPSWeftDensityInoList,
    # sPSWeftDensityLeftoList, sPSGMWTList, sPSGMWTLeftList, sPSGMWTInList, sPSGMWTRightList, sDYMachineNoList, nDYTempList, sDYVSTempAidList,
    # sDYAidList, sDYWeftDensityLeftList, sDYWeftDensityInList, sDYWeftDensityRightList, nDYPRWidthList, sDYGMWTList, sDYGMWTLeftList, sDYGMWTInList,
    # sDYGMWTRightList, nDYYardWeightList, sSEMachineNoList, nSESpeedList, nSETempList, nSETemp2List, nSETemp3_7List, nSETemp8List, sSEAidRecipeList,
    # sSEWidthSetList, sSEPRWidthList, sSEWeftDensityLeftList, sSEWeftDensityInList, sSEWeftDensityRightList, sSEGMWTList, sSEGMWTLeftList, sSEGMWTInList, sSEGMWTRightList
