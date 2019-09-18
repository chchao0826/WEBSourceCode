# 看板SQL
# -*-coding:utf-8-*-

'''
工厂平面图
equipmentStatus / storeStatus / WorkingStatus
'''


# 机台状态
def equipmentStatusSQL():
    returnSql = " \
        SELECT \
        ID,sEquipmentNo,sEquipmentName,sWorkingProcedureName \
        ,bUsable,nRowNumber,bIsPMKanBan,bStatus,sColor \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataEquipmentStatus] A \
        ORDER BY A.sWorkingProcedureName,A.nRowNumber DESC"
    return returnSql


# 库存状态百分比
def storeStatusSQL():
    returnSql = "\
        SELECT * \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataWorkingProcedurePre] \
        WHERE sWorkingProcedureName LIKE '%仓%' "
    return returnSql


# 工段状态百分比
def WorkingStatusSQL():
    returnSql = "\
        SELECT * \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataWorkingProcedurePre]"
    return returnSql


# 技术部看板
def JSInformationSQL(sVar):
    returnSql = "SELECT sSalesName, sCardNo, sMaterialNo, tCardTime, sWorkingProcedureName \
        ,sTopColor, sSaleGroupName, tFactStartTime, tFactEndTime, sISKanBanRush, sKanBanRemark \
        ,ID, nCount, nSaleCount, sWorkingProcedureName2, nWorkingProcedureCount, sSalesNo, sSalesGroupNo, sWorkingProcedureNo \
        FROM [dbo].[pbCommonDataJSKanBan] \
        WHERE sSalesNo LIKE '%%%s%%' \
        OR sWorkingProcedureNo LIKE '%%%s%%' \
        OR sSalesGroupNo LIKE '%%%s%%' " %(sVar, sVar, sVar)
    return returnSql


