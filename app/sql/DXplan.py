# -*-coding:utf-8-*-
# 获得卡号的详细信息
def NoDXPlanSQL(sWorkingProcedureName):
    sWorkingProcedureName2 = ''
    if sWorkingProcedureName == '预定':
        sWorkingProcedureName2 = '水洗'
    return "SELECT \
        CASE WHEN bISRush = 1 THEN '#FFFF00' WHEN A.sLabel = '#FFA54F' THEN  '#FFA54F'  ELSE '#FFFFFF' END AS sBorderColor \
        ,sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
        ,sCustomerName,sSalesGroupName \
        ,CASE WHEN sWorkingProcedureName = '预定' THEN \
        ISNULL(CONVERT(NVARCHAR(10),nPSTemp1),'') ELSE '' END nTemp \
        ,CASE WHEN sWorkingProcedureName IN ('预定','水洗') THEN nPSSpeed END AS nSpeed \
        ,CASE WHEN sWorkingProcedureName IN ('预定','水洗') THEN nPSTime  END AS nTime \
        ,sProductWidth,sProductGMWT,sColorBorder,B.uppTrackJobGUID,sWorkingProcedureNameCurrent,B.sLocation \
        FROM [dbo].[pbCommonDataProductionScheduling] A \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
        WHERE B.bUsable = 1 \
        AND sWorkingProcedureName IN ('%s','%s') \
        AND A.uppTrackJobGUID not in (SELECT uppTrackJobGUID FROM pbCommonDataProductionSchedulingDTL) \
        ORDER BY sMaterialNo, A.nRowNumber,  B.sLocation "%(sWorkingProcedureName, sWorkingProcedureName2)


# 已经预排的数据,没有输入机台号即为所有
def DXPlanSQL(nHDRID):
    nHDRID1 = ''
    nHDRID2 = ''
    nHDRID3 = ''
    nHDRID4 = ''
    nHDRID5 = ''
    nHDRID1 = nHDRID
    if nHDRID == '':
        nHDRID1 = 1    
        nHDRID2 = 2       
        nHDRID3 = 3       
        nHDRID4 = 4       
        nHDRID5 = 5       
    return "SELECT \
        CASE WHEN bISRush = 1 THEN '#FFFF00' WHEN C.sLabel = '#FFA54F' THEN  '#FFA54F'  ELSE '#FFFFFF' END AS sBorderColor \
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
        JOIN pbCommonDataProductionSchedulingHDR B ON A.nHDRID = B.ID \
        JOIN [dbo].[pbCommonDataProductionScheduling] C ON A.uppTrackJobGUID = C.uppTrackJobGUID \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase D ON A.uppTrackJobGUID = D.uppTrackJobGUID \
        WHERE D.bUsable = 1 AND A.nHDRID IN ('%s', '%s', '%s', '%s', '%s') \
        ORDER BY A.nRowNumber"%(nHDRID1, nHDRID2, nHDRID3, nHDRID4, nHDRID5)

