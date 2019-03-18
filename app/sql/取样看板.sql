create table #TT (machine nvarchar(20))
insert into #TT values('A001')
insert into #TT values('A002')
insert into #TT values('A003')
insert into #TT values('A004')
insert into #TT values('A007')
insert into #TT values('A006')
insert into #TT values('B007')
insert into #TT values('B008')
insert into #TT values('B009')
insert into #TT values('B010')
insert into #TT values('C015')
insert into #TT values('C016')
insert into #TT values('C017')
insert into #TT values('C018')
insert into #TT values('C019')
insert into #TT values('C020')
insert into #TT values('D021')
insert into #TT values('D022')
insert into #TT values('D023')
insert into #TT values('D024')
insert into #TT values('E025')
insert into #TT values('E026')
insert into #TT values('E027')
insert into #TT values('E028')
insert into #TT values('E029')
insert into #TT values('E030')
insert into #TT values('E031')
select #TT.machine AS sEquipmentNo
,A.batch_text_01 AS sCardNo, "Function"
,case when "Function"=123 then left(right(convert(varchar(20) ,timeRequested),7),5) +' :' + case when opcallstate=1 then '尚未' else '' end+'取樣' 
when "function"=146 and timetoopcall=timetonextstep then convert(nvarchar(10),timetoopcall)+'分鐘後取樣' end as scall,
CASE WHEN timetoopcall+10>timetoend then convert(nvarchar(10),timetoopcall)+'分鐘後出步' END AS sout
,timetoopcall AS nNextCallTime
,CASE WHEN K.sBrandName is null THEN K.sCustomerName ELSE K.sBrandName END AS sCustomerName
,I.sArtColorNo AS sColorNo
,I.sLotColorName AS sColorName
,I.sMaterialNo  AS sMaterialNo
,timeRequested
into #T
from #TT 
left join [192.168.11.10].[ORGATEX].[dbo].[BatchDetail] A WITH(NOLOCK) ON #TT.Machine=A.Machine_No collate Chinese_PRC_CI_AI_WS
left join [192.168.11.10].[ORGATEX-INTEG].[dbo].[Machinestatus] F WITH(NOLOCK) on F.DyelotrefNo=A.Batch_Ref_No collate Chinese_PRC_CI_AI_WS
left join [192.168.11.10].[ORGATEX-INTEG].[dbo].[dyelot_QC] G WITH(NOLOCK) on G.DyelotrefNo=A.Batch_Ref_No collate Chinese_PRC_CI_AI_WS
left join  [198.168.6.253].[HSWarpERP_NJYY].dbo.psWorkFlowCard H WITH(NOLOCK) ON H.sCardNo=LEFT(A.batch_text_01,10) collate Chinese_PRC_CI_AI_WS
left join  [198.168.6.253].[HSWarpERP_NJYY].dbo.vwsdOrder I WITH(NOLOCK) ON H.usdOrderLotGUID = I.usdOrderLotGUID
left join  [198.168.6.253].[HSWarpERP_NJYY].dbo.pbCustomer K WITH(NOLOCK) ON I.upbCustomerGUID=K.uGUID and K.bUsable='1'
left join (select batch_ref_no,sum(case when AlarmGroup=1 then 1 else 0 end) as Alarmcount
from  [192.168.11.10].[ORGATEX].[dbo].[MachineProtocol] WITH(NOLOCK)
where logtimestamp >=  (CONVERT(NVARCHAR(10), DATEADD(DD, -3, GETDATE()), 120)+' 8:00' )
group by batch_ref_no) J on J.batch_ref_no=A.Batch_Ref_No
where A.started is not null and A.terminated is null 
order by A.machine_no
select sEquipmentNo,case when sCardNo like '20%' then '洗缸' else  sCardNo end  as sCardNo
,sCustomerName,sColorNo,sMaterialNo
,case when scall is null then sout else scall end as special
,nNextCallTime
,ROW_NUMBER() OVER(ORDER BY sEquipmentNo) AS nRowNumber
INTO #TTT
from #T
where (scall is not null or sout is not null) and  convert(decimal(18,2),nNextCallTime) < 15
order by case when scall like '%後%' or sout  like '%後%' then null else timeRequested end DESC, convert(decimal(18,2),nNextCallTime) 
SELECT *FROM #TTT ORDER BY nRowNumber
drop table #TTT
drop table #TT
drop table #T