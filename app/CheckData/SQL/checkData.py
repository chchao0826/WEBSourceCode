# 获得卡号的研发数据
def JSSearchDataSQL(sWorkingProcedureName, sMaterialNo1, sMaterialNo2, sMaterialNo3, sMaterialNo4, sMaterialNo5, sMaterialNo6, sMaterialNo7, sMaterialNo8, sMaterialNo9):
    return "DECLARE @sWorkingProcedureName NVARCHAR(100) \
        ,@sMaterialNo1 NVARCHAR(200) \
        ,@sMaterialNo2 NVARCHAR(200) \
        ,@sMaterialNo3 NVARCHAR(200) \
        ,@sMaterialNo4 NVARCHAR(200) \
        ,@sMaterialNo5 NVARCHAR(200) \
        ,@sMaterialNo6 NVARCHAR(200) \
        ,@sMaterialNo7 NVARCHAR(200) \
        ,@sMaterialNo8 NVARCHAR(200) \
        ,@sMaterialNo9 NVARCHAR(200) \
        SET @sWorkingProcedureName = '%s' \
        SET @sMaterialNo1 = '%s' \
        SET @sMaterialNo2 = '%s' \
        SET @sMaterialNo3 = '%s' \
        SET @sMaterialNo4 = '%s' \
        SET @sMaterialNo5 = '%s' \
        SET @sMaterialNo6 = '%s' \
        SET @sMaterialNo7 = '%s' \
        SET @sMaterialNo8 = '%s' \
        SET @sMaterialNo9 = '%s' \
        IF @sWorkingProcedureName = 'title' \
        BEGIN \
        SELECT A.sCardNo,A.sMaterialNo,A.sFellNo \
        ,CONVERT(NVARCHAR(100),NULL) AS sSourceName \
        ,CONVERT(NVARCHAR(100),NULL) AS sMaterialLot \
        ,CONVERT(NVARCHAR(200),NULL) AS sMaterialProperty \
        INTO #TEMPTABLE \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND bIsOk = 1 \
        UPDATE #TEMPTABLE \
        SET sMaterialLot = B.sMaterialLot \
        ,sSourceName = E.sProviderName \
        ,sMaterialProperty  =C.sMaterialProperty \
        FROM #TEMPTABLE A \
        LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].psWorkFlowCard B ON A.sCardNo = B.sCardNo \
        LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].mmMaterial C ON C.uGUID = B.ummMaterialGUID \
        LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].tmBOMHdr D ON D.ummMaterialGUID = C.uGUID AND D.iOrderNo = B.sMaterialLot \
        LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbProvider E ON E.uGUID = D.upbProviderGUID \
        SELECT *FROM #TEMPTABLE \
        DROP TABLE #TEMPTABLE \
        END \
        IF @sWorkingProcedureName = 'PR' \
        BEGIN \
        SELECT A.iIden,A.nPRWidth,A.nPRYardWeight \
        ,'左: ' + ISNULL(A.sPRWeftDensityLeft,'') + '中: ' + ISNULL(A.sPRWeftDensityIn, '') + '右: '+ ISNULL(A.sPRWeftDensityRight, '') AS sPRWeftDensity \
        ,'左: ' + ISNULL(A.nPRGMWTLeft,'') + '中: ' + ISNULL(A.nPRGMWTIn, '') + '右: '+ ISNULL(A.nPRGMWTRight, '') AS nPRGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND sOKMan = 'OK' AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = 'FS' \
        BEGIN \
        SELECT A.iIden,A.nFSPRWidth,A.nFSYardWeight \
        ,'左: ' + ISNULL(A.nFSGMWTLeft,'') + '中: ' + ISNULL(A.nFSGMWTIn, '') + '右: '+ ISNULL(A.nFSGMWTRight, '') AS nFSGMWT \
        ,'左: ' + ISNULL(A.sFSWeftDensityLeft,'') + '中: ' + ISNULL(A.sFSWeftDensityIn, '') + '右: '+ ISNULL(A.sFSWeftDensityRight, '') AS sFSWeftDensity \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = 'SC' \
        BEGIN \
        SELECT A.iIden,A.sSCMachineNo,A.nSCSpeed,A.sSCTension \
        ,'1: ' + ISNULL(A.nSCTempIn,'') + '; 2: ' + ISNULL(A.nSCTempIn2,'') AS nSCTemp \
        ,A.nSCPRWidth,A.nSCYardWeight \
        ,'左: ' + ISNULL(A.sSCWeftDensityLeft,'') + '中: ' + ISNULL(A.sSCWeftDensityIn, '') + '右: '+ ISNULL(A.sSCWeftDensityRight, '') AS sSCWeftDensity \
        ,A.sSCGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = 'PS' \
        BEGIN \
        SELECT A.iIden,A.sPSMachineNo,A.nPSSpeed \
        ,'1:' + ISNULL(A.nPSTemp,'') + '; 2:' + ISNULL(A.nPSTemp2,'') + '; 3-7:' + ISNULL(A.nPSTemp3_7,'') + '; 8:' + ISNULL(A.nPSTemp8,'') AS nPSTemp \
        ,A.sPSWidthSet,A.sPSWidth,A.nPSYardWeight \
        ,'左: ' + ISNULL(A.sPSWeftDensityLeft,'') + '中: ' + ISNULL(A.sPSWeftDensityIn, '') + '右: '+ ISNULL(A.sPSWeftDensityRight, '') AS sPSWeftDensity \
        ,A.sPSGMWT \
        ,'左: ' + ISNULL(A.sPSGMWTLeft,'') + '中: ' + ISNULL(A.sPSGMWTIn, '') + '右: '+ ISNULL(A.sPSGMWTRight, '') AS sPSGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = 'DY' \
        BEGIN \
        SELECT A.iIden,A.sDYMachineNo,A.sDYVSTempAid,A.nDYTemp,A.sDYAid,A.nDYPRWidth,A.nDYYardWeight,A.sDYGMWT \
        ,'左: ' + ISNULL(A.sDYWeftDensityLeft,'') + '中: ' + ISNULL(A.sDYWeftDensityIn, '') + '右: '+ ISNULL(A.sDYWeftDensityRight, '') AS sDYWeftDensity \
        ,'左: ' + ISNULL(A.sDYGMWTLeft,'') + '中: ' + ISNULL(A.sDYGMWTIn, '') + '右: '+ ISNULL(A.sDYGMWTRight, '') AS sDYGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A  \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = 'SE' \
        BEGIN \
        SELECT A.iIden,A.sSEMachineNo,A.nSESpeed \
        ,'1:' + ISNULL(A.nSETemp,'') + '; 2:' + ISNULL(A.nSETemp2,'') + '; 3-7:' + ISNULL(A.nSETemp3_7,'') + '; 8:' + ISNULL(A.nSETemp8,'') AS nSETemp \
        ,A.sSEAidRecipe,A.sSEWidthSet,A.sSEPRWidth,A.nSEYardWeight \
        ,'左: ' + ISNULL(A.sSEWeftDensityLeft,'') + '中: ' + ISNULL(A.sSEWeftDensityIn, '') + '右: '+ ISNULL(A.sSEWeftDensityRight, '') AS sSEWeftDensity \
        ,'克重: ' + ISNULL(sSEGMWT,'') + '左: ' + ISNULL(A.sSEGMWTLeft,'') + '中: ' + ISNULL(A.sSEGMWTIn, '') + '右: '+ ISNULL(A.sSEGMWTRight, '') AS sSEGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) AND bIsOk = 1 \
        END" % (sWorkingProcedureName, sMaterialNo1, sMaterialNo2, sMaterialNo3, sMaterialNo4, sMaterialNo5, sMaterialNo6, sMaterialNo7, sMaterialNo8, sMaterialNo9)



