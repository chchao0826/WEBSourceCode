# -*- coding: utf-8 -*-


# 定型达成率SQL
def DXDoneSql():
    return 'SELECT \
        B.sEquipmentName,B.sEquipmentNo,A.uppTrackJobGUID \
        ,A.tUpdateTime \
        ,CONVERT(DATETIME, NULL) AS tFactEndTime \
        INTO #TEMPTABLE \
        FROM [dbo].[pbCommonDataProductionSchedulingDTL] A \
        JOIN [dbo].[pbCommonDataProductionSchedulingHDR] B ON A.nHDRID = B.ID \
        WHERE A.bUsable = 1 \
        UPDATE #TEMPTABLE \
        SET tFactEndTime = B.tFactEndTime \
        FROM #TEMPTABLE A \
        JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pptrackJob B ON A.uppTrackJobGUID = B.uGUID \
        SELECT sEquipmentNo \
        ,SUM(CASE WHEN tFactEndTime IS NOT NULL THEN 1 ELSE 0 END) AS nFinish \
        ,SUM(CASE WHEN tFactEndTime IS NULL THEN 1 ELSE 0 END) AS nNotFinish \
        FROM #TEMPTABLE \
        GROUP BY sEquipmentNo \
        DROP TABLE #TEMPTABLE'


# 定型 三日异常 / 开动率 / 开机率
def DXTop3Sql():
    return "DECLARE @dDay DATE \
        SELECT @dDay = MAX(dDay) FROM [WebDataBase].[dbo].pbCommonDataDXChartData \
        SELECT ID,dDay,sType,sRemark,sEquipmentNo,CONVERT(NVARCHAR(10),nCount) AS nCount \
        FROM [WebDataBase].[dbo].pbCommonDataDXChartData \
        WHERE dDay = @dDay AND sEquipmentNo LIKE '%%LB%%'\
        ORDER BY sType, sEquipmentNo, sRemark ,nCount"