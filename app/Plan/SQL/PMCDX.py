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
    return "DECLARE @sType NVARCHAR(100), @tTime DATETIME \
            SET @sType = '%s' \
            /*找到最后一次更新的数据*/ \
            SELECT TOP 1 @tTime = tUpdateTime  \
            FROM [dbo].[pbCommonDataProductionScheduling] \
            WHERE sType = @sType \
            ORDER BY tUpdateTime DESC \
            SELECT  \
            CASE WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=12 THEN '12' \
            WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=24 THEN '12-24' \
            WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=72 THEN '24-72' \
            WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) >72 THEN '72' END AS  sOverTime \
            ,B.sCustomerName  \
            ,B.sLocation,B.sMaterialNo,B.sMaterialLot,B.sCardNo,B.sColorNo,B.nFactInputQty  \
            ,B.sWorkingProcedureNameLast,B.sWorkingProcedureNameCurrent,B.sWorkingProcedureNameNext  \
            ,B.dReplyDate,B.dDeliveryDate \
            ,B.nTJTime,B.nPSTime,B.nDyeingTime,B.nSETime,B.sSalesGroupName  \
            ,B.sRemark \
            ,CASE WHEN A.bIsFinish = 1 THEN 'sFinish' WHEN A.sLabel = '2' THEN 'sUrgent' WHEN B.sIsRush = '1' or A.sLabel = '1' THEN 'ERPUrgent' ELSE '#FFF' END AS sLabel \
            ,A.uppTrackJobGUID \
            FROM [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A \
            JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo \
            WHERE A.sType = @sType AND A.tUpdateTime = @tTime \
            ORDER BY bIsFinish,nRowNumber" % (sWorkingProcedureName)


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
    return "INSERT INTO [dbo].[pbCommonDataProductionScheduling](sType,nRowNumber,uppTrackJobGUID,tUpdateTime,sLabel,sCardNo) VALUES (%s, %d,%s,%s,%s,%s)"
