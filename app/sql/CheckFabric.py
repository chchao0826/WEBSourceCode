# 获得卡号的详细信息
def GETMaterial(sCardNo):
    return "DECLARE @iOrderProcedure INT \
            SELECT B.sOrderNo,C.sMaterialNo,B.sCustomerName,D.sColorNo,B.sProductWidth \
            ,G.sLocation,G.upbWorkingProcedureGUID,G.tFactEndTime \
            ,ROW_NUMBER() OVER(ORDER BY G.iOrderProcedure) AS iOrderProcedure \
            INTO #TEMP \
            FROM [HSWarpERP_NJYY].[dbo].psWorkFlowCard A \
            LEFT JOIN [HSWarpERP_NJYY].[dbo].vwsdOrder B ON A.usdOrderLotGUID = B.usdOrderLotGUID \
            LEFT JOIN [HSWarpERP_NJYY].[dbo].mmMaterial C ON C.uGUID = A.ummMaterialGUID \
            LEFT JOIN [HSWarpERP_NJYY].[dbo].tmColor D ON A.utmColorGUID = D.uGUID \
            LEFT JOIN [HSWarpERP_NJYY].[dbo].ppTrackJob G ON G.upsWorkFlowCardGUID = A.uGUID \
            WHERE A.sCardNo = %s AND G.upbWorkingProcedureGUID NOT IN ('16F724BD-0CD0-402D-9802-A70200B84598','1383888F-98EE-46EF-8D9A-A69B00A428CB') \
            ORDER BY G.iOrderProcedure \
            SET @iOrderProcedure = (SELECT MIN(iOrderProcedure) FROM #TEMP WHERE  upbWorkingProcedureGUID IN('0BA4EFED-DB2E-4A83-81C2-A4A30119E4AD',    'FABE6E28-2736-45EB-9421-A8DA00EA2A53' ) AND tFactEndTime IS NULL ) \
            SELECT sOrderNo,sMaterialNo,sCustomerName,sColorNo,sProductWidth,sLocation \
            FROM #TEMP WHERE iOrderProcedure = @iOrderProcedure - 1 \
            DROP TABLE #TEMP" % (sCardNo)

# 获得卡号的配检信息
def GETFabric(sCardNo):
    return "SELECT A.sFabricNo,B.sMaterialNo,B.sMaterialName,A.sMaterialLot,A.nFactInputQty,A.nFactInputLen \
    FROM [HSWarpERP_NJYY].dbo.psWorkFlowCardInput A WITH(NOLOCK) \
    JOIN [HSWarpERP_NJYY].dbo.mmMaterialFabric B WITH(NOLOCK) ON B.ummMaterialGUID=A.ummMaterialGUID \
    INNER JOIN [HSWarpERP_NJYY].dbo.psWorkFlowCard C WITH(NOLOCK) ON A.upsWorkFlowCardGUID=C.uGUID \
    WHERE  C.sCardNo = %s" % (sCardNo)

# 遍历疵点类型
def GETDefectType():
    return "SELECT A.iID,A.sDefectTypeName FROM dbo.qmInspectDefectType A"

# 根据疵点类型查询疵点
def GETDefect(iqmInspectDefectTypeID):
    return "SELECT sDefectNameCN FROM dbo.qmInspectDefect A \
    WHERE A.iqmInspectCategoryID = '7' AND A.iqmInspectDefectTypeID = %s" % (iqmInspectDefectTypeID)

# 获得机台号
def GETEquipment():
    return "SELECT sEquipmentNo,sEquipmentName \
    FROM emEquipment \
    WHERE upbWorkCentreGUID = 'FAD3E6F4-2B72-4256-AD71-A46100B5F9A4' AND uemEquipmentModelGUID = 'B0AF3F1E-6292-4D51-8A78-A4C101788801'"
