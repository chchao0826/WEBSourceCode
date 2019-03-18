--CREATE TABLE pbCommonDataWorkingProcedure(
--id INT primary key IDENTITY(1,1)
--,sWorkingProcedureName NVARCHAR(30)
--,nUpper DECIMAL(18,2)
--)


SELECT A.sCardNo,B.tFactStartTime,B.tFactEndTime
,CASE WHEN C.sWorkingProcedureName IN ('���Ʒ��ɫ','��Ʒ��ɫ','��ɫ','��ɫ') THEN '������'
WHEN C.sWorkingProcedureName IN ('���b') THEN '��װ'
WHEN C.sWorkingProcedureName IN ('�ɶ���') THEN '�ɶ���'
WHEN C.sWorkingProcedureName IN ('�M�׻�ԭϴ','�ʲ�','Ⱦɫ','ӆ߅','�׾�','��Ⱦ','����','ϴ��','��ɫ','�M����','��ϴ') THEN 'Ⱦɫ'
WHEN C.sWorkingProcedureName IN ('��z��','��z+�˾�','��z+����','��z+ˮϴ') THEN '��첼'
WHEN C.sWorkingProcedureName IN ('��ɫ','򞲼') THEN '�鲼'
WHEN C.sWorkingProcedureName IN ('ˮϴ') THEN 'ˮϴ'
WHEN C.sWorkingProcedureName IN ('Ԥ��','����','���','�͜��A��','��') THEN 'Ԥ��'
WHEN C.sWorkingProcedureName IN ('Óˮ','�ʲ�+չ��','չ��','Óˮ+�_��','Óˮ+չ��') THEN '��ˮչ��'
WHEN C.sWorkingProcedureName IN ('ĥë','�p��ĥë') THEN 'ĥë'
WHEN C.sWorkingProcedureName IN ('��Ʒ�U��') THEN '��Ʒ�ɿ�'
WHEN C.sWorkingProcedureName IN ('�˾�') THEN '�˾�' ELSE NULL END AS sWorkingProcedureName
,A.tCardTime
,ROW_NUMBER() OVER(PARTITION BY sCardNo ORDER BY  B.iOrderProcedure) AS nRowNumber
INTO #TEMP
FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].psWorkFlowCard A
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].ppTrackJob B ON A.uGUID = B.upsWorkFlowCardGUID
LEFT JOIN [198.168.6.253].[HSWarpERP_NJYY].[dbo].pbWorkingProcedure C ON C.uGUID = B.upbWorkingProcedureGUID
JOIN [198.168.6.253].[HSWarpERP_NJYY].dbo.vwsdOrder E WITH(NOLOCK) ON E.usdOrderLotGUID = A.usdOrderLotGUID
WHERE B.tFactEndTime IS NULL AND A.sStatus = '����' AND A.bUsable = 1 AND DATEDIFF(MONTH,tCardTime,GETDATE()) <= 6
AND E.sOrderType IN ('D','K','G','LTKJ','L','I','IL','S','J')
DELETE  #TEMP WHERE nRowNumber > 1 OR sWorkingProcedureName IS NULL
SELECT sWorkingProcedureName,COUNT(*) AS nCount
INTO #TEMP1
FROM #TEMP A
GROUP BY sWorkingProcedureName
SELECT A.sWorkingProcedureName
,CONVERT(DECIMAL(18,2),B.nCount/A.nUpper *100) AS nPre
,CONVERT(NVARCHAR(10),B.nCount) +'/' +CONVERT(NVARCHAR(10),A.nUpper) AS sTDX
FROM [dbo].[pbCommonDataWorkingProcedure] A
LEFT JOIN #TEMP1 B ON A.sWorkingProcedureName = B.sWorkingProcedureName
DROP TABLE #TEMP
DROP TABLE #TEMP1



