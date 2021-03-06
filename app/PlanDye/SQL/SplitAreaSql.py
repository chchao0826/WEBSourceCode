# 通过ID得到确认的数据
def IDGetCheckDataSql(ID):
    return"SELECT \
    D.sEquipmentNo \
    ,A.ID \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '24' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '24-48' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '48-72' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '72以上' END AS sOverTime \
    ,C.sCardNo \
    ,C.sMaterialNo \
    ,C.sMaterialLot \
    ,C.sColorNo \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameLast) AS sWorkingProcedureNameLast \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameCurrent) AS sWorkingProcedureNameCurrent \
    ,C.nFactInputQty \
    ,C.nDyeingTime \
    ,CONVERT(CHAR(12),C.sCustomerName) AS sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,CASE WHEN C.sColorCode IS NULL THEN '#FFF' ELSE C.sColorCode END AS sColorCode \
    ,A.nRowNumber \
    ,A.sType AS sType \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE '#FFF' END AS sIsStartColor \
    ,CASE WHEN A.sPlanDX = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN CASE WHEN A.sPlanDye LIKE '%%_%%' THEN RIGHT(A.sPlanDye, LEN(A.sPlanDye) - LEN(LEFT(A.sPlanDye, CHARINDEX('_',A.sPlanDye)))) ELSE '染' END ELSE '染' END AS sDyeingCount /*中控是否排染色*/  \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN \
        CASE WHEN RIGHT(A.sPlanDye,1) = 1 THEN '#3CB371'  \
             WHEN RIGHT(A.sPlanDye,1) = 2 THEN '#83C75D' \
             WHEN RIGHT(A.sPlanDye,1) = 3 THEN '#90EE90' END ELSE NULL END AS sDyeingColor /*中控是否排染色*/ \
    ,CASE WHEN C.sWorkCode IS NULL THEN NULL ELSE C.sWorkCode END AS  sWorkCode/*工段颜色*/ \
    ,CASE WHEN C.bISHYS = 1 THEN '#83C75D' ELSE NULL END AS sIsHYS \
    ,CASE WHEN A.bISChange = 1 THEN '#98FB98' ELSE NULL END AS bISCheck \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '#5BBD2B' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '#00B2BF' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '#FCF54C' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '#E33539' END AS sOverColor \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameNext) AS sWorkingProcedureNameNext \
	,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#FFE1FF' ELSE '#FFF' END AS sIsStart \
	,RIGHT(CONVERT(NVARCHAR(10),dReplyDate,120),5) AS dReplyDate \
	,RIGHT(CONVERT(NVARCHAR(10),dDeliveryDate,120),5) AS dDeliveryDate \
	,CONVERT(NVARCHAR(10),C.sRemark,120) AS sRemark \
	,CASE WHEN C.sIsRush = 1 THEN '急' ELSE '' END AS sIsRush \
	,ISNULL(C.sISHasHYS,'') AS sISHasHYS \
	,ISNULL(C.sISHasDX,'') AS sISHasDX \
    ,CASE WHEN C.sIsRush = 1 THEN '#3CB371' ELSE NULL END AS sIsRushColor \
    , C.sOrderNo \
    ,CONVERT(CHAR(14),C.sColorName) AS sColorName \
    ,RIGHT(CONVERT(NVARCHAR(16),A.tPlanTime,120),11) AS tPlanTime \
    ,CASE WHEN A.bISCheck = 0 THEN '#FFF' WHEN A.bISCheck = 1 THEN '#7FFFAA' ELSE NULL END AS sCheckColor \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A  \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
	LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbWorkingProcedure] E ON E.sWorkingProcedureName = C.sWorkingProcedureNameCurrent \
    WHERE A.bUsable = 1 AND D.ID =  '%s' AND A.bISCheck = 1 AND ISNULL(C.sStatus,'') NOT IN ('取消','中止') \
    ORDER BY A.nRowNumber, A.sType DESC" % (ID)


# 通过ID得到未确认的数据
def IDGetNotCheckDataSql(ID):
    return"SELECT \
        D.sEquipmentNo \
    ,A.ID \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '24' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '24-48' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '48-72' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '72以上' END AS sOverTime \
    ,C.sCardNo \
    ,C.sMaterialNo \
    ,C.sMaterialLot \
    ,C.sColorNo \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameLast) AS sWorkingProcedureNameLast \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameCurrent) AS sWorkingProcedureNameCurrent \
    ,C.nFactInputQty \
    ,C.nDyeingTime \
    ,CONVERT(CHAR(12),C.sCustomerName) AS sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,CASE WHEN C.sColorCode IS NULL THEN '#FFF' ELSE C.sColorCode END AS sColorCode \
    ,A.nRowNumber \
    ,A.sType AS sType \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE NULL END AS sIsStartColor \
    ,CASE WHEN A.sPlanDX = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN CASE WHEN A.sPlanDye LIKE '%%_%%' THEN RIGHT(A.sPlanDye, LEN(A.sPlanDye) - LEN(LEFT(A.sPlanDye, CHARINDEX('_',A.sPlanDye)))) ELSE '染' END ELSE '染' END AS sDyeingCount /*中控是否排染色*/  \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN \
        CASE WHEN RIGHT(A.sPlanDye,1) = 1 THEN '#3CB371'  \
             WHEN RIGHT(A.sPlanDye,1) = 2 THEN '#83C75D' \
             WHEN RIGHT(A.sPlanDye,1) = 3 THEN '#90EE90' END ELSE NULL END AS sDyeingColor /*中控是否排染色*/ \
    ,CASE WHEN C.sWorkCode IS NULL THEN NULL ELSE C.sWorkCode END AS  sWorkCode/*工段颜色*/ \
    ,CASE WHEN C.bISHYS = 1 THEN '#83C75D' ELSE NULL END AS sIsHYS \
    ,CASE WHEN A.bISChange = 1 THEN '#98FB98' ELSE NULL END AS bISCheck \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '#5BBD2B' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '#00B2BF' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '#FCF54C' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '#E33539' END AS sOverColor \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameNext) AS sWorkingProcedureNameNext \
	,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#FFE1FF' ELSE NULL END AS sIsStart \
	,RIGHT(CONVERT(NVARCHAR(10),dReplyDate,120),5) AS dReplyDate \
	,RIGHT(CONVERT(NVARCHAR(10),dDeliveryDate,120),5) AS dDeliveryDate \
	,CONVERT(NVARCHAR(10),C.sRemark,120) AS sRemark \
	,CASE WHEN C.sIsRush = 1 THEN '急' ELSE '' END AS sIsRush \
	,ISNULL(C.sISHasHYS,'') AS sISHasHYS \
	,ISNULL(C.sISHasDX,'') AS sISHasDX \
    ,CASE WHEN C.sIsRush = 1 THEN '#3CB371' ELSE NULL END AS sIsRushColor \
    , C.sOrderNo \
    ,CONVERT(CHAR(14),C.sColorName) AS sColorName \
    ,RIGHT(CONVERT(NVARCHAR(16),A.tPlanTime,120),11) AS tPlanTime \
    ,CASE WHEN A.bISCheck = 0 THEN '#FFF' WHEN A.bISCheck = 1 THEN '#7FFFAA' ELSE NULL END AS sCheckColor \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A  \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
	LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbWorkingProcedure] E ON E.sWorkingProcedureName = C.sWorkingProcedureNameCurrent \
    WHERE A.bUsable = 1 AND D.ID =  '%s' AND A.bISCheck = 0 AND ISNULL(C.sStatus,'') NOT IN ('取消','中止') \
    ORDER BY C.sWorkRow,E.iOrderNo DESC,E.iWorkLevel DESC,B.tFactStartTime DESC, ISNULL(C.tFactEndTimeLast,GETDATE())" % (ID)


# 所有数据
def IDGetAllDataSql(ID):
    return"SELECT \
    D.sEquipmentNo \
    ,A.ID \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '24' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '24-48' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '48-72' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '72以上' END AS sOverTime \
    ,C.sCardNo \
    ,C.sMaterialNo \
    ,C.sMaterialLot \
    ,C.sColorNo \
    ,C.sWorkingProcedureNameLast \
    ,C.sWorkingProcedureNameCurrent \
    ,C.nFactInputQty \
    ,C.nDyeingTime \
    ,CONVERT(CHAR(12),C.sCustomerName) AS sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,CASE WHEN C.sColorCode IS NULL THEN '#FFF' ELSE C.sColorCode END AS sColorCode \
    ,A.nRowNumber \
    ,A.sType AS sType \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE NULL END AS sIsStartColor \
    ,CASE WHEN A.sPlanDX = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN CASE WHEN A.sPlanDye LIKE '%%_%%' THEN RIGHT(A.sPlanDye, LEN(A.sPlanDye) - LEN(LEFT(A.sPlanDye, CHARINDEX('_',A.sPlanDye)))) ELSE '染' END ELSE '染' END AS sDyeingCount /*中控是否排染色*/  \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN \
        CASE WHEN RIGHT(A.sPlanDye,1) = 1 THEN '#3CB371'  \
             WHEN RIGHT(A.sPlanDye,1) = 2 THEN '#83C75D' \
             WHEN RIGHT(A.sPlanDye,1) = 3 THEN '#90EE90' END ELSE NULL END AS sDyeingColor /*中控是否排染色*/ \
    ,CASE WHEN C.sWorkCode IS NULL THEN NULL ELSE C.sWorkCode END AS  sWorkCode/*工段颜色*/ \
    ,CASE WHEN C.bISHYS = 1 THEN '#83C75D' ELSE NULL END AS sIsHYS \
    ,CASE WHEN A.bISChange = 1 THEN '#98FB98' ELSE NULL END AS bISCheck \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '#5BBD2B' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '#00B2BF' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '#FCF54C' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '#E33539' END AS sOverColor \
    ,CONVERT(NVARCHAR(4),C.sWorkingProcedureNameNext) AS sWorkingProcedureNameNext \
	,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#FFE1FF' ELSE NULL END AS sIsStart \
	,RIGHT(CONVERT(NVARCHAR(10),dReplyDate,120),5) AS dReplyDate \
	,RIGHT(CONVERT(NVARCHAR(10),dDeliveryDate,120),5) AS dDeliveryDate \
	,CONVERT(NVARCHAR(10),C.sRemark,120) AS sRemark \
	,CASE WHEN C.sIsRush = 1 THEN '急' ELSE '' END AS sIsRush \
	,ISNULL(C.sISHasHYS,'') AS sISHasHYS \
	,ISNULL(C.sISHasDX,'') AS sISHasDX \
    ,CASE WHEN C.sIsRush = 1 THEN '#3CB371' ELSE NULL END AS sIsRushColor \
    , C.sOrderNo \
    ,CONVERT(CHAR(14),C.sColorName) AS sColorName \
    ,RIGHT(CONVERT(NVARCHAR(16),A.tPlanTime,120),11) AS tPlanTime \
    ,CASE WHEN A.bISCheck = 0 THEN NULL WHEN A.bISCheck = 1 THEN '#7FFFAA' ELSE NULL END AS sCheckColor \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A  \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
	LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbWorkingProcedure] E ON E.sWorkingProcedureName = C.sWorkingProcedureNameCurrent \
    WHERE A.bUsable = 1 AND D.ID =  '%s' AND ISNULL(C.sStatus,'') NOT IN ('取消','中止') \
    ORDER BY A.bISCheck DESC ,CASE WHEN A.bISCheck = 1 THEN A.nRowNumber ELSE 999 END ,C.sWorkRow ,B.tFactStartTime DESC, ISNULL(C.tFactEndTimeLast,GETDATE())" % (ID)


# 在点击保存的时候更新机台回253Sql
# def UpdateEquipmentTo253Sql():
#     return "SELECT A.uppTrackJobGUID,A.nHDRID,B.sEquipmentNo,B.sEquipmentName,B.uemEquipmentGUID \
#         iNTO #TEMPTABLE1 \
#         FROM [198.168.6.236].[WebDataBase].[dbo].pbCommonDataProductionSchedulingDyeingDTL A \
#         JOIN [198.168.6.236].[WebDataBase].[dbo].pbCommonDataProductionSchedulingDyeingHDR B ON A.nHDRID = B.ID \
#         WHERE A.bIScheck = 1 AND A.bUsable = 1 \
#         SELECT A.uGUID AS uppTrackJobGUID,B.uGUID AS upsWorkFlowCardGUID, B.sEquipmentPrepareName, B.sEquipmentPrepareNo, B.uemEquipmentPrepareGUID \
#         INTO #TEMPTABLE2  \
#         FROM #TEMPTABLE1 C \
# 		JOIN [HSWarpERP_NJYY].[dbo].ppTrackJob A ON C.uppTrackJobGUID = A.uGUID \
#         JOIN [HSWarpERP_NJYY].[dbo].psWorkFlowCard B ON A.upsWorkFlowCardGUID = B.uGUID \
#         UPDATE #TEMPTABLE2 \
#         SET sEquipmentPrepareName = B.sEquipmentName \
#         ,sEquipmentPrepareNo = B.sEquipmentNo \
#         ,uemEquipmentPrepareGUID = B.uemEquipmentGUID \
#         FROM #TEMPTABLE2 A \
#         JOIN #TEMPTABLE1 B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
#         WHERE sEquipmentPrepareNo != B.sEquipmentNo \
#         UPDATE [HSWarpERP_NJYY].[dbo].psWorkFlowCard \
#         SET sEquipmentPrepareName = B.sEquipmentPrepareName \
#         ,sEquipmentPrepareNo = B.sEquipmentPrepareNo \
#         ,uemEquipmentPrepareGUID = B.uemEquipmentPrepareGUID \
#         FROM [HSWarpERP_NJYY].[dbo].psWorkFlowCard A \
#         JOIN #TEMPTABLE2 B ON A.uGUID = B.upsWorkFlowCardGUID \
#         SELECT * FROM #TEMPTABLE2 \
#         DROP TABLE #TEMPTABLE1 \
#         DROP TABLE #TEMPTABLE2 "
