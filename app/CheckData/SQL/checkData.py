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
        SELECT A.sCardNo,A.sMaterialNo,ISNULL(A.sFellNo,'') AS sFellNo \
        ,CONVERT(NVARCHAR(100),NULL) AS sSourceName \
        ,CONVERT(NVARCHAR(100),NULL) AS sMaterialLot \
        ,CONVERT(NVARCHAR(200),NULL) AS sMaterialProperty \
        INTO #TEMPTABLE \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> ''  AND ISNULL(bIsOK,0) != 1 \
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
        SELECT A.iIden,ISNULL(A.nPRWidth, '') AS nPRWidth,ISNULL(A.nPRYardWeight,'') AS nPRYardWeight \
        ,ISNULL('左: ' + A.sPRWeftDensityLeft,'') + ISNULL('; 中: ' + A.sPRWeftDensityIn, '') + ISNULL('; 右: '+ A.sPRWeftDensityRight, '') AS sPRWeftDensity \
        ,ISNULL('克重: ' + A.nPRGMWT + '; ','') + ISNULL('左: ' + A.nPRGMWTLeft + '; ','') + ISNULL('中: ' + A.nPRGMWTIn + '; ', '') + ISNULL('右: '+ A.nPRGMWTRight, '') AS nPRGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> ''  AND ISNULL(bIsOK,0) != 1 \
        END \
        IF @sWorkingProcedureName = 'FS' \
        BEGIN \
        SELECT A.iIden,ISNULL(A.nFSPRWidth,'') AS nFSPRWidth,ISNULL(A.nFSYardWeight,'') AS nFSYardWeight \
        ,ISNULL('克重: ' + A.nFSGMWT+ '; ','') + ISNULL('左: ' + A.nFSGMWTLeft+ '; ','') + ISNULL( '中: ' + A.nFSGMWTIn+ '; ', '') + ISNULL( '右: '+ A.nFSGMWTRight, '') AS nFSGMWT \
        ,ISNULL('左: ' + A.sFSWeftDensityLeft+ '; ','') + '中: ' + ISNULL(A.sFSWeftDensityIn+ '; ', '') + '右: '+ ISNULL(A.sFSWeftDensityRight, '') AS sFSWeftDensity \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> '' AND ISNULL(bIsOK,0) != 1 \
        END \
        IF @sWorkingProcedureName = 'SC' \
        BEGIN \
        SELECT A.iIden,ISNULL(A.sSCMachineNo,'') AS sSCMachineNo,ISNULL(A.nSCSpeed,'') AS nSCSpeed,ISNULL(A.sSCTension,'') AS sSCTension \
        ,ISNULL('1: ' + A.nSCTempIn+ '; ','') + ISNULL('2: ' + A.nSCTempIn2,'') AS nSCTemp \
        ,A.nSCPRWidth,A.nSCYardWeight \
        ,ISNULL('左: ' + A.sSCWeftDensityLeft+ '; ','') +ISNULL( '中: ' + A.sSCWeftDensityIn+ '; ', '') + ISNULL('右: '+ A.sSCWeftDensityRight, '') AS sSCWeftDensity \
        ,ISNULL('克重: ' + A.sSCGMWT+ '; ','') + ISNULL( '左: ' + A.sSCGMWTLeft+ '; ','') + ISNULL('中: ' + A.sSCGMWTIn+ '; ', '') + ISNULL('右: '+ A.sSCGMWTRight, '') AS sSCGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> '' AND ISNULL(bIsOK,0) != 1 \
        END \
        IF @sWorkingProcedureName = 'PS' \
        BEGIN \
        SELECT A.iIden,ISNULL(A.sPSMachineNo,'') AS sPSMachineNo,ISNULL(A.nPSSpeed,'') AS nPSSpeed \
        ,'1: ' + ISNULL(A.nPSTemp,'') + '; 2: ' + ISNULL(A.nPSTemp2,'') + '; 3-7: ' + ISNULL(A.nPSTemp3_7,'') + '; 8: ' + ISNULL(A.nPSTemp8,'') AS nPSTemp \
        ,ISNULL(A.sPSWidthSet,'') AS sPSWidthSet,ISNULL(A.sPSWidth,'') AS sPSWidth,ISNULL(A.nPSYardWeight,'') AS nPSYardWeight \
        ,ISNULL('左: ' + A.sPSWeftDensityLeft+ '; ','') + ISNULL('中: ' + A.sPSWeftDensityIn+ '; ', '') + ISNULL('右: '+ A.sPSWeftDensityRight+ '; ', '') AS sPSWeftDensity \
        ,ISNULL('克重: ' + A.sPSGMWT+ '; ','') + ISNULL( '左: ' + A.sPSGMWTLeft+ '; ','') + ISNULL('中: ' + A.sPSGMWTIn+ '; ', '') + ISNULL('右: '+ A.sPSGMWTRight+ '; ', '') AS sPSGMWT \
        ,sPSAidRecipe \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> '' AND ISNULL(bIsOK,0) != 1 \
        END \
        IF @sWorkingProcedureName = 'DY' \
        BEGIN \
        SELECT A.iIden,ISNULL(A.sDYMachineNo,'') AS sDYMachineNo \
		,ISNULL(A.sDYVSTempAid,'') AS sDYVSTempAid \
        ,ISNULL(A.nDYTemp,'') AS nDYTemp \
		,ISNULL(A.sDYAid,'') AS sDYAid \
        ,ISNULL(A.nDYPRWidth,'') AS nDYPRWidth \
		,ISNULL(A.nDYYardWeight,'') AS nDYYardWeight \
        ,ISNULL('左: ' + A.sDYWeftDensityLeft+ '; ','') + ISNULL('中: ' + A.sDYWeftDensityIn+ '; ', '') + ISNULL('右: '+ A.sDYWeftDensityRight+ '; ', '') AS sDYWeftDensity \
        ,+ISNULL('克重: ' + A.sDYGMWT+ '; ','') + ISNULL('左: ' + A.sDYGMWTLeft+ '; ','') + ISNULL('中: ' + A.sDYGMWTIn+ '; ', '') + ISNULL('右: '+ A.sDYGMWTRight, '') AS sDYGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A  \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> '' AND ISNULL(bIsOK,0) != 1 \
        END \
        IF @sWorkingProcedureName = 'SE' \
        BEGIN \
        SELECT A.iIden,ISNULL(A.sSEMachineNo,'') AS sSEMachineNo,ISNULL(A.nSESpeed,'') AS nSESpeed \
        ,'1: ' + ISNULL(A.nSETemp,'') + '; 2: ' + ISNULL(A.nSETemp2,'') + '; 3-7: ' + ISNULL(A.nSETemp3_7,'') + '; 8: ' + ISNULL(A.nSETemp8,'') AS nSETemp \
        ,ISNULL(A.sSEAidRecipe,'') AS sSEAidRecipe,ISNULL(A.sSEWidthSet,'') AS sSEWidthSet \
        ,ISNULL(A.sSEPRWidth,'') AS sSEPRWidth,ISNULL(A.nSEYardWeight,'') AS nSEYardWeight \
        ,ISNULL('左: ' + A.sSEWeftDensityLeft+ '; ','') + ISNULL('中: ' + A.sSEWeftDensityIn+ '; ', '') + ISNULL('右: '+ A.sSEWeftDensityRight+ '; ', '') AS sSEWeftDensity \
        ,ISNULL('克重: ' + sSEGMWT+ '; ','') + ISNULL('左: ' + A.sSEGMWTLeft+ '; ','') + ISNULL('中: ' + A.sSEGMWTIn+ '; ', '') + ISNULL('右: '+ A.sSEGMWTRight+ '; ', '') AS sSEGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE (sCardNo IN (@sMaterialNo1, @sMaterialNo2, @sMaterialNo3, @sMaterialNo4, @sMaterialNo5, @sMaterialNo6, @sMaterialNo7, @sMaterialNo8, @sMaterialNo9) ) AND ISNULL(sMaterialNo,'') <> ''  AND ISNULL(sCardNo,'') <> '' AND ISNULL(bIsOK,0) != 1 \
        END"% (sWorkingProcedureName, sMaterialNo1, sMaterialNo2, sMaterialNo3, sMaterialNo4, sMaterialNo5, sMaterialNo6, sMaterialNo7, sMaterialNo8, sMaterialNo9)



