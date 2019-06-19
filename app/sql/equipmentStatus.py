equipmentStatus="SELECT \
ID,sEquipmentNo,sEquipmentName,sWorkingProcedureName,bUsable,nRowNumber,bIsPMKanBan,bStatus,sColor \
FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataEquipmentStatus] A ORDER BY A.sWorkingProcedureName,A.nRowNumber DESC"