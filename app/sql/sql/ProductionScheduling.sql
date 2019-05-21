SELECT 
CASE WHEN bISRush = 1 THEN '#008000' 
WHEN DATEDIFF(HOUR,CONVERT(DATETIME,tFactEndTimeLast),GETDATE()) >72 THEN '#FF0000'
WHEN DATEDIFF(HOUR,CONVERT(DATETIME,tFactEndTimeLast),GETDATE()) >= 24 THEN '#FFFF00' END AS sBorderColor
,sCardNo,sMaterialNo,sMaterialLot,sColorNo,nFactInPutQty
,sCustomerName,sSalesName,sSalesGroupName
,nPSTime,nSETime,nPSSpeed,nSESpeed
,nPSTemp1,nPS2Temp2,nPS2Temp3_7,nPS2Temp8
,nSETemp,nSETemp2,nSETemp3_7,nSETemp8
,sProductWidth,sProductGMWT
FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[pbCommonDataProductionSchedulingBase]
WHERE bIsScheduling = 1  AND bUsable = 1 AND sType = '整理' AND sMaterialType = 'NET'

SELECT *FROM pbCommonDataProductionSchedulingHDR

--INSERT INTO pbCommonDataProductionSchedulingHDR(
--sEquipmentNo,sEquipmentName,sType,uemEquipmentGUID
--)
--SELECT 
--sEquipmentNo,sEquipmentName,'整理' AS sType,uGUID
--FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].[emEquipment]
--WHERE sEquipmentName LIKE 'LB%定型%'


--CREATE TABLE pbCommonDataProductionSchedulingHDR
--(
--ID INT PRIMARY KEY IDENTITY(1,1)
--,uemEquipmentGUID uniqueidentifier
--,sEquipmentNo NVARCHAR(20)
--,sEquipmentName NVARCHAR(20)
--,sType NVARCHAR(20)
--)

--CREATE TABLE pbCommonDataProductionSchedulingDTL
--(
--ID INT PRIMARY KEY IDENTITY(1,1)
--,sCardNo NVARCHAR(20)
--,npbCommonDataProductionSchedulingHDRID INT
--)

--DROP TABLE pbCommonDataProductionSchedulingHDR
--DROP TABLE pbCommonDataProductionSchedulingDTL
