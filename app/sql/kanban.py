# 看板SQL
# -*-coding:utf-8-*-

'''
工厂平面图
equipmentStatus / storeStatus / WorkingStatus
'''


def equipmentStatus():
    # 机台状态
    returnSql = " \
        SELECT \
        ID,sEquipmentNo,sEquipmentName,sWorkingProcedureName \
        ,bUsable,nRowNumber,bIsPMKanBan,bStatus,sColor \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataEquipmentStatus] A \
        ORDER BY A.sWorkingProcedureName,A.nRowNumber DESC"
    return returnSql


def storeStatus():
    # 库存状态百分比
    returnSql = "\
        SELECT * \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataWorkingProcedurePre] \
        WHERE sWorkingProcedureName LIKE '%仓%' "
    return returnSql


def WorkingStatus():
    # 工段状态百分比
    returnSql = "\
        SELECT * \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataWorkingProcedurePre]"
    return returnSql
