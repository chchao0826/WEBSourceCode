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
    ,C.sWorkingProcedureNameLast \
    ,C.sWorkingProcedureNameCurrent \
    ,C.nFactInputQty \
    ,C.nDyeingTime \
    ,CONVERT(CHAR(12),C.sCustomerName) AS sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,C.sColorCode \
    ,A.nRowNumber \
    ,A.sType AS sType \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE NULL END AS sIsStart \
    ,CASE WHEN A.sPlanDX = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN CASE WHEN A.sPlanDye LIKE '%%_%%' THEN RIGHT(A.sPlanDye, LEN(A.sPlanDye) - LEN(LEFT(A.sPlanDye, CHARINDEX('_',A.sPlanDye)))) ELSE '染' END ELSE '染' END AS sDyeingCount /*中控是否排染色*/  \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN \
        CASE WHEN RIGHT(A.sPlanDye,1) = 1 THEN '#3CB371'  \
             WHEN RIGHT(A.sPlanDye,1) = 2 THEN '#83C75D' \
             WHEN RIGHT(A.sPlanDye,1) = 3 THEN '#90EE90' END ELSE NULL END AS sDyeingColor /*中控是否排染色*/ \
    ,C.sWorkCode /*工段颜色*/ \
    ,CASE WHEN C.bISHYS = 1 THEN '#83C75D' ELSE NULL END AS sIsHYS \
    ,CASE WHEN A.nRowNumber = 999 THEN '#98FB98' ELSE NULL END AS bISCheck \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '#5BBD2B' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '#00B2BF' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '#FCF54C' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '#E33539' END AS sOverColor \
    ,C.sWorkingProcedureNameNext \
	,CASE WHEN B.tFactStartTime iS NOT NULL THEN 1 ELSE 0 END AS sIsStart \
	,RIGHT(CONVERT(NVARCHAR(10),dReplyDate,120),5) AS dReplyDate \
	,RIGHT(CONVERT(NVARCHAR(10),dDeliveryDate,120),5) AS dDeliveryDate \
	,CONVERT(NVARCHAR(10),C.sRemark,120) AS sRemark \
	,CASE WHEN C.sIsRush = 1 THEN '急' ELSE ''  END AS sIsRush \
	,ISNULL(C.sISHasHYS,'') AS sISHasHYS \
	,ISNULL(C.sISHasDX,'') AS sISHasDX \
    ,CASE WHEN C.sIsRush = 1 THEN '#3CB371' ELSE ''  END AS sIsRushColor \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A  \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
	LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbWorkingProcedure] E ON E.sWorkingProcedureName = C.sWorkingProcedureNameCurrent \
    WHERE A.bUsable = 1 AND D.ID =  '%s' AND A.bISCheck = 1 AND ISNULL(C.sStatus,'') NOT IN ('取消','中止') \
    ORDER BY A.nRowNumber, A.sType DESC"%(ID)


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
    ,C.sWorkingProcedureNameLast \
    ,C.sWorkingProcedureNameCurrent \
    ,C.nFactInputQty \
    ,C.nDyeingTime \
    ,CONVERT(CHAR(12),C.sCustomerName) AS sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,C.sColorCode \
    ,A.nRowNumber \
    ,A.sType AS sType \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE NULL END AS sIsStart \
    ,CASE WHEN A.sPlanDX = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN CASE WHEN A.sPlanDye LIKE '%%_%%' THEN RIGHT(A.sPlanDye, LEN(A.sPlanDye) - LEN(LEFT(A.sPlanDye, CHARINDEX('_',A.sPlanDye)))) ELSE '染' END ELSE '染' END AS sDyeingCount /*中控是否排染色*/  \
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN \
        CASE WHEN RIGHT(A.sPlanDye,1) = 1 THEN '#3CB371'  \
             WHEN RIGHT(A.sPlanDye,1) = 2 THEN '#83C75D' \
             WHEN RIGHT(A.sPlanDye,1) = 3 THEN '#90EE90' END ELSE NULL END AS sDyeingColor /*中控是否排染色*/ \
    ,C.sWorkCode /*工段颜色*/ \
    ,CASE WHEN C.bISHYS = 1 THEN '#83C75D' ELSE NULL END AS sIsHYS \
    ,CASE WHEN A.nRowNumber = 999 THEN '#98FB98' ELSE NULL END AS bISCheck \
    ,CASE WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 24 THEN '#5BBD2B' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 48 THEN '#00B2BF' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) <= 72 THEN '#FCF54C' \
        WHEN CONVERT(INT,CONVERT(DECIMAL(18,2),DATEDIFF(MINUTE,C.tFactEndTimeLast,GETDATE())) / 60) >72 THEN '#E33539' END AS sOverColor \
    ,C.sWorkingProcedureNameNext \
	,CASE WHEN B.tFactStartTime iS NOT NULL THEN '#FFE1FF' ELSE '' END AS sIsStart \
	,RIGHT(CONVERT(NVARCHAR(10),dReplyDate,120),5) AS dReplyDate \
	,RIGHT(CONVERT(NVARCHAR(10),dDeliveryDate,120),5) AS dDeliveryDate \
	,CONVERT(NVARCHAR(10),C.sRemark,120) AS sRemark \
	,CASE WHEN C.sIsRush = 1 THEN '急' ELSE ''  END AS sIsRush \
	,ISNULL(C.sISHasHYS,'') AS sISHasHYS \
	,ISNULL(C.sISHasDX,'') AS sISHasDX \
    ,CASE WHEN C.sIsRush = 1 THEN '#3CB371' ELSE ''  END AS sIsRushColor \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A  \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID  \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
	LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbWorkingProcedure] E ON E.sWorkingProcedureName = C.sWorkingProcedureNameCurrent \
    WHERE A.bUsable = 1 AND D.ID =  '%s' AND A.bISCheck = 0 AND ISNULL(C.sStatus,'') NOT IN ('取消','中止') \
    ORDER BY C.sWorkRow,E.iOrderNo DESC,E.iWorkLevel DESC,B.tFactStartTime DESC, ISNULL(C.tFactEndTimeLast,GETDATE())"%(ID)


