# 获得卡号的详细信息
def GETSchedulingSQL(sMaterialType):
    return "SELECT \
        CASE WHEN bISRush = 1 THEN '#FFFF00' WHEN A.sLabel = '#FFA54F' THEN  '#FF0000'  ELSE '#008000' END AS sBorderColor \
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
        ,sProductWidth,sProductGMWT,sColorBorder,B.uppTrackJobGUID,sWorkingProcedureNameCurrent,B.sLocation \
        FROM [dbo].[pbCommonDataProductionScheduling] A \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
        WHERE B.bUsable = 1 AND B.sMaterialType = '%s' AND A.uppTrackJobGUID not in (SELECT uppTrackJobGUID FROM pbCommonDataProductionSchedulingDTL) \
        ORDER BY A.nRowNumber, B.sLocation "%(sMaterialType)


def GetSchedulingDtlSQL():
    return "SELECT \
        CASE WHEN bISRush = 1 THEN '#FFFF00' WHEN C.sLabel = '#FFA54F' THEN  '#FF0000'  ELSE '#008000' END AS sBorderColor \
        ,D.sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
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
        ,sProductWidth,sProductGMWT,sColorBorder,A.uppTrackJobGUID,sWorkingProcedureNameCurrent,D.sLocation ,B.sEquipmentNo, A.nHDRID, A.nRowNumber \
        FROM pbCommonDataProductionSchedulingDTL A \
        LEFT JOIN pbCommonDataProductionSchedulingHDR B ON A.nHDRID = B.ID \
        LEFT JOIN [dbo].[pbCommonDataProductionScheduling] C ON A.uppTrackJobGUID = C.uppTrackJobGUID \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase D ON A.uppTrackJobGUID = D.uppTrackJobGUID \
        WHERE D.bUsable = 1 \
        ORDER BY A.nRowNumber"