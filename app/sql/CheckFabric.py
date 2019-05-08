# 获得卡号的详细信息
def GETMaterial(sCardNo):
    return "SELECT B.sOrderNo,C.sMaterialNo,B.sCustomerName,D.sColorNo,B.sProductWidth \
        ,G.sLocation,G.upbWorkingProcedureGUID,G.tFactEndTime \
        ,ROW_NUMBER() OVER(ORDER BY G.iOrderProcedure) AS iOrderProcedure \
        ,G.uGUID AS uppTrackJobGUID \
        ,A.usdOrderLotGUID \
        ,C.uGUID AS ummMaterialGUID \
        ,D.uGUID AS utmColorGUID \
        ,A.uGUID AS upsWorkFlowCardGUID \
        INTO #TEMP \
        FROM [HSWarpERP_NJYY].[dbo].psWorkFlowCard A \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].vwsdOrder B ON A.usdOrderLotGUID = B.usdOrderLotGUID \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].mmMaterial C ON C.uGUID = A.ummMaterialGUID \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].tmColor D ON A.utmColorGUID = D.uGUID \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].ppTrackJob G ON G.upsWorkFlowCardGUID = A.uGUID \
        WHERE A.sCardNo = %s AND G.upbWorkingProcedureGUID NOT IN ('16F724BD-0CD0-402D-9802-A70200B84598','1383888F-98EE-46EF-8D9A-A69B00A428CB') \
        ORDER BY G.iOrderProcedure \
        DECLARE @iOrderProcedure INT \
        SET @iOrderProcedure = (SELECT MIN(iOrderProcedure) FROM #TEMP WHERE  upbWorkingProcedureGUID IN('0BA4EFED-DB2E-4A83-81C2-A4A30119E4AD',    'FABE6E28-2736-45EB-9421-A8DA00EA2A53' ) AND tFactEndTime IS NULL ) \
        SELECT * INTO #TEMPTABLE FROM #TEMP \
        WHERE iOrderProcedure = @iOrderProcedure \
        UPDATE #TEMPTABLE \
        SET sLocation = B.sLocation \
        FROM #TEMP A \
        JOIN (SELECT sOrderNo,sMaterialNo,sCustomerName,sColorNo,sProductWidth,sLocation,uppTrackJobGUID,usdOrderLotGUID,ummMaterialGUID,utmColorGUID \
        FROM #TEMP WHERE iOrderProcedure = @iOrderProcedure - 1 \
        )B ON A.uppTrackJobGUID= B.uppTrackJobGUID \
        SELECT A.sOrderNo,A.sMaterialNo,A.sCustomerName,A.sColorNo,A.sProductWidth,A.sLocation \
        ,A.uppTrackJobGUID,A.usdOrderLotGUID,A.ummMaterialGUID,A.utmColorGUID,A.upsWorkFlowCardGUID \
        FROM #TEMPTABLE A \
        DROP TABLE #TEMP \
        DROP TABLE #TEMPTABLE"%(sCardNo)

# 获得卡号的配检信息
def GETFabric(sCardNo):
    return "SELECT A.sFabricNo,B.sMaterialNo,B.sMaterialName,A.sMaterialLot,A.nFactInputQty,A.nFactInputLen \
    INTO #TEMP \
    FROM [HSWarpERP_NJYY].dbo.psWorkFlowCardInput A WITH(NOLOCK) \
    JOIN [HSWarpERP_NJYY].dbo.mmMaterialFabric B WITH(NOLOCK) ON B.ummMaterialGUID=A.ummMaterialGUID \
    INNER JOIN [HSWarpERP_NJYY].dbo.psWorkFlowCard C WITH(NOLOCK) ON A.upsWorkFlowCardGUID=C.uGUID \
    WHERE  C.sCardNo = %s \
    DELETE #TEMP \
    WHERE sFabricNo IN ( \
            SELECT B.sFabricNo FROM [HSWarpERP_NJYY].dbo.pbCommonDataHalfInspectHdr A \
            LEFT JOIN [HSWarpERP_NJYY].dbo.pbCommonDataHalfInspectDtl B ON A.ID = B.ipbCommonDataHalfInspectHdrID \
	    WHERE sCardNo = %s ) \
    SELECT *FROM #TEMP \
    DROP TABLE #TEMP" % (sCardNo, sCardNo)

# 遍历疵点类型
def GETDefectType():
    return "SELECT A.iID,A.sDefectTypeName FROM dbo.qmInspectDefectType A WHERE A.iID NOT IN ('25','27','28','29','30')"

# 根据疵点类型查询疵点
def GETDefect(iqmInspectDefectTypeID):
    return "SELECT sDefectNameCN FROM dbo.qmInspectDefect A \
    WHERE A.iqmInspectCategoryID = '7' AND A.iqmInspectDefectTypeID = %s" % (iqmInspectDefectTypeID)

# 获得机台号
def GETEquipment():
    return "SELECT sEquipmentNo,sEquipmentName \
    FROM emEquipment \
    WHERE upbWorkCentreGUID = 'FAD3E6F4-2B72-4256-AD71-A46100B5F9A4' AND uemEquipmentModelGUID = 'B0AF3F1E-6292-4D51-8A78-A4C101788801'"

# 获得用户名称
def GETUserName():
    f = open('D:/ERP/huansi.ini', 'r')
    value = f.read()
    value_list = value.split('\n')
    sUserName = ''
    for i in value_list:
        if (i.find('DefaultUser') == 0):
            sUserName = i.split('=')[1]
    f.close()
    return "SELECT sUserID,sUserName FROM [dbo].[smUser] WHERE sUserID = \'%s\'" %(sUserName)

# 预览查询表头信息
def ViewTitle(sCardNo):
    return "SELECT A.sCardNo,C.sColorNo,D.sMaterialNo,B.sMaterialLot,E.sCustomerName,E.sMaterialNoProduct,E.sCustomerOrderNo \
        FROM [dbo].[pbCommonDataHalfInspectHdr] A \
        JOIN [dbo].[psWorkFlowCard] B ON A.sCardNo = B.sCardNo \
        JOIN [dbo].[tmColor] C ON B.utmColorGUID = C.uGUID \
        JOIN [dbo].[mmMaterial] D ON D.uGUID = B.ummMaterialGUID \
        JOIN [dbo].[vwsdOrder] E ON E.usdOrderLotGUID = B.usdOrderLotGUID \
        WHERE A.sCardNo = %s"%(sCardNo)

# 获得每个疋号第一行的数据
def Fabric(sCardNo):
    return "SELECT B.sFabricNo,B.nLengthYard \
        ,CONVERT(DECIMAL(18,1),B.nLengthYard * 0.9144) AS nLengthMeter,nDensity,nWidth,nGMWTLeft,nGMWTInner,nGMWTRight \
        ,SUM(CASE WHEN C.nScore = 1 THEN 1 ELSE 0 END) AS One \
        ,SUM(CASE WHEN C.nScore = 2 THEN 1 ELSE 0 END) AS Two \
        ,SUM(CASE WHEN C.nScore = 3 THEN 1 ELSE 0 END) AS three \
        ,SUM(CASE WHEN C.nScore = 4 THEN 1 ELSE 0 END) AS Four \
        ,SUM(C.nScore) AS SUMScore \
        ,CONVERT(INT, B.nLengthYard*0.2) AS nMaxScore \
        ,B.sMainDefectName,B.sRemark,B.sGrade \
        ,CONVERT(NVARCHAR(20),'') AS sDefectTypeName \
        ,CONVERT(DECIMAL(18,2),0) AS nSite \
        ,CONVERT(DECIMAL(18,2),0) AS nScore \
        ,COUNT(C.nScore) AS nCount \
        ,B.ID \
        INTO #TEMP \
        FROM [dbo].[pbCommonDataHalfInspectHdr] A \
        LEFT JOIN [dbo].[pbCommonDataHalfInspectDtl] B ON A.ID = B.ipbCommonDataHalfInspectHdrID \
        LEFT JOIN [dbo].[pbCommonDataHalfInspectDefect] C ON B.ID = C.ipbCommonDataHalfInspectDtlID \
        WHERE sCardNo = %s \
        GROUP BY B.sFabricNo,B.nLengthYard,nDensity,nWidth,nGMWTLeft,nGMWTInner,nGMWTRight,B.sMainDefectName,B.sRemark,B.sGrade,B.ID \
        UPDATE #TEMP \
        SET sDefectTypeName = C.sDefectTypeName, nSite = C.nSite ,nScore = C.nScore \
        FROM #TEMP A \
        JOIN [dbo].[pbCommonDataHalfInspectDefect] C ON A.ID = C.ipbCommonDataHalfInspectDtlID \
        WHERE C.iNumber = 1 \
        SELECT *FROM #TEMP \
        DROP TABLE #TEMP \
        "%(sCardNo)

# 查询剩余的异常
def OtherDefect(sCardNo):
    return "SELECT A.sCardNo, B.sFabricNo,C.sDefectTypeName, C.nSite, C.nScore \
        FROM [dbo].[pbCommonDataHalfInspectHdr] A \
        LEFT JOIN [dbo].[pbCommonDataHalfInspectDtl] B ON A.ID = B.ipbCommonDataHalfInspectHdrID \
        JOIN [dbo].[pbCommonDataHalfInspectDefect] C ON B.ID = C.ipbCommonDataHalfInspectDtlID \
        WHERE C.iNumber != 1 AND A.sCardNo = %s \
        ORDER BY iNumber"%(sCardNo)

# 查询数据库中是否存在 新增的uppTrackJobGUID信息
def IsHaveuppTrackJobGUID(uppTrackJobGUID):
    return "SELECT 1 FROM [dbo].[pbCommonDataHalfInspectHdr] \
        WHERE uppTrackJobGUID = %s" %(uppTrackJobGUID)

# 判断是否可以新增DTL的数据
def IsInsertDtl(uppTrackJobGUID, sFabricNo):
    return "SELECT 1 FROM pbCommonDataHalfInspectHdr A \
        JOIN pbCommonDataHalfInspectDtl B ON A.ID = B.ipbCommonDataHalfInspectHdrID \
        WHERE A.uppTrackJobGUID = %s AND B.sFabricNo = %s" %(uppTrackJobGUID, sFabricNo)

# 弹出窗口是开工还是查询资料
def IsPopupBeginOrSearch(sCardNo):
    return "SELECT A.sCardNo,CONVERT(NVARCHAR(5),'已完成') AS sType,A.ID,A.uppTrackJobGUID \
        ,CONVERT(DATETIME,NULL) AS tInspectTime \
        ,CONVERT(NVARCHAR(20),NULL) AS sWorkingProcedureName \
        ,ROW_NUMBER() OVER(ORDER BY tCreateTime DESC) AS nRowNumber \
        INTO #TEMP \
        FROM pbCommonDataHalfInspectHdr A \
        WHERE sCardNo = %s \
        UPDATE #TEMP \
        SET tInspectTime = B.tInspectTime \
        FROM #TEMP A \
        JOIN (SELECT A.ID,MIN(B.tInspectTime) AS tInspectTime FROM #TEMP A \
        JOIN pbCommonDataHalfInspectDtl B ON A.ID = B.ipbCommonDataHalfInspectHdrID \
        GROUP BY A.ID \
        )B ON A.ID = B.ID \
        UPDATE #TEMP \
        SET sWorkingProcedureName = C.sWorkingProcedureName \
        FROM #TEMP A \
        JOIN ppTrackJob B ON A.uppTrackJobGUID = B.uGUID \
        JOIN pbWorkingProcedure C ON C.uGUID = B.upbWorkingProcedureGUID \
        INSERT INTO #TEMP(sType) \
        SELECT  CONVERT(NVARCHAR(5),'待开工') AS sType \
        FROM psWorkFlowCard A \
        JOIN ppTrackJob  B ON A.uGUID = B.upsWorkFlowCardGUID \
        WHERE sCardNo = %s \
        AND upbWorkingProcedureGUID IN('0BA4EFED-DB2E-4A83-81C2-A4A30119E4AD',    'FABE6E28-2736-45EB-9421-A8DA00EA2A53' ) \
        AND B.tFactEndTime IS NULL \
        SELECT sType,tInspectTime,sWorkingProcedureName,nRowNumber,sCardNo,ID \
        FROM #TEMP \
        DROP TABLE #TEMP"%(sCardNo, sCardNo)

# UpdateTable
def Updatetable(ipbCommonDataHalfInspectHdrID):
    return "SELECT A.tInspectTime,A.sFabricNo,C.sMaterialLot,A.nLengthYard \
        ,CONVERT(DECIMAL(18,2),(nLengthYard * 0.9144)) AS nLengthMeter \
        ,A.nWidth,A.nDensity,A.nGMWTLeft,A.nGMWTInner,A.nGMWTRight \
        ,A.sRemark,A.ID,ipbCommonDataHalfInspectHdrID,sGrade,sMainDefectName \
        FROM pbCommonDataHalfInspectDtl A \
        JOIN pbCommonDataHalfInspectHdr B ON A.ipbCommonDataHalfInspectHdrID = B.ID \
        JOIN psWorkFlowCard C ON B.upsWorkFlowCardGUID = C.uGUID \
        WHERE ipbCommonDataHalfInspectHdrID = %s"%(ipbCommonDataHalfInspectHdrID)

# UpdateDefect
def UpdateDefect(ipbCommonDataHalfInspectDtlID):
    return "SELECT iNumber,sDefectTypeName,nScore,nSite,ID \
        FROM pbCommonDataHalfInspectDefect \
        WHERE ipbCommonDataHalfInspectDtlID = %s" %(ipbCommonDataHalfInspectDtlID)

# 搜索卡号信息
def SearchCard(sCardNo):
    return "SELECT B.sOrderNo,C.sMaterialNo,B.sCustomerName,D.sColorNo,B.sProductWidth \
        ,G.sLocation,G.upbWorkingProcedureGUID,G.tFactEndTime \
        ,ROW_NUMBER() OVER(ORDER BY G.iOrderProcedure) AS iOrderProcedure \
        ,G.uGUID AS uppTrackJobGUID \
        ,A.usdOrderLotGUID \
        ,C.uGUID AS ummMaterialGUID \
        ,D.uGUID AS utmColorGUID \
        ,A.uGUID AS upsWorkFlowCardGUID \
        INTO #TEMP \
        FROM [HSWarpERP_NJYY].[dbo].psWorkFlowCard A \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].vwsdOrder B ON A.usdOrderLotGUID = B.usdOrderLotGUID \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].mmMaterial C ON C.uGUID = A.ummMaterialGUID \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].tmColor D ON A.utmColorGUID = D.uGUID \
        LEFT JOIN [HSWarpERP_NJYY].[dbo].ppTrackJob G ON G.upsWorkFlowCardGUID = A.uGUID \
        WHERE A.sCardNo = %s \
        AND G.upbWorkingProcedureGUID NOT IN ('16F724BD-0CD0-402D-9802-A70200B84598','1383888F-98EE-46EF-8D9A-A69B00A428CB') \
        ORDER BY G.iOrderProcedure \
        DECLARE @iOrderProcedure INT \
        SET @iOrderProcedure = (SELECT MIN(iOrderProcedure) FROM #TEMP WHERE  upbWorkingProcedureGUID IN('0BA4EFED-DB2E-4A83-81C2-A4A30119E4AD',    'FABE6E28-2736-45EB-9421-A8DA00EA2A53' )) \
        SELECT * INTO #TEMPTABLE FROM #TEMP \
        WHERE iOrderProcedure = @iOrderProcedure \
        UPDATE #TEMPTABLE \
        SET sLocation = B.sLocation \
        FROM #TEMP A \
        JOIN (SELECT sOrderNo,sMaterialNo,sCustomerName,sColorNo,sProductWidth,sLocation,uppTrackJobGUID,usdOrderLotGUID,ummMaterialGUID,utmColorGUID \
        FROM #TEMP WHERE iOrderProcedure = @iOrderProcedure - 1 \
        )B ON A.uppTrackJobGUID= B.uppTrackJobGUID \
        SELECT A.sOrderNo,A.sMaterialNo,A.sCustomerName,A.sColorNo,A.sProductWidth,A.sLocation \
        ,A.uppTrackJobGUID,A.usdOrderLotGUID,A.ummMaterialGUID,A.utmColorGUID,A.upsWorkFlowCardGUID \
        FROM #TEMPTABLE A \
        DROP TABLE #TEMP \
        DROP TABLE #TEMPTABLE"%(sCardNo)

