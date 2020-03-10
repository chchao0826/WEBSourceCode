
def SQL_PlanDX(sEquipmentNo):
    return " \
    DECLARE @sEquipmentNo NVARCHAR(100) \
    SET @sEquipmentNo = '%s'  \
    IF @sEquipmentNo != 'NoPlan' \
    BEGIN \
    SELECT B.nRowNumber,C.sEquipmentNo \
    ,ISNULL(CONVERT(NVARCHAR(19),B.tPlanTime,120),'') AS tPlanTime \
    ,CONVERT(NVARCHAR(50),NULL) AS sOverTime  \
    ,CONVERT(NVARCHAR(50),NULL) AS sCustomerName  \
    ,CONVERT(NVARCHAR(50),NULL) AS sLocation  \
    ,CONVERT(NVARCHAR(50),NULL) AS sMaterialNo  \
    ,CONVERT(NVARCHAR(50),NULL) AS sMaterialLot  \
    ,CONVERT(NVARCHAR(50),NULL) AS sCardNo  \
    ,CONVERT(NVARCHAR(50),NULL) AS sColorNo  \
    ,CONVERT(DECIMAL(18,2),NULL) AS nFactInputQty \
    ,CONVERT(NVARCHAR(50),NULL) AS sWorkingProcedureNameLast \
    ,CONVERT(NVARCHAR(50),NULL) AS sWorkingProcedureNameCurrent \
    ,CONVERT(NVARCHAR(50),NULL) AS sWorkingProcedureNameNext \
    ,CONVERT(NVARCHAR(10),NULL) AS dReplyDate \
    ,CONVERT(NVARCHAR(10),NULL) AS dDeliveryDate \
    ,CONVERT(DECIMAL(18,2),NULL) AS nTime \
    ,CONVERT(NVARCHAR(50),NULL) AS sSalesGroupName \
    ,CONVERT(NVARCHAR(100),NULL) AS sRemark \
    ,CONVERT(NVARCHAR(50),NULL) AS sLabel \
    ,CONVERT(NVARCHAR(19),'') AS tFactEndTime \
    ,CONVERT(NVARCHAR(19),'') AS tUpdateTime \
    ,CONVERT(INT,NULL) AS nPMCNumber \
    ,CONVERT(NVARCHAR(50),NULL) AS sPMCType\
    ,B.uppTrackJobGUID \
    ,CONVERT(NVARCHAR(50),NULL) AS sOrderNo  \
    INTO #TEMPTABLE \
    FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL B \
    JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingHDR C ON C.ID = B.nHDRID \
    WHERE B.bUsable = 1  AND C.sEquipmentNo = @sEquipmentNo \
    UPDATE #TEMPTABLE \
    SET sOverTime = CASE WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=12 THEN '12'  \
    WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=24 THEN '12-24'  \
    WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=72 THEN '24-72'  \
    WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) >72 THEN '72' END \
    ,sCustomerName = B.sCustomerName \
    ,sLocation = B.sLocation \
    ,sMaterialNo = B.sMaterialNo \
    ,sMaterialLot = B.sMaterialLot \
    ,sCardNo = B.sCardNo \
    ,sColorNo = B.sColorNo \
    ,nFactInputQty = B.nFactInputQty \
    ,sWorkingProcedureNameLast = B.sWorkingProcedureNameLast \
    ,sWorkingProcedureNameCurrent = B.sWorkingProcedureNameCurrent \
    ,sWorkingProcedureNameNext = B.sWorkingProcedureNameNext \
    ,dReplyDate = ISNULL(CONVERT(NVARCHAR(10),B.dReplyDate,120),'') \
    ,dDeliveryDate = ISNULL(CONVERT(NVARCHAR(10),B.dDeliveryDate,120),'') \
    ,nTime = CASE WHEN A.sType IN ('预定','水洗','水洗1','水洗2') THEN B.nPSTime  ELSE B.nSETime END \
    ,sSalesGroupName = B.sSalesGroupName \
    ,sRemark = B.sRemark \
    ,sLabel = CASE WHEN A.bIsFinish = 1 THEN 'sFinish' WHEN A.sLabel = '2' THEN 'sUrgent' WHEN B.sIsRush = '1' or A.sLabel = '1' THEN 'ERPUrgent' ELSE '#FFF' END \
    ,tFactEndTime = CONVERT(NVARCHAR(19),A.tFactEndTime,120) \
    ,tUpdateTime = CONVERT(NVARCHAR(19),A.tUpdateTime,120) \
    ,nPMCNumber = A.nRowNumber \
    ,sPMCType = A.sType \
    ,sOrderNo = B.sOrderNo \
    FROM #TEMPTABLE C  \
    JOIN [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A ON A.uppTrackJobGUID = C.uppTrackJobGUID  \
    JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo  \
    SELECT *FROM #TEMPTABLE  \
    DROP TABLE #TEMPTABLE \
    END \
    /*未预排的数据*/  \
    IF @sEquipmentNo = 'NoPlan' \
    BEGIN \
    SELECT MAX(tUpdateTime) AS tUpdateTime,sType \
    iNTO #TEMP3 \
    FROM [dbo].[pbCommonDataProductionScheduling]  \
    GROUP BY sType \
    SELECT   \
    CONVERT(NVARCHAR(10),'') AS nRowNumber  \
    ,CONVERT(NVARCHAR(20),'') AS sEquipmentNo  \
    ,CONVERT(NVARCHAR(19),'') AS tPlanTime  \
    ,CASE WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=12 THEN '12'  \
    WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=24 THEN '12-24'  \
    WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=72 THEN '24-72'  \
    WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) >72 THEN '72' END AS  sOverTime  \
    ,B.sCustomerName  \
    ,B.sLocation,B.sMaterialNo,B.sMaterialLot,B.sCardNo,B.sColorNo,B.nFactInputQty   \
    ,B.sWorkingProcedureNameLast,B.sWorkingProcedureNameCurrent,B.sWorkingProcedureNameNext   \
    ,ISNULL(CONVERT(NVARCHAR(10),B.dReplyDate,120),'') AS dReplyDate \
    ,ISNULL(CONVERT(NVARCHAR(10),B.dDeliveryDate,120),'') AS dDeliveryDate  \
    ,CASE WHEN A.sType IN ('预定','水洗','水洗1','水洗2') THEN B.nPSTime  ELSE B.nSETime END AS nTime \
    ,B.sSalesGroupName   \
    ,B.sRemark  \
    ,CASE WHEN A.bIsFinish = 1 THEN 'sFinish' WHEN A.sLabel = '2' THEN 'sUrgent' WHEN B.sIsRush = '1' or A.sLabel = '1' THEN  \'ERPUrgent' ELSE '#FFF' END AS sLabel  \
    ,ISNULL(CONVERT(NVARCHAR(19),A.tFactEndTime,120),'') AS tFactEndTime \
    ,ISNULL(CONVERT(NVARCHAR(19),A.tUpdateTime,120),'') AS tUpdateTime \
    ,A.nRowNumber AS nPMCNumber \
    ,A.sType AS sPMCType \
    ,A.uppTrackJobGUID  \
    ,B.sOrderNo \
    iNTO #TEMP  \
    FROM [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A  \
    JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo  \
    JOIN #TEMP3 C ON C.sType = A.sType AND C.tUpdateTime = A.tUpdateTime \
    ORDER BY nRowNumber \
    UPDATE #TEMP  \
    SET nRowNumber = B.nRowNumber  \
    ,sEquipmentNo = C.sEquipmentNo  \
    ,tPlanTime = ISNULL(CONVERT(NVARCHAR(19),B.tPlanTime,120),'') \
    FROM #TEMP A  \
    JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL B ON A.uppTrackJobGUID = B.uppTrackJobGUID AND B.bUsable = 1  \
    JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingHDR C ON C.ID = B.nHDRID  \
    WHERE B.bUsable = 1  \
    DELETE #TEMP WHERE ISNULL(sEquipmentNo,'') <> '' \
    SELECT *FROM #TEMP \
    DROP TABLE #TEMP \
    DROP TABLE #TEMP3 \
    END" % (sEquipmentNo)


# 搜索SQL
def SearchFunSql(sSearchValue):
    return " \
        DECLARE @sSearchValue NVARCHAR(100), @nHDRID INT, @tUpdateTime DATETIME, @sType NVARCHAR(100) \
        SET @sSearchValue = upper('%s') \
        SELECT MAX(tUpdateTime) AS tUpdateTime,uppTrackJobGUID,A.sType \
        INTO #TEMPTABLE1 \
        FROM [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo   \
        WHERE B.sOrderNo LIKE '%%'+@sSearchValue+'%%' \
        OR B.sCardNo LIKE '%%'+@sSearchValue+'%%' \
        OR B.sMaterialNo LIKE '%%'+@sSearchValue+'%%' \
        GROUP BY uppTrackJobGUID,A.sType \
        SELECT @tUpdateTime = tUpdateTime, @sType = sType FROM #TEMPTABLE1 \
        /*得到机台*/ \
        SELECT @nHDRID = nHDRID \
        FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL B  \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingHDR C ON C.ID = B.nHDRID  \
        WHERE B.uppTrackJobGUID IN (SELECT uppTrackJobGUID FROM #TEMPTABLE1) AND B.bUsable = 1 \
        /*有预排数据*/ \
        IF @nHDRID IS NOT NULL \
        BEGIN \
        SELECT B.nRowNumber,C.sEquipmentNo  \
        ,ISNULL(CONVERT(NVARCHAR(19),B.tPlanTime,120),'') AS tPlanTime \
        ,CONVERT(NVARCHAR(50),NULL) AS sOverTime \
        ,CONVERT(NVARCHAR(50),NULL) AS sCustomerName \
        ,CONVERT(NVARCHAR(50),NULL) AS sLocation \
        ,CONVERT(NVARCHAR(50),NULL) AS sMaterialNo \
        ,CONVERT(NVARCHAR(50),NULL) AS sMaterialLot \
        ,CONVERT(NVARCHAR(50),NULL) AS sCardNo \
        ,CONVERT(NVARCHAR(50),NULL) AS sColorNo \
        ,CONVERT(DECIMAL(18,2),NULL) AS nFactInputQty \
        ,CONVERT(NVARCHAR(50),NULL) AS sWorkingProcedureNameLast \
        ,CONVERT(NVARCHAR(50),NULL) AS sWorkingProcedureNameCurrent \
        ,CONVERT(NVARCHAR(50),NULL) AS sWorkingProcedureNameNext \
        ,CONVERT(NVARCHAR(10),NULL) AS dReplyDate \
        ,CONVERT(NVARCHAR(10),NULL) AS dDeliveryDate \
        ,CONVERT(DECIMAL(18,2),NULL) AS nTime \
        ,CONVERT(NVARCHAR(50),NULL) AS sSalesGroupName \
        ,CONVERT(NVARCHAR(100),NULL) AS sRemark \
        ,CONVERT(NVARCHAR(50),NULL) AS sLabel \
        ,CONVERT(NVARCHAR(19),'') AS tFactEndTime \
        ,CONVERT(NVARCHAR(19),'') AS tUpdateTime \
        ,CONVERT(INT,NULL) AS nPMCNumber \
        ,CONVERT(NVARCHAR(50),NULL) AS sPMCType\
        ,B.uppTrackJobGUID \
        ,CONVERT(NVARCHAR(50),NULL) AS sOrderNo   \
        INTO #TEMPTABLE  \
        FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL B  \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingHDR C ON C.ID = B.nHDRID \
        WHERE B.bUsable = 1  AND B.nHDRID = @nHDRID \
        UPDATE #TEMPTABLE  \
        SET sOverTime = CASE WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=12 THEN '12' \
        WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=24 THEN '12-24' \
        WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=72 THEN '24-72' \
        WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) >72 THEN '72' END \
        ,sCustomerName = B.sCustomerName \
        ,sLocation = B.sLocation \
        ,sMaterialNo = B.sMaterialNo \
        ,sMaterialLot = B.sMaterialLot \
        ,sCardNo = B.sCardNo \
        ,sColorNo = B.sColorNo \
        ,nFactInputQty = B.nFactInputQty \
        ,sWorkingProcedureNameLast = B.sWorkingProcedureNameLast \
        ,sWorkingProcedureNameCurrent = B.sWorkingProcedureNameCurrent \
        ,sWorkingProcedureNameNext = B.sWorkingProcedureNameNext \
        ,dReplyDate = ISNULL(CONVERT(NVARCHAR(10),B.dReplyDate,120),'') \
        ,dDeliveryDate = ISNULL(CONVERT(NVARCHAR(10),B.dDeliveryDate,120),'') \
        ,nTime = CASE WHEN A.sType IN ('预定','水洗','水洗1','水洗2') THEN B.nPSTime  ELSE B.nSETime END \
        ,sSalesGroupName = B.sSalesGroupName \
        ,sRemark = B.sRemark \
        ,sLabel = CASE WHEN A.bIsFinish = 1 THEN 'sFinish' WHEN A.sLabel = '2' THEN 'sUrgent' WHEN B.sIsRush = '1' or A.sLabel = '1' THEN 'ERPUrgent' ELSE '#FFF' END \
        ,tFactEndTime = CONVERT(NVARCHAR(19),A.tFactEndTime,120) \
        ,tUpdateTime = CONVERT(NVARCHAR(19),A.tUpdateTime,120) \
        ,nPMCNumber = A.nRowNumber \
        ,sPMCType = A.sType \
        ,sOrderNo = B.sOrderNo \
        FROM #TEMPTABLE C \
        JOIN [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A ON A.uppTrackJobGUID = C.uppTrackJobGUID \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo \
        SELECT *FROM #TEMPTABLE \
        DROP TABLE #TEMPTABLE \
        END \
        /*无预排数据*/ \
        IF @nHDRID IS NULL \
        BEGIN \
        SELECT MAX(tUpdateTime) AS tUpdateTime,sType \
        iNTO #TEMP3 \
        FROM [dbo].[pbCommonDataProductionScheduling]  \
        GROUP BY sType \
        SELECT \
        CONVERT(NVARCHAR(10),'') AS nRowNumber \
        ,CONVERT(NVARCHAR(20),'') AS sEquipmentNo \
        ,CONVERT(NVARCHAR(19),'') AS tPlanTime \
        ,CASE WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=12 THEN '12' \
        WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=24 THEN '12-24' \
        WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) <=72 THEN '24-72' \
        WHEN DATEDIFF(HOUR,B.tFactEndTimeLast,GETDATE()) >72 THEN '72' END AS  sOverTime \
        ,B.sCustomerName  \
        ,B.sLocation,B.sMaterialNo,B.sMaterialLot,B.sCardNo,B.sColorNo,B.nFactInputQty   \
        ,B.sWorkingProcedureNameLast,B.sWorkingProcedureNameCurrent,B.sWorkingProcedureNameNext   \
        ,ISNULL(CONVERT(NVARCHAR(10),B.dReplyDate,120),'') AS dReplyDate \
        ,ISNULL(CONVERT(NVARCHAR(10),B.dDeliveryDate,120),'') AS dDeliveryDate  \
        ,CASE WHEN A.sType IN ('预定','水洗','水洗1','水洗2') THEN B.nPSTime  ELSE B.nSETime END AS nTime \
        ,B.sSalesGroupName   \
        ,B.sRemark  \
        ,CASE WHEN A.bIsFinish = 1 THEN 'sFinish' WHEN A.sLabel = '2' THEN 'sUrgent' WHEN B.sIsRush = '1' or A.sLabel = '1' THEN  'ERPUrgent' ELSE '#FFF' END AS sLabel  \
        ,ISNULL(CONVERT(NVARCHAR(19),A.tFactEndTime,120),'') AS tFactEndTime \
        ,ISNULL(CONVERT(NVARCHAR(19),A.tUpdateTime,120),'') AS tUpdateTime \
        ,A.nRowNumber AS nPMCNumber \
        ,A.sType AS sPMCType \
        ,A.uppTrackJobGUID  \
        ,B.sOrderNo \
        iNTO #TEMP  \
        FROM [WebDataBase].[dbo].[pbCommonDataProductionScheduling] A  \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingBase B ON A.sCardNo = B.sCardNo  \
        WHERE A.sType = @sType AND A.tUpdateTime = @tUpdateTime \
        ORDER BY nRowNumber  \
        UPDATE #TEMP   \
        SET nRowNumber = B.nRowNumber   \
        ,sEquipmentNo = C.sEquipmentNo   \
        ,tPlanTime = ISNULL(CONVERT(NVARCHAR(19),B.tPlanTime,120),'')  \
        FROM #TEMP A   \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL B ON A.uppTrackJobGUID = B.uppTrackJobGUID AND B.bUsable = 1   \
        JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingHDR C ON C.ID = B.nHDRID   \
        WHERE B.bUsable = 1   \
        SELECT *FROM #TEMP  \
        DROP TABLE #TEMP  \
        DROP TABLE #TEMP3  \
        END \
        DROP TABLE #TEMPTABLE1" % (sSearchValue)
