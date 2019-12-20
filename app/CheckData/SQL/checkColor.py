# -*- coding: utf-8 -*-

# 色样获取,并对确认的色样进行删除和确认
def sCheckColorSql():
    return "SELECT \
        sColorNo,sColorName,sColorCode \
        ,CASE WHEN bIsCheck = 1 THEN ' 	#F0FFF0' WHEN bIsCheck = 0 THEN '#FF0000' END AS sIsCheck \
        ,CASE WHEN bUsable = 0 THEN '#F00' ELSE '' END AS sIsDelete \
        FROM tmColor \
        WHERE sColorCode IS NOT NULL \
        ORDER BY bUsable DESC ,bIsCheck DESC"


