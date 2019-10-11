# 预排SQL
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


# 生管预排
# SQL : 未预排的数据
def GetData_NoPlan(sWorkingProcedureName):
    return " \
    SELECT A.ID \
    ,CASE WHEN A.bIsRush = 1 THEN '#FFFF00' WHEN DATEDIFF(HOUR,B.tUpdateTime,GETDATE()) >6 THEN '#FA8072' ELSE '#FFF' END AS sIsRush \
    ,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
    ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty,sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(20),sFactEndTimeLast) AS tFactEndTimeLast,sNotDoneProcedure \
    ,nTJTime,nPSTime,nDyeingTime,nSETime,sCustomerName,sSalesName \
    ,sSalesGroupName,sColorBorder,sOverTime AS nOverTime,bUsable,A.uppTrackJobGUID , A.sLocation ,B.sLabel \
    ,B.uppTrackJobGUID AS uppTrackJobGUIDB \
    ,CONVERT(NVARCHAR(10),A.sRemark) AS sRemark \
    ,A.sWorkingProcedureNameLast,A.sWorkingProcedureNameNext \
    ,A.sReplyDate AS dReplyDate,A.sDeliveryDate AS dDeliveryDate \
    INTO #TEMPTABLE \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase A \
    LEFT JOIN [WebDataBase].[dbo].[pbCommonDataProductionScheduling] B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    WHERE sWorkingProcedureNameCurrent = '%s'  AND bUsable = 1 AND sWorkingProcedureName = '%s' \
    SELECT *FROM #TEMPTABLE \
	WHERE uppTrackJobGUIDB IS NULL \
	ORDER BY sLocation,sMaterialNo\
    DROP TABLE #TEMPTABLE" % (sWorkingProcedureName, sWorkingProcedureName)


# SQL: 已预排的数据
def GetData_Plan(sWorkingProcedureName):
    return "\
    SELECT B.ID \
    ,CASE WHEN B.bIsRush = 1 THEN '#FF0000' WHEN DATEDIFF(HOUR,A.tUpdateTime,GETDATE()) >6 THEN '#FA8072' ELSE '#00FF00' END AS sIsRush,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
    ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty,sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(20),sFactEndTimeLast) AS tFactEndTimeLast,sNotDoneProcedure \
    ,nTJTime,nPSTime,nDyeingTime,nSETime,sCustomerName,sSalesName,sSalesGroupName,sColorBorder,sOverTime AS nOverTime,bUsable,B.uppTrackJobGUID \
    ,CASE WHEN A.sLabel = '2' THEN 'sUrgent' WHEN A.sLabel = '1' OR B.bIsRush = 1 THEN 'ERPUrgent' ELSE '#FFF' END AS sLabel \
    , B.sLocation,CONVERT(NVARCHAR(10),B.sRemark) AS sRemark,B.sWorkingProcedureNameLast,B.sWorkingProcedureNameNext,B.sReplyDate AS dReplyDate,B.sDeliveryDate AS dDeliveryDate \
    FROM [dbo].pbCommonDataProductionScheduling A \
    JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    WHERE A.sType = '%s' AND B.bUsable = 1 \
    ORDER BY sWorkingProcedureNameCurrent,A.nRowNumber, sMaterialNo" % (sWorkingProcedureName)


# SQL: 查找没有的数据
def GetData_AllNoPlan(sVarInput, sWoring):
    return " \
    DECLARE @sVarStr NVARCHAR(20) \
    SET @sVarStr = '%s' \
    SELECT A.ID,CASE WHEN bIsRush = 1 THEN '#FF0000' WHEN DATEDIFF(HOUR,B.tUpdateTime,GETDATE()) >6 THEN '#FA8072' ELSE '#00FF00' END AS sIsRush,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
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