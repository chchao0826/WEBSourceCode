# -*- Coding:utf-8 -*-

# 染色预排数据
def allDyeingSql(sEquipmentModelName):
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
    ,CONVERT(NVARCHAR(16),C.sCustomerName) AS sCustomerName \
    ,C.sSalesGroupName \
    ,C.sSalesName \
    ,C.sColorCode \
    ,A.nRowNumber \
    ,A.sType AS nDyeingCount \
    ,CASE WHEN B.tFactStartTime IS NOT NULL THEN '#83C75D' ELSE NULL END AS sIsStart \
    ,CASE WHEN A.sPlanDX = '预定' THEN '#83C75D' ELSE NULL END AS sPSColor /*是否预排定型*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染色%%' THEN RIGHT(A.sPlanDye,1) ELSE '' END AS sDyeingCount /*中控是否排染色*/ \
    ,CASE WHEN A.sPlanDye LIKE '%%染色%%' THEN \
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
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
    WHERE A.bUsable = 1 AND D.sEquipmentModelName LIKE '%%%s%%' AND A.bISCheck = 1\
    ORDER BY A.nRowNumber, C.sWorkRow"%(sEquipmentModelName)


# 染色机台
def DyeingEquipmentSql(sEquipmentModelName):
        return "SELECT \
        A.ID,A.sEquipmentNo,A.sEquipmentName \
        ,CONVERT(INT,NULL) AS nCardCount  \
        ,CONVERT(INT,NULL) AS nCheckCount \
        ,CONVERT(INT,NULL) AS nNoCheckCount \
        INTO #TEMP \
        FROM [pbCommonDataProductionSchedulingDyeingHDR] A  \
        WHERE A.sEquipmentModelName LIKE '%%%s%%'   \
        UPDATE #TEMP \
        SET nCardCount = B.nCardCount \
        ,nCheckCount = B.nCheckCount \
        ,nNoCheckCount = B.nNoCheckCount \
        FROM #TEMP A \
        JOIN ( \
        SELECT A.nHDRID, COUNT(*)  AS nCardCount \
        ,SUM(CASE WHEN A.bISCheck = 1 THEN 1 ELSE 0 END) AS nCheckCount\
        ,SUM(CASE WHEN A.bISCheck = 0 THEN 1 ELSE 0 END) AS nNoCheckCount \
        FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
        JOIN #TEMP B ON A.nHDRID = B.ID \
        WHERE A.bUsable = 1 \
        GROUP BY nHDRID \
        )B ON A.ID = B.nHDRID \
        SELECT *FROM #TEMP \
        DROP TABLE #TEMP"%(sEquipmentModelName)


# 根据ID获取机台信息
# 染色预排数据
def IDGetDataSql(ID):
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
    ,CASE WHEN A.sPlanDye LIKE '%%染%%' THEN CASE WHEN A.sPlanDye LIKE '%%_%%' THEN RIGHT(A.sPlanDye, LEN(A.sPlanDye) - LEN(LEFT(A.sPlanDye,CHARINDEX('_',A.sPlanDye)))) ELSE '染' END ELSE '染' END AS sDyeingCount /*中控是否排染色*/ \
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
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[ppTrackJob] B ON A.uppTrackJobGUID = B.uGUID \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON A.nHDRID = D.ID \
    WHERE A.bUsable = 1 AND D.ID =  '%s' AND A.bISCheck = 1\
    ORDER BY A.nRowNumber, C.sWorkRow"%(ID)


# 染色机台
def IDGetEquipmentSql(ID):
    return "SELECT \
        A.ID,A.sEquipmentNo,A.sEquipmentName \
        ,CONVERT(INT,NULL) AS nCardCount  \
        ,CONVERT(INT,NULL) AS nCheckCount \
        ,CONVERT(INT,NULL) AS nNoCheckCount \
        INTO #TEMP \
        FROM [pbCommonDataProductionSchedulingDyeingHDR] A  \
        WHERE A.ID = '%s'  \
        UPDATE #TEMP \
        SET nCardCount = B.nCardCount \
        ,nCheckCount = B.nCheckCount \
        ,nNoCheckCount = B.nNoCheckCount \
        FROM #TEMP A \
        JOIN ( \
        SELECT A.nHDRID, COUNT(*)  AS nCardCount \
        ,SUM(CASE WHEN A.bISCheck = 1 THEN 1 ELSE 0 END) AS nCheckCount\
        ,SUM(CASE WHEN A.bISCheck = 0 THEN 1 ELSE 0 END) AS nNoCheckCount \
        FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
        JOIN #TEMP B ON A.nHDRID = B.ID \
        WHERE A.bUsable = 1 \
        GROUP BY nHDRID \
        )B ON A.ID = B.nHDRID \
        SELECT *FROM #TEMP \
        DROP TABLE #TEMP"%(ID)


# 搜索SQL
def searchSql(inputValue):
    return "\
    DECLARE @sInputValue NVARCHAR(100) \
    SET @sInputValue = '%s' \
    SELECT TOP 7 \
    D.sCardNo,B.sEquipmentNo,D.sMaterialNo,D.sWorkingProcedureNameCurrent,A.nHDRID \
    FROM [WebDataBase].[dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
    JOIN [WebDataBase].[dbo].[pbCommonDataProductionSchedulingDyeingHDR] B ON A.nHDRID = B.ID \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob C ON A.uppTrackJobGUID = C.uGUID \
    LEFT JOIN [WebDataBase].[dbo].[pbCommonDataProductionSchedulingBase] D ON D.upsWorkFlowCardGUID = C.upsWorkFlowCardGUID \
    WHERE A.bUsable = 1 \
    AND (sMaterialNo LIKE '%%'+@sInputValue+'%%' \
    OR sCardNo LIKE '%%'+@sInputValue+'%%' \
    OR sEquipmentNo = @sInputValue) \
    ORDER BY sWorkRow " %(inputValue)


