# 通过机台类型搜索机台号
def SearchEquipmentNoSQL(sEquipmentModelName):
    return "SELECT B.sEquipmentModelName \
    ,A.sEquipmentNo,sEquipmentName,A.uGUID AS uemEquipmentGUID \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].emEquipment A \
    LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].emEquipmentModel B ON A.uemEquipmentModelGUID = B.uGUID \
    WHERE b.sEquipmentModelName = '%s'  AND A.bUsable = 1 \
    "%(sEquipmentModelName)