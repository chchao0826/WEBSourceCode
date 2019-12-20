# -*-coding:utf-8-*-
# 染色预排-搜索订单号 / 工卡号 / 物料编号

# 搜索SQL
def SearchSql(inputvalue):
    return "\
    DECLARE @sInputValue NVARCHAR(100) \
    SET @sInputValue = '%s' \
    SELECT C.sCardNo,C.sMaterialNo,C.sOrderNo,D.sEquipmentNo \
    ,CASE WHEN A.bISCheck = 1 THEN '已预排' ELSE '未预排' END AS sCheckType \
    ,A.ID, D.ID AS nHDRID \
    FROM [dbo].[pbCommonDataProductionSchedulingDyeingDTL] A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob B ON A.uppTrackJobGUID = B.uGUID \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingBase] C ON C.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID \
    LEFT JOIN [dbo].[pbCommonDataProductionSchedulingDyeingHDR] D ON D.ID = A.nHDRID \
    WHERE A.bUsable = 1 AND sCardNo IS NOT NULL \
    AND( \
    C.sCardNo LIKE '%%'+@sInputValue+'%%' OR \
    C.sMaterialNo LIKE '%%'+@sInputValue+'%%' OR \
    C.sOrderNo LIKE '%%'+@sInputValue+'%%' \
    )" %(inputvalue)



