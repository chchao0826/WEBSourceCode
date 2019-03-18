JSInformation="SELECT A.sCardNo,CONVERT(NVARCHAR(30),B.sMaterialNo + '	#' +A.sMaterialLot) AS sMaterialNo \
,RIGHT(CONVERT(NVARCHAR(10),A.tCardTime,120),5) +'~'+ RIGHT(CONVERT(NVARCHAR(10),C.dReplyDate,120),5)  AS tCardTime \
,C.sSalesName,CASE WHEN C.sSalesGroupName LIKE '%营%营%' THEN CONVERT(NVARCHAR(3),C.sSalesGroupName) ELSE C.sSalesGroupName END AS sSalesGroupName \
,E.sWorkingProcedureName +'/'+ CONVERT(NVARCHAR(30),CASE WHEN F.tFactStartTime IS NOT NULL THEN '已开工' ELSE '未开工' END) AS sWorkingProcedureName \
,CASE WHEN DATEDIFF(day,A.tCardTime,C.dReplyDate) <= 4 THEN '加急' END AS sType \
,RIGHT(CONVERT(NVARCHAR(16),ISNULL(F.tFactStartTime, I.tFactStartTime),120),11) AS tFactStartTime \
,RIGHT(CONVERT(NVARCHAR(16),ISNULL(F.tFactEndTime, I.tFactEndTime),120),11) AS tFactEndTime \
,CASE WHEN DATEDIFF(DAY,C.dReplyDate,GETDATE()) <= 1 AND DATEDIFF(DAY,C.dReplyDate,GETDATE())  >=0 THEN '#FFFF00' WHEN DATEDIFF(DAY,C.dReplyDate,GETDATE()) <0 THEN '#FF0000' ELSE '#008000' END AS sTopColor \
,A.uGUID AS upsWorkFlowCardGUID \
INTO #TEMP \
FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].psWorkFlowCard A  \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].mmMaterial B ON A.ummMaterialGUID = B.uGUID \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].vwsdOrder C ON C.usdOrderLotGUID = A.usdOrderLotGUID \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].tmColor D ON D.uGUID = A.utmColorGUID \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbWorkingProcedure E ON E.uGUID =  A.upbWorkingProcedureGUIDCurrent \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob F ON E.uGUID = F.upbWorkingProcedureGUID   AND bIsCurrent=1 AND A.uGUID=F.upsWorkFlowCardGUID \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob I WITH(NOLOCK) ON A.uGUID=I.upsWorkFlowCardGUID AND I.iOrderProcedure=F.iOrderProcedure-1 \
WHERE C.sOrderType IN ('D','K') AND E.sWorkingProcedureName IS NOT NULL AND DATEDIFF(MONTH,I.tFactStartTime,GETDATE()) <=1 \
ORDER BY sSalesGroupName,A.tCardTime \
SELECT A.upsWorkFlowCardGUID,A.sCardNo,C.sWorkingProcedureName,B.upbWorkingProcedureGUID \
INTO #TEMP2 \
FROM #TEMP A \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob B ON A.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID \
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbWorkingProcedure C ON C.uGUID = B.upbWorkingProcedureGUID \
WHERE B.tFactStartTime IS NULL \
DELETE #TEMP2 \
WHERE upbWorkingProcedureGUID IN ('0BA4EFED-DB2E-4A83-81C2-A4A30119E4AD','03387401-5B36-4832-9564-A4A3011A31E6','689DED99-4BF3-4684-B263-A4A3011A5B14') \
DELETE #TEMP \
WHERE upsWorkFlowCardGUID NOT IN (SELECT DISTINCT upsWorkFlowCardGUID FROM #TEMP2) \
SELECT sSalesName,sCardNo,sMaterialNo,tCardTime,sWorkingProcedureName,sTopColor,sSalesGroupName,tFactStartTime,tFactEndTime \
FROM #TEMP \
ORDER BY sSalesGroupName,sSalesName, sWorkingProcedureName \
DROP TABLE #TEMP \
DROP TABLE #TEMP2"