SELECT CASE WHEN C.sSalesGroupName LIKE '%营%营%' THEN CONVERT(NVARCHAR(3),C.sSalesGroupName) ELSE C.sSalesGroupName END AS sSalesGroupName 
FROM [HSWarpERP_NJYY].[dbo].psWorkFlowCard A  
JOIN [HSWarpERP_NJYY].[dbo].vwsdOrder C ON C.usdOrderLotGUID = A.usdOrderLotGUID AND DATEDIFF(MONTH,C.tCreateTime,GETDATE()) <=3
LEFT JOIN [HSWarpERP_NJYY].[dbo].pbWorkingProcedure E ON E.uGUID =  A.upbWorkingProcedureGUIDCurrent 
LEFT JOIN [HSWarpERP_NJYY].[dbo].ppTrackJob F ON E.uGUID = F.upbWorkingProcedureGUID   AND bIsCurrent=1 AND A.uGUID=F.upsWorkFlowCardGUID 
LEFT JOIN [HSWarpERP_NJYY].[dbo].ppTrackJob I WITH(NOLOCK) ON A.uGUID=I.upsWorkFlowCardGUID AND I.iOrderProcedure=F.iOrderProcedure-1 
WHERE C.sOrderType IN ('D','K') AND E.sWorkingProcedureName IS NOT NULL AND DATEDIFF(MONTH,I.tFactStartTime,GETDATE()) <=1 
GROUP BY CASE WHEN C.sSalesGroupName LIKE '%营%营%' THEN CONVERT(NVARCHAR(3),C.sSalesGroupName) ELSE C.sSalesGroupName END