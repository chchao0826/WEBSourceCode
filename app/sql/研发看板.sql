USE WebDataBase
INSERT INTO [dbo].[pbCommonDataJSKanBan](sCardNo,sMaterialNo,sColorNo,tCardTime,sSalesGroupName,sWorkingProcedureName,sType)
SELECT A.sCardNo
,B.sMaterialNo + '	#' +A.sMaterialLot AS sMaterialNo
,D.sColorNo
,CONVERT(NVARCHAR(10),A.tCardTime,120) AS tCardTime,C.sSalesGroupName,E.sWorkingProcedureName
,CASE WHEN F.tFactStartTime IS NOT NULL THEN '已开工' ELSE '未开工' END AS sType
FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].psWorkFlowCard A
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].mmMaterial B ON A.ummMaterialGUID = B.uGUID
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].vwsdOrder C ON C.usdOrderLotGUID = A.usdOrderLotGUID
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].tmColor D ON D.uGUID = A.utmColorGUID
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbWorkingProcedure E ON E.uGUID = A.upbWorkingProcedureGUIDCurrent
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob F ON E.uGUID = F.upbWorkingProcedureGUID   AND bIsCurrent=1 AND A.uGUID=F.upsWorkFlowCardGUID
--前一工段
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].dbo.ppTrackJob I WITH(NOLOCK) ON A.uGUID=I.upsWorkFlowCardGUID AND I.iOrderProcedure=F.iOrderProcedure-1
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].dbo.pbWorkingProcedure J WITH(NOLOCK) ON I.upbWorkingProcedureGUID = J.uGUID
WHERE C.sOrderType IN ('D','K') AND E.sWorkingProcedureName IS NOT NULL AND DATEDIFF(MONTH,I.tFactStartTime,GETDATE()) <=1
ORDER BY sSalesGroupName,A.tCardTime