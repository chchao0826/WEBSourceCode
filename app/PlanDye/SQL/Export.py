# -*- Coding:utf-8 -*-


def ExportSQL():
    return "SELECT \
    B.sEquipmentNo,E.sEquipmentPrepareNo AS sPlanEquipmentNo, \
    CASE WHEN DATEDIFF(HOUR,CASE WHEN D.tFactStartTimeCurrent IS NULL THEN D.tFactEndTimeLast ELSE D.tFactStartTimeCurrent END,GETDATE()) <= 12 THEN '12小时' \
    WHEN DATEDIFF(HOUR,CASE WHEN D.tFactStartTimeCurrent IS NULL THEN D.tFactEndTimeLast ELSE D.tFactStartTimeCurrent END,GETDATE()) <= 24 THEN '12-24小时' \
    WHEN DATEDIFF(HOUR,CASE WHEN D.tFactStartTimeCurrent IS NULL THEN D.tFactEndTimeLast ELSE D.tFactStartTimeCurrent END,GETDATE()) <= 48 THEN '24-48小时' \
    WHEN DATEDIFF(HOUR,CASE WHEN D.tFactStartTimeCurrent IS NULL THEN D.tFactEndTimeLast ELSE D.tFactStartTimeCurrent END,GETDATE()) <= 72 THEN '48-72小时' \
    WHEN DATEDIFF(HOUR,CASE WHEN D.tFactStartTimeCurrent IS NULL THEN D.tFactEndTimeLast ELSE D.tFactStartTimeCurrent END,GETDATE()) > 72 THEN '72小时以上' END AS sOverTime \
    ,D.sCustomerName,D.sCardNo,D.sMaterialNo,D.sMaterialLot \
    ,D.sColorNo,D.nFactInputQty,D.sWorkingProcedureNameLast,D.sWorkingProcedureNameCurrent,D.sWorkingProcedureNameNext,D.nDyeingTime \
    ,D.sLocation,D.sRemark,F.sOrderNo \
    FROM [WebDataBase].[dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
    JOIN [WebDataBase].[dbo].[pbCommonDataProductionSchedulingDyeingHDR] B ON A.nHDRID = B.ID \
    JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob C ON A.uppTrackJobGUID = C.uGUID \
    JOIN [WebDataBase].[dbo].[pbCommonDataProductionSchedulingBase] D ON C.upsWorkFlowCardGUID = D.upsWorkFlowCardGUID \
    JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].psWorkFlowCard E ON E.uGUID = D.upsWorkFlowCardGUID \
    JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].vwsdOrder F ON F.usdOrderLotGUID = E.usdOrderLotGUID \
    WHERE A.bUsable = 1 AND B.sEquipmentNo not like '%%E%%'\
    ORDER BY sEquipmentNo,A.nRowNumber"


    