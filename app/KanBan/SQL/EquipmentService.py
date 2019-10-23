# -*-coding:utf-8-*-


# 故障检修看板
def equipmentServiceSQL():
    return "SELECT A.sServiceNO \
    ,RIGHT(CONVERT(NVARCHAR(11),A.tBeginTime,120),6) + RIGHT(CONVERT(NVARCHAR(16),A.tBeginTime,120),5) AS sTime \
    ,RIGHT(A.sWorkCentreName,3) AS sWorkCentreName \
    ,A.sReportName, A.sServiceType, A.sEquipmentName, A.sEquipmentNo, A.sEquipmentDetailType \
    ,A.sEquipmentDetail, A.sServiceName, A.sFaultReason, A.sServiceStatus \
    ,CASE WHEN A.sServiceName IS NULL THEN \
        CASE WHEN DATEDIFF(MINUTE,A.tBeginTime,GETDATE()) < 15 THEN '#00FF00' \
                WHEN DATEDIFF(MINUTE,A.tBeginTime,GETDATE()) < 30 THEN '#FFFF00' \
                WHEN DATEDIFF(MINUTE,A.tBeginTime,GETDATE()) >= 30 THEN '#FF0000' END \
    ELSE \
        CASE WHEN A.sServiceStatus = '待零件' THEN \
                CASE WHEN DATEDIFF(DAY,A.tBeginTime,GETDATE()) < 3 THEN '#FFFF00' \
                        WHEN DATEDIFF(DAY,A.tBeginTime,GETDATE()) >= 3 THEN '#FF0000' END \
        WHEN A.sServiceStatus = '待完成' OR A.sServiceStatus IS NULL THEN \
                CASE WHEN DATEDIFF(HOUR,A.tBeginTime,GETDATE()) < 6 THEN '#00FF00' \
                        WHEN DATEDIFF(HOUR,A.tBeginTime,GETDATE()) < 12 THEN '#FFFF00' \
                        WHEN DATEDIFF(HOUR,A.tBeginTime,GETDATE()) < 24 THEN '#FF0000' END END \
    END AS sStatus \
    FROM [198.168.6.253].[HSWarpERP_NJYY].[dbo].emEquipmentServiceRecord A \
    WHERE A.iNoteTypeID = '1237' AND iSNULL(A.sServiceStatus,'') != '已完成'"
