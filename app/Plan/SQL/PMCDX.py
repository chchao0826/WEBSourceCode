# -*-coding:utf-8-*-


def SearchWoringSQL(sWorkingProcedureNo):
    return " \
    SELECT sWorkingProcedureName \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbWorkingProcedure \
    WHERE sWorkingProcedureNo = '%s' " % (sWorkingProcedureNo)


# 通过机台类型搜索机台号
def SearchEquipmentSQL(sEquipmentModelName):
    return " \
    SELECT B.sEquipmentModelName \
    ,A.sEquipmentNo,sEquipmentName,A.uGUID AS uemEquipmentGUID \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].emEquipment A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].emEquipmentModel B ON A.uemEquipmentModelGUID = B.uGUID \
    WHERE b.sEquipmentModelName = '%s'  AND A.bUsable = 1 " % (sEquipmentModelName)


# 去除序号
def WipeNumber(Feild):
    if Feild.find('1') != -1:
        Feild = Feild.split('1')[0]
    elif Feild.find('2') != -1:
        Feild = Feild.split('2')[0]
    return Feild


# 生管预排
# SQL : 未预排的数据
def GetData_NoPlan(sWorkingProcedureName):
    sWorkingProcedureNameNoNumber = WipeNumber(sWorkingProcedureName)
    return "SELECT sOverTime AS nOverTime,sCustomerName \
        ,A.sLocation,sMaterialNo,sMaterialLot,A.sCardNo,sColorNo \
        ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty \
        ,A.sWorkingProcedureNameLast,A.sWorkingProcedureNameCurrent,A.sWorkingProcedureNameNext  \
        ,A.sReplyDate AS dReplyDate,A.sDeliveryDate AS dDeliveryDate \
        ,nTJTime,nPSTime,nDyeingTime,nSETime,sSalesGroupName  \
        ,CONVERT(NVARCHAR(10),A.sRemark) AS sRemark \
        ,CASE WHEN B.sLabel = '2' THEN 'sUrgent' WHEN A.bIsRush = '1' THEN 'ERPUrgent' ELSE '#FFF' END AS sLabel \
        ,A.uppTrackJobGUID \
        ,B.uppTrackJobGUID AS uppTrackJobGUIDB \
        INTO #TEMPTABLE \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase A \
        LEFT JOIN [WebDataBase].[dbo].[pbCommonDataProductionScheduling] B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
        WHERE sWorkingProcedureNameCurrent = '%s'  AND bUsable = 1 AND sWorkingProcedureName = '%s' \
        SELECT *FROM #TEMPTABLE \
        WHERE uppTrackJobGUIDB IS NULL \
        ORDER BY sLocation,sMaterialNo \
        DROP TABLE #TEMPTABLE" % (sWorkingProcedureNameNoNumber, sWorkingProcedureNameNoNumber)


# SQL: 已预排的数据
def GetData_Plan(sWorkingProcedureName):
    return "SELECT \
        CASE WHEN sType LIKE '%%1%%' OR sType LIKE '%%2%%' THEN '预定' ELSE sType END AS  sWorkingProcedureName  \
        ,tUpdateTime, sLabel,CONVERT(NVARCHAR(100),NULL) AS sCardNo,CONVERT(BIT,1) AS bUsable,upptrackJobGUID AS upptrackJobGUID  \
        INTO #TEMP \
        FROM [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A \
        WHERE sType = '%s' AND ISNULL(bIsFinish,0) = 0 \
        UPDATE #TEMP \
        SET sCardNo = B.sCardNo \
        FROM #TEMP A \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.upptrackJobGUID = B.upptrackJobGUID \
        UPDATE #TEMP \
        SET bUsable = 0 \
        FROM #TEMP A \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo AND A.sWorkingProcedureName = B.sWorkingProcedureName AND B.bUsable = 0 \
        DELETE #TEMP WHERE bUsable = 0 \
        SELECT sOverTime AS nOverTime,sCustomerName \
        ,A.sLocation,sMaterialNo,sMaterialLot,A.sCardNo,sColorNo \
        ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty \
        ,A.sWorkingProcedureNameLast,A.sWorkingProcedureNameCurrent,A.sWorkingProcedureNameNext  \
        ,A.sReplyDate AS dReplyDate,A.sDeliveryDate AS dDeliveryDate \
        ,nTJTime,nPSTime,nDyeingTime,nSETime,sSalesGroupName  \
        ,CONVERT(NVARCHAR(10),A.sRemark) AS sRemark \
        ,CASE WHEN B.sLabel = '2' THEN 'sUrgent' WHEN A.bIsRush = '1' THEN 'ERPUrgent' ELSE '#FFF' END AS sLabel \
        ,A.uppTrackJobGUID \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase A \
        JOIN #TEMP B ON A.upptrackJobGUID = B.upptrackJobGUID \
        DROP TABLE #TEMP" % (sWorkingProcedureName)


# SQL: 查找没有的数据
def GetData_AllNoPlan(sVarInput, sWoring):
    return " \
    DECLARE @sVarStr NVARCHAR(20) \
    SET @sVarStr = '%s' \
    SELECT A.ID,CASE WHEN bIsRush = 1 THEN '#FF0000' END AS sIsRush,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
    ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty,sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(20),sFactEndTimeLast) AS tFactEndTimeLast,sNotDoneProcedure \
    ,nTJTime,nPSTime,nDyeingTime,nSETime,sCustomerName,sSalesName,sSalesGroupName,sColorBorder,sOverTime AS nOverTime,bUsable,A.uppTrackJobGUID \
    , A.sLocation , A.sWorkingProcedureNameLast, A.sWorkingProcedureNameNext,A.sReplyDate AS dReplyDate,A.sDeliveryDate AS dDeliveryDate ,CONVERT(NVARCHAR(10),A.sRemark) AS sRemark,B.ID AS IDB \
	INTO #TEMPTABLE \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase A \
	LEFT JOIN [dbo].[pbCommonDataProductionScheduling] B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    WHERE (sCardNo LIKE '%%'+@sVarStr+'%%' \
    OR sMaterialNo LIKE '%%'+@sVarStr+'%%' \
    OR sColorNo LIKE '%%'+@sVarStr+'%%' \
    OR sWorkingProcedureNameCurrent LIKE '%%'+@sVarStr+'%%' \
    OR sSalesGroupName LIKE '%%'+@sVarStr+'%%' \
    OR sSalesName LIKE '%%'+@sVarStr+'%%') AND bUsable = 1 AND A.sWorkingProcedureName = '%s'\
    SELECT *FROM #TEMPTABLE \
	WHERE IDB IS NULL \
	DROP TABLE #TEMPTABLE \
    " % (sVarInput, sWoring)


# 插入数据
def InsertImportData():
    return "INSERT INTO [dbo].[pbCommonDataProductionScheduling](sType,nRowNumber,uppTrackJobGUID,tUpdateTime,sLabel) VALUES (%s, %d,%s,%s,%s)"
