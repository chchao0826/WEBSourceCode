def GetSchedulingSQL_ZL_PMC(sWorkingProcedureName, sWorkingProcedureName2):
    return "SELECT A.ID,CASE WHEN bIsRush = 1 THEN '#FFFF00' ELSE '#FFF' END AS sIsRush,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
    ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty,sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(20),tFactEndTimeLast) AS tFactEndTimeLast,sNotDoneProcedure \
    ,nTJTime,nPSTime,nDyeingTime,nSETime,sCustomerName,sSalesName,sSalesGroupName,sColorBorder,nOverTime,bUsable,A.uppTrackJobGUID \
    , A.sLocation ,B.sLabel ,B.uppTrackJobGUID AS uppTrackJobGUIDB \
    INTO #TEMPTABLE \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase A \
    LEFT JOIN [dbo].[pbCommonDataProductionScheduling] B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    WHERE sWorkingProcedureNameCurrent = '%s' AND bUsable = 1 AND sWorkingProcedureName = '%s'\
    DELETE #TEMPTABLE \
    WHERE uppTrackJobGUIDB IS NOT NULL \
    SELECT *FROM #TEMPTABLE ORDER BY sLocation\
    DROP TABLE #TEMPTABLE"%(sWorkingProcedureName, sWorkingProcedureName2)

def GetSchedulingSQL_ZL_PMCHDR(sType):
    return "SELECT \
    B.ID,CASE WHEN bIsRush = 1 THEN '#FF0000' ELSE '#00FF00' END AS sIsRush,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
    ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty,sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(20),tFactEndTimeLast) AS tFactEndTimeLast,sNotDoneProcedure \
    ,nTJTime,nPSTime,nDyeingTime,nSETime,sCustomerName,sSalesName,sSalesGroupName,sColorBorder,nOverTime,bUsable,B.uppTrackJobGUID,A.sLabel, B.sLocation \
    FROM [dbo].pbCommonDataProductionScheduling A \
    JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    WHERE A.sType = '%s' AND B.bUsable = 1\
    ORDER BY A.nRowNumber"%(sType)


def SearchAllCard(sVarInput, sWorkingProcedureName):
    return " \
    DECLARE @sVarStr NVARCHAR(20) \
    SET @sVarStr = '%s' \
    SELECT A.ID,CASE WHEN bIsRush = 1 THEN '#FF0000' ELSE '#00FF00' END AS sIsRush,sCardNo,sMaterialNo,sMaterialLot,sColorNo \
    ,ISNULL(nFactInputQty,nPlanOutputQty) AS nFactInputQty,sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(20),tFactEndTimeLast) AS tFactEndTimeLast,sNotDoneProcedure \
    ,nTJTime,nPSTime,nDyeingTime,nSETime,sCustomerName,sSalesName,sSalesGroupName,sColorBorder,nOverTime,bUsable,A.uppTrackJobGUID \
    , A.sLocation ,B.ID AS IDB \
	INTO #TEMPTABLE \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonDataProductionSchedulingBase A \
	LEFT JOIN [dbo].[pbCommonDataProductionScheduling] B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    WHERE (sCardNo LIKE '%%'+@sVarStr+'%%' \
    OR sMaterialNo LIKE '%%'+@sVarStr+'%%' \
    OR sColorNo LIKE '%%'+@sVarStr+'%%' \
    OR sWorkingProcedureNameCurrent LIKE '%%'+@sVarStr+'%%' \
    OR sSalesGroupName LIKE '%%'+@sVarStr+'%%' \
    OR sSalesName LIKE '%%'+@sVarStr+'%%') AND bUsable = 1 AND A.sWorkingProcedureName = '%s' \
    SELECT *FROM #TEMPTABLE \
	WHERE IDB IS NULL \
	DROP TABLE #TEMPTABLE \
    "%(sVarInput, sWorkingProcedureName)
