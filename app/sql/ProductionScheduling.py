# 获得卡号的详细信息
def GETSchedulingSQL(sMaterialType):
    return "SELECT \
    CASE WHEN bISRush = 1 THEN '#FF0000' \
    WHEN DATEDIFF(HOUR,CONVERT(DATETIME,tFactEndTimeLast),GETDATE()) >72 THEN '#0000FF' \
    WHEN DATEDIFF(HOUR,CONVERT(DATETIME,tFactEndTimeLast),GETDATE()) >= 24 THEN '#FFFF00' ELSE '#008000' END AS sBorderColor \
    ,sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
    ,sCustomerName,sSalesName,sSalesGroupName \
    ,nPSTime,nSETime,nPSSpeed,nSESpeed \
    ,ISNULL(CONVERT(NVARCHAR(10),nPSTemp1) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp8) ,'') AS nPS2Temp \
    ,ISNULL(CONVERT(NVARCHAR(10),nSETemp) + '/' ,'') +  \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp2) + '/' ,'') +  \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp8) ,'') AS nSETemp \
    ,sProductWidth,sProductGMWT,sColorBorder \
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
    ,CASE WHEN B.bISRush = 1 THEN '#FF0000'  ELSE '#008000' END AS sBorderColor \
    ,B.sCardNo,sMaterialNo,B.sMaterialLot,B.sColorNo,B.nFactInPutQty \
    ,B.sCustomerName,B.sSalesName,B.sSalesGroupName \
    ,B.nPSTime,B.nSETime,B.nPSSpeed,B.nSESpeed \
    ,ISNULL(CONVERT(NVARCHAR(10),nPSTemp1) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nPS2Temp8) ,'') AS nPS2Temp \
    ,ISNULL(CONVERT(NVARCHAR(10),nSETemp) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp2) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp3_7) + '/' ,'') + \
    ISNULL(CONVERT(NVARCHAR(10),nSETemp8) ,'') AS nSETemp \
    ,B.sProductWidth,B.sProductGMWT,B.sColorBorder \
    FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL A \
    LEFT JOIN #TEMPTABLE B ON A.sCardNo = B.sCardNo \
    ORDER BY A.nRowNumber \
    DROP TABLE #TEMPTABLE \
    "