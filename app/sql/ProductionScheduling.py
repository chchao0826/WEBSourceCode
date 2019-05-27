# 获得卡号的详细信息
def GETSchedulingSQL(sMaterialType):
    return "SELECT \
    CASE WHEN bISRush = 1 THEN '#FF0000' END AS sBorderColor \
    ,sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
    ,sCustomerName,sSalesGroupName \
    ,CASE WHEN sWorkingProcedureName = '预定' THEN \
    ISNULL(CONVERT(NVARCHAR(10),nPSTemp1) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp8) ,'') \
    ELSE ISNULL(CONVERT(NVARCHAR(10),nSETemp) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp8) ,'') END nTemp \
    ,CASE WHEN sWorkingProcedureName = '预定' THEN nPSSpeed ELSE nSESpeed END AS nSpeed \
    ,CASE WHEN sWorkingProcedureName = '预定' THEN nPSTime ELSE nSETime END AS nTime \
    ,sProductWidth,sProductGMWT,sColorBorder,uppTrackJobGUID,sWorkingProcedureName \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataProductionSchedulingBase] \
    WHERE bIsScheduling = 1  AND bUsable = 1 AND sType = '整理' AND sMaterialType = '%s' AND sCardNo NOT IN (SELECT sCardNo FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL) "%(sMaterialType)


def GetSchedulingDtlSQL():
    return " \
    SELECT A.* \
    INTO #TEMPTABLE \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataProductionSchedulingBase] A \
    JOIN ( \
    SELECT sCardNo,MIN(iOrderProcedure) AS iOrderProcedure \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataProductionSchedulingBase] \
    GROUP BY sCardNo \
    ) B ON A.iOrderProcedure = B.iOrderProcedure AND A.sCardNo = B.sCardNo \
    SELECT A.ID,A.nHDRID,A.nRowNumber \
    ,CASE WHEN B.bISRush = 1 THEN '#FF0000'  ELSE '#008000' END AS sBorderColor\
    ,B.sCardNo,sMaterialNo,B.sMaterialLot,B.sColorNo,B.nFactInPutQty \
    ,B.sCustomerName,B.sSalesName,B.sSalesGroupName \
    ,CASE WHEN sWorkingProcedureName = '预定' THEN \
    ISNULL(CONVERT(NVARCHAR(10),nPSTemp1) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp8) ,'') \
    ELSE ISNULL(CONVERT(NVARCHAR(10),nSETemp) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp8) ,'') END nTemp \
    ,CASE WHEN sWorkingProcedureName = '预定' THEN nPSSpeed ELSE nSESpeed END AS nSpeed \
    ,CASE WHEN sWorkingProcedureName = '预定' THEN nPSTime ELSE nSETime END AS nTime \
    ,B.sProductWidth,B.sProductGMWT,B.sColorBorder,B.uppTrackJobGUID,sWorkingProcedureName \
    FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL A \
    LEFT JOIN #TEMPTABLE B ON A.sCardNo = B.sCardNo \
    ORDER BY A.nRowNumber \
    DROP TABLE #TEMPTABLE \
    "