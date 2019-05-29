def ZLKanBanSQL():
    return " \
    SELECT CONVERT(NVARCHAR(20),NULL) AS sCardNo \
    ,CONVERT(NVARCHAR(20),NULL) AS sEquipmentNo \
    ,CONVERT(INT,NULL) AS nRowNumber \
    ,CONVERT(NVARCHAR(20),NULL) AS sColorNo \
    ,CONVERT(NVARCHAR(20),NULL) AS sMaterialNo \
    ,CONVERT(NVARCHAR(20),NULL) AS sWorkingProcedureName \
    ,CONVERT(DECIMAL(18,2) ,NULL) AS nTime \
    ,CONVERT(DECIMAL(18,2) ,NULL) AS nFactTime \
    ,CONVERT(DECIMAL(18,2) ,NULL) AS nFactInPutQty \
    ,CONVERT(DECIMAL(18,2) ,NULL) AS nSpeed \
    ,CONVERT(NVARCHAR(200) ,NULL) AS nTemp \
    ,CONVERT(NVARCHAR(20) ,NULL) AS sProductWidth \
    ,CONVERT(NVARCHAR(20),NULL) AS sProductGMWT \
    ,CONVERT(uniqueidentifier ,NULL) AS uppTrackJobGUID \
    ,CONVERT(NVARCHAR(50) ,NULL) AS sCustomerName \
    INTO #TEMPTABLE \
    FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL \
    WHERE ID IS NULL \
    DECLARE @VarInt INT, @MaxInt INT \
    SET @MaxInt = 6 \
    SET @VarInt = 1 \
    WHILE (@VarInt < @MaxInt) \
    BEGIN \
    INSERT INTO #TEMPTABLE(sCardNo, sEquipmentNo, nRowNumber, uppTrackJobGUID) \
    SELECT A.sCardNo,B.sEquipmentNo,A.nRowNumber,A.uppTrackJobGUID \
    FROM [WebDataBase].[dbo].pbCommonDataProductionSchedulingDTL A \
    LEFT JOIN [WebDataBase].[dbo].pbCommonDataProductionSchedulingHDR B ON A.nHDRID = B.ID \
    WHERE ISNULL(bUsable,0) <> 1 AND A.nHDRID = @VarInt \
    ORDER BY nRowNumber \
    SET @VarInt = @VarInt + 1 \
    END \
    UPDATE #TEMPTABLE \
    SET sMaterialNo = B.sMaterialNo \
    ,sColorNo = B.sColorNo \
    ,nFactInPutQty = B.nFactInPutQty \
    ,nTemp = CASE WHEN B.sWorkingProcedureName = '预定' THEN \
        ISNULL(CONVERT(NVARCHAR(10),nPSTemp1) + '/' ,'') + \
        ISNULL(CONVERT(NVARCHAR(10),nPS2Temp2) + '/' ,'') + \
        ISNULL(CONVERT(NVARCHAR(10),nPS2Temp3_7) + '/' ,'') + \
        ISNULL(CONVERT(NVARCHAR(10),nPS2Temp8) ,'') \
        ELSE ISNULL(CONVERT(NVARCHAR(10),nSETemp) + '/' ,'') + \
        ISNULL(CONVERT(NVARCHAR(10),nSETemp2) + '/' ,'') + \
        ISNULL(CONVERT(NVARCHAR(10),nSETemp3_7) + '/' ,'') + \
        ISNULL(CONVERT(NVARCHAR(10),nSETemp8) ,'') END \
    ,nSpeed = CASE WHEN B.sWorkingProcedureName = '预定' THEN nPSSpeed ELSE nSESpeed END \
    ,nTime = CASE WHEN B.sWorkingProcedureName = '预定' THEN nPSTime ELSE nSETime END \
    ,sProductWidth = B.sProductWidth \
    ,sProductGMWT = B.sProductGMWT \
    ,sWorkingProcedureName = B.sWorkingProcedureName \
    ,sCustomerName = B.sCustomerName \
    FROM #TEMPTABLE A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataProductionSchedulingBase] B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
    SELECT A.sCardNo,A.uppTrackJobGUID \
    ,DATEDIFF(MINUTE,B.tFactStartTime,GETDATE()) AS nFactTime \
    INTO #TEMPTABLE2 \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataProductionSchedulingBase]  A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob B ON A.uppTrackJobGUID = B.uGUID \
    WHERE B.tFactEndTime IS NULL AND B.tFactStartTime IS NOT NULL \
    UPDATE #TEMPTABLE \
    SET nFactTime = B.nFactTime \
    FROM #TEMPTABLE A \
    JOIN #TEMPTABLE2 B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
	SELECT * \
	,CONVERT(INT,CONVERT(DECIMAL(18,2),nFactTime / nTime) * 100) AS nPre \
	FROM( \
	SELECT \
    sCardNo,sEquipmentNo,sColorNo,sMaterialNo,sWorkingProcedureName,nTime,nFactTime \
    ,nFactInPutQty,nSpeed,nTemp,sProductWidth,sProductGMWT,uppTrackJobGUID \
	,ROW_NUMBER() OVER(PARTITION BY sEquipmentNo ORDER BY nFactTime DESC,nRowNumber) AS nRowNumber \
    ,sCustomerName \
    FROM #TEMPTABLE \
	) B \
    WHERE B.nRowNumber <= 2 \
    ORDER BY nRowNumber \
    DROP TABLE #TEMPTABLE \
    DROP TABLE #TEMPTABLE2 \
    "