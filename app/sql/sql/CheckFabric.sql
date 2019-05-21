SELECT B.sOrderNo,C.sMaterialNo,B.sCustomerName,D.sColorNo,B.sProductWidth
FROM [dbo].psWorkFlowCard A
LEFT JOIN [dbo].vwsdOrder B ON A.usdOrderLotGUID = B.usdOrderLotGUID
LEFT JOIN [dbo].mmMaterial C ON C.uGUID = A.ummMaterialGUID
LEFT JOIN [dbo].tmColor D ON A.utmColorGUID = D.uGUID
WHERE A.sCardNo = 'C190300841-R1'

SELECT A.sFabricNo,B.sMaterialNo,B.sMaterialName,A.sMaterialLot,A.nFactInputQty
FROM [HSWarpERP_NJYY].dbo.psWorkFlowCardInput A WITH(NOLOCK) 
JOIN [HSWarpERP_NJYY].dbo.mmMaterialFabric B WITH(NOLOCK) ON B.ummMaterialGUID=A.ummMaterialGUID 
INNER JOIN [HSWarpERP_NJYY].dbo.psWorkFlowCard C WITH(NOLOCK) ON A.upsWorkFlowCardGUID=C.uGUID 
WHERE  C.sCardNo= 'C190300841-R1'


SELECT * FROM dbo.qmInspectDefect A
WHERE A.iqmInspectCategoryID = '7' AND A.iqmInspectDefectTypeID = '22'

SELECT * FROM dbo.qmInspectCategory

SELECT A.iID,A.sDefectTypeName FROM dbo.qmInspectDefectType A