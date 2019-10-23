# 获得卡号的研发数据
def JSSearchDataSQL(sWorkingProcedureName, sMaterialNo):
    return "\
        DECLARE @sWorkingProcedureName NVARCHAR(100), @sMaterialNo NVARCHAR(200) \
        SET @sWorkingProcedureName = '%s' \
        SET @sMaterialNo = '%s' \
        IF @sWorkingProcedureName = '主表' \
        BEGIN \
        SELECT A.sCardNo,A.sMaterialNo,A.sFellNo \
        ,CONVERT(NVARCHAR(100),NULL) AS sSourceName \
        ,CONVERT(NVARCHAR(100),NULL) AS sMaterialLot \
        ,CONVERT(NVARCHAR(200),NULL) AS sMaterialProperty \
        INTO #TEMPTABLE \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo = @sMaterialNo AND bIsOk = 1 \
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
        IF @sWorkingProcedureName = '配检布' \
        BEGIN \
        SELECT A.iIden,A.nPRWidth,A.nPRYardWeight \
        ,'左: ' + ISNULL(A.nPRGMWTLeft,'') + '中: ' + ISNULL(A.nPRGMWTIn, '') + '右: '+ ISNULL(A.nPRGMWTRight, '') AS nPRGMWT \
        ,'左: ' + ISNULL(A.sPRWeftDensityLeft,'') + '中: ' + ISNULL(A.sPRWeftDensityIn, '') + '右: '+ ISNULL(A.sPRWeftDensityRight, '') AS sPRWeftDensity \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo = @sMaterialNo AND sOKMan = 'OK' AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = '沸缩' \
        BEGIN \
        SELECT A.iIden,A.nFSPRWidth,A.nFSYardWeight \
        ,'左: ' + ISNULL(A.nFSGMWTLeft,'') + '中: ' + ISNULL(A.nFSGMWTIn, '') + '右: '+ ISNULL(A.nFSGMWTRight, '') AS nFSGMWT \
        ,'左: ' + ISNULL(A.sFSWeftDensityLeft,'') + '中: ' + ISNULL(A.sFSWeftDensityIn, '') + '右: '+ ISNULL(A.sFSWeftDensityRight, '') AS sFSWeftDensity \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo = @sMaterialNo AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = '精炼' \
        BEGIN \
        SELECT A.iIden,A.sSCMachineNo,A.nSCSpeed,A.sSCTension,A.nSCPRWidth,A.sSCGMWT,A.nSCYardWeight \
        ,'1: ' + ISNULL(A.nSCTempIn,'') + '2: ' + ISNULL(A.nSCTempIn2,'') AS nSCTemp \
        ,'左: ' + ISNULL(A.sSCWeftDensityLeft,'') + '中: ' + ISNULL(A.sSCWeftDensityIn, '') + '右: '+ ISNULL(A.sSCWeftDensityRight, '') AS sSCWeftDensity \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo = @sMaterialNo AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = '预定' \
        BEGIN \
        SELECT A.iIden,A.sPSMachineNo,A.nPSSpeed,A.sPSWidth,A.sPSWidthSet,A.nPSYardWeight,A.sPSGMWT \
        ,'1:' + ISNULL(A.nPSTemp,'') + '2:' + ISNULL(A.nPSTemp2,'') + '3-7:' + ISNULL(A.nPSTemp3_7,'') + '8:' + ISNULL(A.nPSTemp8,'') AS nPSTemp \
        ,'左: ' + ISNULL(A.sPSWeftDensityLeft,'') + '中: ' + ISNULL(A.sPSWeftDensityIn, '') + '右: '+ ISNULL(A.sPSWeftDensityRight, '') AS sPSWeftDensity \
        ,'左: ' + ISNULL(A.sPSGMWTLeft,'') + '中: ' + ISNULL(A.sPSGMWTIn, '') + '右: '+ ISNULL(A.sPSGMWTRight, '') AS sPSGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo = @sMaterialNo AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = '染色' \
        BEGIN \
        SELECT A.iIden,A.sDYMachineNo,A.nDYTemp,A.sDYVSTempAid,A.sDYAid,A.nDYPRWidth,A.sDYGMWT,A.nDYYardWeight \
        ,'左: ' + ISNULL(A.sDYWeftDensityLeft,'') + '中: ' + ISNULL(A.sDYWeftDensityIn, '') + '右: '+ ISNULL(A.sDYWeftDensityRight, '') AS sDYWeftDensity \
        ,'左: ' + ISNULL(A.sDYGMWTLeft,'') + '中: ' + ISNULL(A.sDYGMWTIn, '') + '右: '+ ISNULL(A.sDYGMWTRight, '') AS sDYGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A  \
        WHERE sMaterialNo = @sMaterialNo AND bIsOk = 1 \
        END \
        IF @sWorkingProcedureName = '成定' \
        BEGIN \
        SELECT A.iIden,A.sSEMachineNo,A.nSESpeed,A.sSEAidRecipe,A.sSEWidthSet,A.sSEPRWidth,A.nSEYardWeight \
        ,'1:' + ISNULL(A.nSETemp,'') + '2:' + ISNULL(A.nSETemp2,'') + '3-7:' + ISNULL(A.nSETemp3_7,'') + '8:' + ISNULL(A.nSETemp8,'') AS nSETemp \
        ,'左: ' + ISNULL(A.sSEWeftDensityLeft,'') + '中: ' + ISNULL(A.sSEWeftDensityIn, '') + '右: '+ ISNULL(A.sSEWeftDensityRight, '') AS sSEWeftDensity \
        ,'克重: ' + ISNULL(sSEGMWT,'') + '左: ' + ISNULL(A.sSEGMWTLeft,'') + '中: ' + ISNULL(A.sSEGMWTIn, '') + '右: '+ ISNULL(A.sSEGMWTRight, '') AS sSEGMWT \
        FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbCommonTestFabricTrackHdr A \
        WHERE sMaterialNo = @sMaterialNo AND bIsOk = 1 \
        END" % (sWorkingProcedureName, sMaterialNo)



