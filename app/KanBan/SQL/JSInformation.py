# -*-coding:utf-8-*-


# 技术部看板
def JSInformationSQL(sVar):
    returnSql = "SELECT sSalesName, sCardNo, sMaterialNo, tCardTime, sWorkingProcedureName \
        ,sTopColor, sSaleGroupName, tFactStartTime, tFactEndTime, sISKanBanRush, sKanBanRemark \
        ,ID, nCount, nSaleCount, sWorkingProcedureName2, nWorkingProcedureCount, sSalesNo, sSalesGroupNo, sWorkingProcedureNo \
        FROM [dbo].[pbCommonDataJSKanBan] \
        WHERE sSalesNo LIKE '%%%s%%' \
        OR sWorkingProcedureNo LIKE '%%%s%%' \
        OR sSalesGroupNo LIKE '%%%s%%' " % (sVar, sVar, sVar)
    return returnSql
