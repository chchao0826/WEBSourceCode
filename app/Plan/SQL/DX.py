# -*-coding:utf-8-*-


# 获得卡号的详细信息
def NoDXPlanSQL(sWorkingProcedureName):
    return "DECLARE @sWorkingProcedureName NVARCHAR(100) \
            SET @sWorkingProcedureName = '%s' \
            CREATE TABLE #TEMP( \
            sWorkingProcedureName NVARCHAR(100), \
            tUpdateTime DATETIME, \
            sLabel NVARCHAR(100), \
            sCardNo NVARCHAR(100), \
            bUsable BIT, \
            upptrackJobGUID uniqueidentifier \
            ) \
            iF @sWorkingProcedureName = '预定' \
            BEGIN \
            INSERT INTO #TEMP \
            SELECT '预定' AS sWorkingProcedureName  \
            ,tUpdateTime, sLabel,CONVERT(NVARCHAR(100),NULL) AS sCardNo,CONVERT(BIT,1) AS bUsable,upptrackJobGUID AS upptrackJobGUID  \
            FROM [dbo].[pbCommonDataProductionScheduling] A \
            WHERE A.bIsFinish IS NULL AND sType iN ('预定', '水洗1', '水洗2') \
            AND upptrackJobGUID NOT IN (SELECT uppTrackJobGUID FROM pbCommonDataProductionSchedulingDTL) \
            END \
            iF @sWorkingProcedureName = '成定型' \
            BEGIN \
            INSERT INTO #TEMP \
            SELECT '成定型' AS sWorkingProcedureName  \
            ,tUpdateTime, sLabel,CONVERT(NVARCHAR(100),NULL) AS sCardNo,CONVERT(BIT,1) AS bUsable,upptrackJobGUID AS upptrackJobGUID \
            FROM [dbo].[pbCommonDataProductionScheduling] A \
            WHERE A.bIsFinish IS NULL AND sType iN ('成定型') \
            AND upptrackJobGUID NOT IN (SELECT uppTrackJobGUID FROM pbCommonDataProductionSchedulingDTL) \
            END \
            SELECT CASE WHEN bISRush = 1 OR A.sLabel = '1' THEN '#FFFF00' WHEN A.sLabel = '#FFA54F' OR A.sLabel = '2' THEN  '#FFA54F'  ELSE '#FFFFFF' END AS sBorderColor \
            ,B.sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
            ,sCustomerName,sSalesGroupName \
            ,CASE WHEN A.sWorkingProcedureName = @sWorkingProcedureName THEN nPS2Temp3_7 ELSE nSETemp3_7 END nTemp \
            ,CASE WHEN A.sWorkingProcedureName = @sWorkingProcedureName THEN nPSSpeed ELSE nSESpeed END AS nSpeed \
            ,CASE WHEN A.sWorkingProcedureName = @sWorkingProcedureName THEN nPSTime  ELSE nSETime END AS nTime \
            ,sProductWidth,sProductGMWT,sColorBorder,B.uppTrackJobGUID,sWorkingProcedureNameCurrent,B.sLocation \
            ,B.sWorkingProcedureNameLast,B.sWorkingProcedureNameNext,B.sMaterialType \
            FROM #TEMP A \
            JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.upptrackJobGUID = B.upptrackJobGUID \
            DROP TABLE #TEMP"%(sWorkingProcedureName)


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
            CASE WHEN bISRush = 1 OR C.sLabel = '1' THEN '#FFFF00' WHEN C.sLabel = '#FFA54F' OR C.sLabel = '2' THEN  '#FFA54F'  ELSE '#FFFFFF' END AS sBorderColor \
            ,D.sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty \
            ,sCustomerName,sSalesGroupName \
            ,CASE WHEN sWorkingProcedureName = '预定' THEN nPS2Temp3_7 ELSE nSETemp3_7 END nTemp \
            ,CASE WHEN sWorkingProcedureName = '预定' THEN nPSSpeed ELSE nSESpeed END AS nSpeed \
            ,CASE WHEN sWorkingProcedureName = '预定' THEN nPSTime ELSE nSETime END AS nTime \
            ,sProductWidth,sProductGMWT,sColorBorder,A.uppTrackJobGUID,sWorkingProcedureNameCurrent,D.sLocation ,B.sEquipmentNo, A.nHDRID, A.nRowNumber \
            ,D.sWorkingProcedureNameLast \
            ,D.sWorkingProcedureNameNext \
            ,D.sMaterialType \
            FROM pbCommonDataProductionSchedulingDTL A \
            JOIN pbCommonDataProductionSchedulingHDR B ON A.nHDRID = B.ID \
            JOIN [dbo].[pbCommonDataProductionScheduling] C ON A.uppTrackJobGUID = C.uppTrackJobGUID \
            JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase D ON A.uppTrackJobGUID = D.uppTrackJobGUID \
            WHERE C.bIsFinish IS NULL AND A.nHDRID IN ('%s', '%s', '%s', '%s', '%s') \
            ORDER BY A.nRowNumber" % (nHDRID1, nHDRID2, nHDRID3, nHDRID4, nHDRID5)
