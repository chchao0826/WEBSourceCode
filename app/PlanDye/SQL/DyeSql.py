# -*- Coding:utf-8 -*-

# 染色预排数据
def allDyeingSql(sEquipmentModelName):
    return"\
    SELECT \
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
    ,C.sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,C.sColorCode \
    ,A.nRowNumber \
    ,A.sType AS nDyeingCount \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE NULL END AS sIsStart \
    ,CASE WHEN A.sPlanOther = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanOther LIKE '%%染色%%' THEN RIGHT(A.sPlanOther,1) ELSE '' END AS sDyeingCount /*中控是否排染色*/ \
    ,CASE WHEN A.sPlanOther LIKE '%%染色%%' THEN \
        CASE WHEN RIGHT(A.sPlanOther,1) = 1 THEN '#3CB371'  \
             WHEN RIGHT(A.sPlanOther,1) = 2 THEN '#83C75D' \
             WHEN RIGHT(A.sPlanOther,1) = 3 THEN '#90EE90' END ELSE NULL END AS sDyeingColor /*中控是否排染色*/ \
    ,C.sWorkCode /*工段颜色*/ \
    ,CASE WHEN C.bISHYS = 1 THEN '#83C75D' ELSE NULL END AS sIsHYS \
    ,CASE WHEN A.nRowNumber = 999 THEN '#98FB98' ELSE NULL END AS bISCheck \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
    JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID \
    JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID \
    JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
    WHERE A.bUsable = 1 AND D.sEquipmentModelName LIKE '%%%s%%' \
    ORDER BY A.nRowNumber, C.sWorkRow"%(sEquipmentModelName)


# 染色机台
def DyeingEquipmentSql(sEquipmentModelName):
    return "SELECT \
    A.ID,A.sEquipmentNo,A.sEquipmentName \
    FROM [pbCommonDataProductionSchedulingDyeingHDR] A \
    WHERE A.sEquipmentModelName LIKE '%%%s%%' "%(sEquipmentModelName)

