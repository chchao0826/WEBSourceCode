ExecUpdateSql = "\
SELECT A.sCardNo,G.sMaterialTypeName,C.sMaterialNo,A.sMaterialLot,H.sColorCatena \
,H.sColorNo,A.nFactInputQty,A.nPlanOutputQty,A.sSourceName \
,F.sWorkingProcedureName,B.iOrderProcedure \
,D.sWorkingProcedureName AS sWorkingProcedureNameCurrent \
,J.sWorkingProcedureName AS sWorkingProcedureNameLast \
,M.sWorkingProcedureName AS sWorkingProcedureNameNext \
,I.tFactEndTime AS tFactEndTimeLast \
,CONVERT(NVARCHAR(200),NULL) AS sCustomerName \
,CONVERT(NVARCHAR(200),NULL) AS sSalesName \
,CONVERT(DECIMAL(18,1),NULL) AS sProductWidth \
,CONVERT(DECIMAL(18,1),NULL) AS sProductGMWT \
,CONVERT(DECIMAL(18,2),NULL) AS nPSSpeed \
,CONVERT(DECIMAL(18,2),NULL) AS nSESpeed \
,CONVERT(NVARCHAR(200),NULL) AS sSalesGroupName \
,CONVERT(NVARCHAR(200),NULL) AS sNotDoneProcedure \
,CONVERT(NVARCHAR(200),NULL) AS sMaterialType \
,CONVERT(DECIMAL(18,2), NULL) AS nTJTime \
,CONVERT(DECIMAL(18,2), NULL) AS nPSTime \
,CONVERT(DECIMAL(18,2), NULL) AS nDyeingTime \
,CONVERT(DECIMAL(18,2), NULL) AS nSETime \
,CONVERT(BIT, NULL) AS sIsRush \
,CONVERT(DECIMAL(18,2), NULL) AS nPSTemp1 \
,CONVERT(DECIMAL(18,2), NULL) AS nPS2Temp2 \
,CONVERT(DECIMAL(18,2), NULL) AS nPS2Temp3_7 \
,CONVERT(DECIMAL(18,2), NULL) AS nPS2Temp8 \
,CONVERT(DECIMAL(18,2), NULL) AS nSETemp \
,CONVERT(DECIMAL(18,2), NULL) AS nSETemp2 \
,CONVERT(DECIMAL(18,2), NULL) AS nSETemp3_7 \
,CONVERT(DECIMAL(18,2), NULL) AS nSETemp8 \
,I.sLocation \
,B.uGUID AS uppTrackJobGUID \
,A.uGUID AS upsWorkFlowCardGUID \
,A.usdOrderLotGUID \
,CASE WHEN H.sColorCatena = 'O' THEN CASE WHEN H.sColorLevel = '1' THEN '#FFA500' WHEN H.sColorLevel = '2' THEN '#EE9A00'  \
				WHEN H.sColorLevel = '3' THEN '#CD8500' WHEN H.sColorLevel = '4' THEN '#FF7F00'  \
				WHEN H.sColorLevel = '5' THEN '#CD6600' WHEN H.sColorLevel > '5' THEN '#FFA500' END \
WHEN H.sColorCatena = 'K' THEN CASE WHEN H.sColorLevel = '1' THEN '#778899' WHEN H.sColorLevel = '2' THEN '#778899' \
				WHEN H.sColorLevel = '3' THEN '#696969' WHEN H.sColorLevel = '4' THEN '#2F4F4F'  \
				WHEN H.sColorLevel = '5' THEN '#000000' WHEN H.sColorLevel > '5' THEN '#000000' END \
WHEN H.sColorCatena = 'W' THEN CASE WHEN H.sColorLevel = '1' THEN '#FFFFFF' WHEN H.sColorLevel = '2' THEN '#EEEEEE' \
				WHEN H.sColorLevel = '3' THEN '#DDDDD' WHEN H.sColorLevel = '4' THEN '#CCCCCC'  \
				WHEN H.sColorLevel = '5' THEN '#BBBBBB' WHEN H.sColorLevel > '5' THEN '#AAAAA' END \
WHEN H.sColorCatena = 'P' THEN CASE WHEN H.sColorLevel = '1' THEN '#FFFFF0'  \
				WHEN H.sColorLevel = '2' THEN '#EEEEE0' WHEN H.sColorLevel = '3' THEN '#CDCDC1' \
				WHEN H.sColorLevel = '4' THEN '#8B8B83' WHEN H.sColorLevel = '5' THEN '#8B8989' END \
WHEN H.sColorCatena = 'G' THEN CASE WHEN H.sColorLevel = '1' THEN '#9AFF9A'  \
				WHEN H.sColorLevel = '2' THEN '#90EE90' WHEN H.sColorLevel = '3' THEN '#00FF00' \
				WHEN H.sColorLevel = '4' THEN '#00EE00' WHEN H.sColorLevel = '5' THEN '#008B00' WHEN H.sColorLevel > '5' THEN  '#7FFF00' END \
WHEN H.sColorCatena = 'R' THEN CASE WHEN H.sColorLevel = '1' THEN '#FA8072' \
				WHEN H.sColorLevel = '2' THEN  	'#FF0000' WHEN H.sColorLevel = '3' THEN '#EE0000' \
				WHEN H.sColorLevel = '4' THEN '#CD0000' WHEN H.sColorLevel = '5' THEN '#8B0000' END \
WHEN H.sColorCatena = 'C' THEN CASE WHEN H.sColorLevel = '1' THEN '#FFA07A'  \
				WHEN H.sColorLevel = '2' THEN  	'#EE9572' WHEN H.sColorLevel = '3' THEN '#FF8C69' \
				WHEN H.sColorLevel = '4' THEN '#EE8262' WHEN H.sColorLevel = '5' THEN '#CD7054' END \
WHEN H.sColorCatena = 'B' THEN CASE WHEN H.sColorLevel = '1' THEN '#63B8FF'  \
				WHEN H.sColorLevel = '2' THEN  	'#5CACEE' WHEN H.sColorLevel = '3' THEN '#1E90FF' \
				WHEN H.sColorLevel = '4' THEN '#1C86EE' WHEN H.sColorLevel = '5' THEN '#0000FF' WHEN H.sColorLevel > '5' THEN  '#00BFFF' END \
WHEN H.sColorCatena = 'Y' THEN CASE WHEN H.sColorLevel = '1' THEN '#FFF68F'  \
				WHEN H.sColorLevel = '2' THEN  	'#EEE685' WHEN H.sColorLevel = '3' THEN '#FFFF00' \
				WHEN H.sColorLevel = '4' THEN '#EEEE00' WHEN H.sColorLevel = '5' THEN '#CDCD00' WHEN H.sColorLevel > '5' THEN '#FFFa0F' END \
WHEN H.sColorCatena = 'V' THEN CASE WHEN H.sColorLevel = '1' THEN '#DDA0DD'  \
				WHEN H.sColorLevel = '2' THEN  	'#EE82EE' WHEN H.sColorLevel = '3' THEN '#DA70D6' \
				WHEN H.sColorLevel = '4' THEN '#BA55D3' WHEN H.sColorLevel = '5' THEN '#9932CC' WHEN H.sColorLevel > '5' THEN '#FF00FF' END \
WHEN H.sColorNo = 'CR' THEN '#FFFFFF' END  \
AS sColorBorder \
,A.sRemark \
,CONVERT(DATETIME,NULL) AS dDeliveryDate \
,CONVERT(DATETIME,NULL) AS dReplyDate \
INTO #TEMPTABLE \
FROM [dbo].psWorkFlowCard A \
LEFT JOIN [dbo].ppTrackJob B ON A.uGUID = B.upsWorkFlowCardGUID \
LEFT JOIN [dbo].mmMaterial C ON C.uGUID = A.ummMaterialGUID \
LEFT JOIN [dbo].pbWorkingProcedure D ON D.uGUID = A.upbWorkingProcedureGUIDCurrent \
LEFT JOIN [dbo].ppTrackJob E ON E.upbWorkingProcedureGUID = D.uGUID AND E.upsWorkFlowCardGUID = A.uGUID AND E.bIsCurrent = 1 \
LEFT JOIN [dbo].pbWorkingProcedure F ON F.uGUID = B.upbWorkingProcedureGUID \
LEFT JOIN [dbo].mmMaterialType G ON G.uGUID = C.ummMaterialTypeGUID \
LEFT JOIN [dbo].tmColor H ON H.uGUID = A.utmColorGUID \
LEFT JOIN dbo.ppTrackJob I WITH(NOLOCK) ON A.uGUID=I.upsWorkFlowCardGUID AND I.iOrderProcedure=E.iOrderProcedure - 1 \
LEFT JOIN HSWarpERP_NJYY.dbo.pbWorkingProcedure J WITH(NOLOCK) ON I.upbWorkingProcedureGUID = J.uGUID \
LEFT JOIN dbo.ppTrackJob K WITH(NOLOCK) ON A.uGUID=K.upsWorkFlowCardGUID AND K.iOrderProcedure=E.iOrderProcedure + 1 \
LEFT JOIN HSWarpERP_NJYY.dbo.pbWorkingProcedure M WITH(NOLOCK) ON K.upbWorkingProcedureGUID = M.uGUID \
WHERE B.upbWorkingProcedureGUID IN ( \
'A5A47A57-0EAF-45A5-BE73-A4A3011295EA','7EDB87B5-5B26-4438-BBED-A67000E33DAF' \
,'759AE3A8-8EDA-45A9-B728-A674014AE987','D9E8E943-C5F5-4D37-BC06-A68400C1FE95' \
,'D3A0B0CB-8430-4646-B758-A4A3011988B4','9E812C90-C0CA-472B-B579-A4A30118C6CB' \
,'8FF73E9D-E9BD-4462-864F-A67401499644','E0B0446A-8D00-45DE-BEAB-A67A01218C3E')  \
AND B.tFactEndTime IS NULL AND   A.sStatus NOT IN ('完成','中止') AND A.bUsable = 1 \
AND DATEDIFF(MONTH,tCardTime,GETDATE()) < 6 \
UPDATE #TEMPTABLE \
SET sProductWidth = B.sProductWidth \
,sProductGMWT = B.sProductGMWT \
,nPSSpeed = B.nPSSpeed \
,nSESpeed = B.nSESpeed \
,nPSTemp1 = B.nPSTemp1 \
,nPS2Temp2 = B.nPS2Temp2 \
,nPS2Temp3_7 = B.nPS2Temp3_7 \
,nPS2Temp8 = B.nPS2Temp8 \
,nSETemp = B.nSETemp \
,nSETemp2 = B.nSETemp2 \
,nSETemp3_7 = B.nSETemp3_7 \
,nSETemp8 = B.nSETemp8 \
FROM #TEMPTABLE A \
JOIN ( \
SELECT D.usdOrderLotGUID,E.nPSSpeed,E.nSESpeed,E.nPSTemp1,E.nPS2Temp2,E.nPS2Temp3_7,E.nPS2Temp8,E.nSETemp,E.nSETemp2,E.nSETemp3_7,E.nSETemp8 \
,CASE WHEN ((sProductWidth LIKE '%”%' OR sProductWidth LIKE '%''''%' OR sProductWidth LIKE '%\"%'  OR sProductWidth LIKE '%'' ''%') \
AND (sProductWidth NOT LIKE '%CM%' OR sProductWidth NOT LIKE '%%cm%')) THEN CONVERT(DECIMAL(18,2), \
		CASE   \
            WHEN TRY_CAST(left(sProductWidth,3) AS int) is  not null then left(sProductWidth,3) \
            WHEN TRY_CAST(left(sProductWidth,2) AS int) is  not null then left(sProductWidth,2)  \
	  ELSE 160 \
	  END)*2.54  ELSE CONVERT(DECIMAL(18,2), \
		CASE WHEN TRY_CAST(left(sProductWidth,3) AS int) is  not null then left(sProductWidth,3) \
				  WHEN TRY_CAST(left(sProductWidth,2) AS int) is  not null then left(sProductWidth,2)  \
	  ELSE 160 \
	  END) END \
 AS sProductWidth, \
CONVERT(DECIMAL(18,2), \
  CASE  \
        WHEN TRY_CAST(left(sProductGMWT,3) AS int) is  not null then left(sProductGMWT,3) \
        WHEN TRY_CAST(left(sProductGMWT,2) AS int) is  not null then left(sProductGMWT,2)  \
		ELSE 150 \
	  END) \
 AS sProductGMWT   \
FROM vwsdOrder D  \
LEFT JOIN pbCommonTestFabricTrackHdr E ON E.sMaterialNo=D.sMaterialNoProduct OR E.sMaterialNo=D.sMaterialNo AND( E.nPSSpeed IS NOT  NULL OR E.nPSSpeed1 IS NOT NULL OR E.nSESpeed IS NOT NULL) AND E.bIsok = 1 \
) B ON A.usdOrderLotGUID = B.usdOrderLotGUID \
UPDATE #TEMPTABLE \
SET nPSSpeed=IIF(ISNULL(nPSSpeed,0)=0.0,20.0,nPSSpeed) \
    ,nSESpeed=IIF(ISNULL(nSESpeed,0)=0.0,20.0,nSESpeed) \
,sProductWidth=CASE WHEN IIF(ISNULL(sProductWidth,0.0)=0.0,160.0,sProductWidth) >=300 THEN 160 ELSE IIF(ISNULL(sProductWidth,0)=0,160.0,sProductWidth) END \
,sProductGMWT=CASE WHEN IIF(ISNULL(sProductGMWT,0.0)=0.0,150.0,sProductGMWT) = 1 THEN 150 ELSE IIF(ISNULL(sProductGMWT,0)=0,150.0,sProductGMWT) END  \
FROM #TEMPTABLE A \
SELECT A.usdOrderLotGUID,A.uppTrackJobGUID,A.sCardNo,A.sMaterialNo,sMaterialTypeName,A.sColorNo,A.sColorCatena,A.sWorkingProcedureNameCurrent \
,C.sWorkingProcedureName,B.iOrderProcedure,A.nFactInputQty,A.nPlanOutputQty,A.sLocation \
,sProductWidth \
,sProductGMWT \
,nPSSpeed \
,nSESpeed \
,CONVERT(NVARCHAR(20), NULL) AS sType \
,CONVERT(DECIMAL(18,2), NULL) AS nTJTime \
,CONVERT(DECIMAL(18,2), NULL) AS nPSTime \
,CONVERT(DECIMAL(18,2), NULL) AS nSETime \
,CONVERT(DECIMAL(18,2), NULL) AS nDyeingTime \
INTO #TEMP \
FROM #TEMPTABLE A \
LEFT JOIN [dbo].ppTrackJob B ON A.upsWorkFlowCardGUID = B.upsWorkFlowCardGUID AND B.iOrderProcedure< A.iOrderProcedure AND B.tFactEndTime IS NULL \
LEFT JOIN [dbo].pbWorkingProcedure C ON C.uGUID = B.upbWorkingProcedureGUID \
ORDER BY A.sCardNo,A.sWorkingProcedureName,B.iOrderProcedure \
UPDATE #TEMPTABLE \
SET sCustomerName = B.sCustomerName \
,sSalesName = B.sSalesName \
,sSalesGroupName = B.sSalesGroupName \
,dReplyDate = B.dReplyDate \
,dDeliveryDate = B.dDeliveryDate \
FROM #TEMPTABLE A \
JOIN vwsdOrder B ON A.usdOrderLotGUID = B.usdOrderLotGUID \
UPDATE #TEMP \
SET nDyeingTime = CASE \
WHEN  sWorkingProcedureNameCurrent NOT IN ('配檢+退卷','配檢布','退卷','水洗','预定','打色','磨毛','訂邊','染色','半成品套色','成品套色','復色','缸練','進缸还原洗') then 0 \
WHEN  sWorkingProcedureNameCurrent  IN ('缸練','進缸还原洗') then 6 \
WHEN left(sColorNo,2) = 'CR' then 0 \
WHEN left(sColorNo,2) = 'BK' then 14 \
WHEN left(sColorNo,2) IN ('WT','IW') then 6 \
WHEN sWorkingProcedureNameCurrent IN ('配檢+退卷','配檢布','退卷','水洗','预定','打色','磨毛','訂邊','染色','半成品套色','成品套色','復色') \
then (CASE  \
WHEN left(sColorNo,1) = 'L' AND TRY_CAST((right(sColorNo,9)) AS int) <=600000000 AND TRY_CAST((right(sColorNo,9)) AS int) >=500000000 then 8 \
WHEN left(sColorNo,1) = 'L' AND TRY_CAST((right(sColorNo,8)) AS int) <=60000000 AND TRY_CAST((right(sColorNo,8)) AS int) >=50000000 then 8 \
WHEN left(sColorNo,1) = 'L' AND TRY_CAST((right(sColorNo,9)) AS int) <=500000000 AND TRY_CAST((right(sColorNo,9)) AS int) >=400000000 then 6 \
WHEN left(sColorNo,1) = 'L' AND TRY_CAST((right(sColorNo,8)) AS int) <=50000000 AND TRY_CAST((right(sColorNo,8)) AS int) >=40000000 then 6 \
WHEN left(sColorNo,2) = 'LN' AND TRY_CAST((right(sColorNo,9)) AS int) <=300000000 AND TRY_CAST((right(sColorNo,9)) AS int) >=100000000 then 4 \
WHEN left(sColorNo,2) = 'LN' AND TRY_CAST((right(sColorNo,8)) AS int) <=30000000 AND TRY_CAST((right(sColorNo,8)) AS int) >=10000000 then 4 \
WHEN left(sColorNo,1) = 'L' AND TRY_CAST((right(sColorNo,9)) AS int) <=300000000 AND TRY_CAST((right(sColorNo,9)) AS int) >=100000000 then 4 \
WHEN left(sColorNo,1) = 'L' AND TRY_CAST((right(sColorNo,8)) AS int) <=30000000 AND TRY_CAST((right(sColorNo,8)) AS int) >=10000000 then 4 \
ELSE 12 END)ELSE 12 END \
UPDATE #TEMP \
SET nTJTime = B.nTJTime \
FROM #TEMP A \
JOIN( \
SELECT A.sCardNo,(ISNULL(A.nFactInputQty,A.nPlanOutputQty)/ sProductWidth / sProductGMWT * 100 * 1000 / 0.9144)/20 AS nTJTime \
FROM #TEMP A \
)B ON A.sCardNo = B.sCardNo \
UPDATE #TEMP \
SET nPSTime = B.nPSTime \
FROM #TEMP A \
JOIN(  \
SELECT A.sCardNo,(ISNULL(A.nFactInputQty,A.nPlanOutputQty)*100000/sProductWidth/sProductGMWT/0.9144/nPSSpeed) AS nPSTime \
FROM #TEMP A \
)B ON A.sCardNo = B.sCardNo \
UPDATE #TEMP \
SET nSETime = B.nSETime \
FROM #TEMP A \
JOIN( \
SELECT A.sCardNo,ISNULL(A.nFactInputQty,A.nPlanOutputQty)*100000/sProductWidth/sProductGMWT/0.9144/nSESpeed AS nSETime \
FROM #TEMP A \
)B ON A.sCardNo = B.sCardNo \
UPDATE #TEMP \
SET sType = CASE WHEN sMaterialTypeName LIKE '%网%' AND sProductGMWT < 130 THEN 'NET' \
ELSE CASE WHEN sColorCatena = 'W' OR sColorCatena = 'K' THEN 'BW' \
ELSE 'Others' END END  \
UPDATE #TEMPTABLE \
SET sMaterialType = B.sType \
FROM #TEMPTABLE A \
JOIN #TEMP B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
UPDATE #TEMPTABLE \
SET sNotDoneProcedure = B.sWorkingProcedureName \
FROM #TEMPTABLE A \
JOIN ( \
SELECT DISTINCT  A.uppTrackJobGUID,D.sWorkingProcedureName \
FROM  \
(SELECT DISTINCT uppTrackJobGUID,sWorkingProcedureName FROM #TEMP) A \
CROSS APPLY( \
SELECT sWorkingProcedureName+',' FROM #TEMP AS B \
WHERE A.uppTrackJobGUID=B.uppTrackJobGUID \
FOR XML PATH('') \
) D (sWorkingProcedureName) \
) B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
UPDATE #TEMPTABLE \
SET nTJTime = B.nTJTime \
,nPSTime = B.nPSTime \
,nSETime = B.nSETime \
,nDyeingTime = B.nDyeingTime \
FROM #TEMPTABLE A \
JOIN #TEMP B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
UPDATE #TEMPTABLE \
SET sIsRush = 1 \
FROM #TEMPTABLE A \
JOIN [dbo].[pbCommonDataRushOrder] B ON A.sCardNo = B.sCardNo \
SELECT A.uppTrackJobGUID AS uppTrackJobGUIDA,B.uppTrackJobGUID AS uppTrackJobGUIDB \
INTO #T1 \
FROM pbCommonDataProductionSchedulingBase A \
LEFT JOIN #TEMPTABLE B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
UPDATE pbCommonDataProductionSchedulingBase \
SET bUsable = 0 \
FROM pbCommonDataProductionSchedulingBase A \
JOIN ( \
SELECT A.*, B.uGUID AS uGUIDB FROM pbCommonDataProductionSchedulingBase A \
LEFT JOIN  ppTrackJob B ON A.uppTrackJobGUID = B.uGUID \
)B ON A.ID = B.ID \
WHERE uGUIDB IS NULL \
UPDATE pbCommonDataProductionSchedulingBase \
SET bUsable = 0 \
FROM pbCommonDataProductionSchedulingBase A \
JOIN ppTrackJob B ON A.uppTrackJobGUID = B.uGUID AND B.tFactEndTime IS NOT NULL \
UPDATE pbCommonDataProductionSchedulingBase \
SET bUsable = 0 \
FROM pbCommonDataProductionSchedulingBase A \
JOIN psWorkFlowCard B ON A.sCardNo = B.sCardNo AND (B.sStatus IN ('取消','中止') OR ISNULL(B.bUsable,1)<>1) \
SELECT A.*,B.uppTrackJobGUID AS uppTrackJobGUIDB \
INTO #T2 \
FROM #TEMPTABLE A \
LEFT JOIN pbCommonDataProductionSchedulingBase B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
UPDATE pbCommonDataProductionSchedulingBase \
SET  \
bIsRush = B.sIsRush \
,nFactInputQty = B.nFactInputQty \
,sWorkingProcedureName = B.sWorkingProcedureName \
,iOrderProcedure = B.iOrderProcedure \
,sWorkingProcedureNameCurrent = B.sWorkingProcedureNameCurrent \
,sWorkingProcedureNameLast = B.sWorkingProcedureNameLast \
,sWorkingProcedureNameNext = B.sWorkingProcedureNameNext \
,tFactEndTimeLast = CONVERT(DATETIME,B.tFactEndTimeLast) \
,sNotDoneProcedure = B.sNotDoneProcedure \
,uppTrackJobGUID = B.uppTrackJobGUID \
,sColorBorder = B.sColorBorder \
,sLocation = B.sLocation \
,sRemark = B.sRemark \
,dReplyDate = B.dReplyDate \
,dDeliveryDate = B.dDeliveryDate \
FROM pbCommonDataProductionSchedulingBase A \
JOIN #T2 B ON A.uppTrackJobGUID = B.uppTrackJobGUID \
WHERE A.bUsable = 1 \
INSERT INTO pbCommonDataProductionSchedulingBase( \
bIsRush,sType,sCardNo,sMaterialNo,sMaterialType,sMaterialTypeName,sMaterialLot,sColorNo,nFactInputQty,nPlanOutputQty,sSourceName \
,sWorkingProcedureName,iOrderProcedure,sWorkingProcedureNameCurrent,sWorkingProcedureNameLast,sNotDoneProcedure \
,nTJTime,nPSTime,nDyeingTime,nSETime,uppTrackJobGUID,usdOrderLotGUID,upsWorkFlowCardGUID \
,sCustomerName,sSalesName,sProductWidth,sProductGMWT,nPSSpeed,nSESpeed,sSalesGroupName \
,nPSTemp1,nPS2Temp2,nPS2Temp3_7,nPS2Temp8,nSETemp,nSETemp2,nSETemp3_7,nSETemp8,sColorBorder \
,nOverTime,tFactEndTimeLast,sLocation,sRemark,sWorkingProcedureNameNext,dReplyDate,dDeliveryDate \
) \
SELECT sIsRush,'整理',sCardNo,sMaterialNo,sMaterialType,sMaterialTypeName,sMaterialLot,sColorNo,nFactInputQty,nPlanOutputQty, sSourceName \
,sWorkingProcedureName,iOrderProcedure,sWorkingProcedureNameCurrent,sWorkingProcedureNameLast,sNotDoneProcedure \
,nTJTime,nPSTime,nDyeingTime,nSETime,uppTrackJobGUID,usdOrderLotGUID,upsWorkFlowCardGUID \
,sCustomerName,sSalesName,sProductWidth,sProductGMWT,nPSSpeed,nSESpeed,sSalesGroupName \
,nPSTemp1,nPS2Temp2,nPS2Temp3_7,nPS2Temp8,nSETemp,nSETemp2,nSETemp3_7,nSETemp8,sColorBorder \
,DATEDIFF(MINUTE,tFactEndTimeLast,GETDATE()) AS nOverTime,CONVERT(DATETIME,tFactEndTimeLast),sLocation,sRemark, sWorkingProcedureNameNext,dReplyDate,dDeliveryDate \
FROM #T2 \
WHERE uppTrackJobGUIDB IS NULL \
UPDATE pbCommonDataProductionSchedulingBase \
SET sFactEndTimeLast = RIGHT(CONVERT(NVARCHAR(16),CONVERT(DATETIME,tFactEndTimeLast),120),11) \
,nOverTime = DATEDIFF(MINUTE,tFactEndTimeLast,GETDATE()) / 60 \
,sDeliveryDate = RIGHT(CONVERT(NVARCHAR(10),CONVERT(DATETIME,dDeliveryDate),120),5) \
,sReplyDate = RIGHT(CONVERT(NVARCHAR(10),CONVERT(DATETIME,dReplyDate),120),5) \
UPDATE pbCommonDataProductionSchedulingBase \
SET sOverTime = CASE WHEN nOverTime < 12 THEN '<12' WHEN nOverTime >=12 AND nOverTime <24 THEN '12-24'  \
							WHEN nOverTime >=24 AND nOverTime < 48 THEN '24-48' \
							WHEN nOverTime >=48 AND nOverTime < 72 THEN '48-72' \
							WHEN nOverTime >=72 THEN '>72' ELSE NULL END  \
SELECT *FROM pbCommonDataProductionSchedulingBase \
DROP TABLE #TEMPTABLE \
DROP TABLE #TEMP \
DROP TABLE #T1 \
DROP TABLE #T2 \
"