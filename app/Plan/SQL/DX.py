# -*-coding:utf-8-*-


# 获得卡号的详细信息
def NoDXPlanSQL(sWorkingProcedureName):
    return "DECLARE @sWorkingProcedureName NVARCHAR(100),@tTime DATETIME \
            SET @sWorkingProcedureName = '%s' \
            /*找到最后一次更新的数据*/ \
            SELECT TOP 1 @tTime = tUpdateTime  \
            FROM [dbo].[pbCommonDataProductionScheduling] \
            WHERE sType = @sWorkingProcedureName \
            ORDER BY tUpdateTime DESC \
            SELECT \
            CASE WHEN B.sIsRush = 1 OR A.sLabel = '1' THEN '#FFFF00' WHEN A.sLabel = '#FFA54F' OR A.sLabel = '2' THEN  '#FFA54F'  ELSE '#FFFFFF' END AS sBorderColor \
            ,B.sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
            ,sCustomerName,sSalesGroupName \
            ,CASE WHEN A.sType IN ('预定', '水洗1', '水洗2') THEN B.nPSTemp ELSE B.nSETemp END nTemp \
            ,CASE WHEN A.sType IN ('预定', '水洗1', '水洗2') THEN B.nPSSpeed ELSE B.nSESpeed END AS nSpeed \
            ,CASE WHEN A.sType IN ('预定', '水洗1', '水洗2') THEN B.nPSTime  ELSE B.nSETime END AS nTime \
            ,sProductWidth,sProductGMWT,sColorBorder,A.uppTrackJobGUID,sWorkingProcedureNameCurrent,B.sLocation \
            ,B.sWorkingProcedureNameLast,B.sWorkingProcedureNameNext,B.sType \
            FROM [dbo].[pbCommonDataProductionScheduling] A \
            JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo \
            WHERE A.sType = @sWorkingProcedureName AND tUpdateTime = @tTime AND ISNULL(A.bIsFinish,0) = 0 \
            AND A.uppTrackJobGUID NOT IN (SELECT uppTrackJobGUID FROM pbCommonDataProductionSchedulingDTL WHERE bUsable = 1) \
            ORDER BY nRowNumber"%(sWorkingProcedureName)


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
    return "SELECT uppTrackJobGUID,MAX(tUpdateTime) AS tUpdateTime \
            iNTO #TEMP \
            FROM [pbCommonDataProductionScheduling] \
            WHERE bIsFinish IS NULL \
            GROUP BY uppTrackJobGUID \
            SELECT \
            CASE WHEN sISRush = 1 OR C.sLabel = '1' THEN '#FFFF00' WHEN C.sLabel = '#FFA54F' OR C.sLabel = '2' THEN  '#FFA54F'  ELSE '#FFFFFF' END AS sBorderColor \
            ,D.sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
            ,sCustomerName,sSalesGroupName \
            ,CASE WHEN C.sType IN ('预定','水洗1','水洗2') THEN nPSTemp ELSE nSETemp END nTemp \
            ,CASE WHEN C.sType IN ('预定','水洗1','水洗2') THEN nPSSpeed ELSE nSESpeed END AS nSpeed \
            ,CASE WHEN C.sType IN ('预定','水洗1','水洗2') THEN nPSTime ELSE nSETime END AS nTime \
            ,sProductWidth,sProductGMWT,sColorBorder,A.uppTrackJobGUID,sWorkingProcedureNameCurrent,D.sLocation ,B.sEquipmentNo, A.nHDRID, A.nRowNumber \
            ,D.sWorkingProcedureNameLast \
            ,D.sWorkingProcedureNameNext \
            ,D.sType AS sMaterialType \
            FROM pbCommonDataProductionSchedulingDTL A \
            JOIN pbCommonDataProductionSchedulingHDR B ON A.nHDRID = B.ID \
            JOIN [dbo].[pbCommonDataProductionScheduling] C ON A.uppTrackJobGUID = C.uppTrackJobGUID \
            JOIN [dbo].pbCommonDataProductionSchedulingBase D ON C.sCardNo = D.sCardNo  \
            JOIN #TEMP E ON E.uppTrackJobGUID = C.uppTrackJobGUID AND E.tUpdateTime = C.tUpdateTime \
            WHERE C.bIsFinish IS NULL AND A.nHDRID IN ('%s', '%s', '%s', '%s', '%s') AND A.bUsable = 1 \
            ORDER BY A.nRowNumber \
            DROP TABLE #TEMP " % (nHDRID1, nHDRID2, nHDRID3, nHDRID4, nHDRID5)
