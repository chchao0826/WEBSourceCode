var cal = function () {
    var getList = $$('SedData').children;
    var sumTime = 0;
    $$('card-count').children[0].innerHTML = '总卡数:' + getList.length;
    for (var i = 0; i < getList.length; i++) {
        var ntime = getList[i].children[0].children[0].children[1].children[1].children[1].innerHTML;
        sumTime += parseFloat(ntime);
    }
    $$('card-time').children[0].innerHTML = '总耗时:' + sumTime.toFixed(2);
}

// ClassName
var _$ = function (id) {
    return document.getElementsByClassName(id);
}

// ID
var $$ = function (id) {
    return document.getElementById(id);
}

// Name
var __$ = function (id) {
    return document.getElementsByName(id);
}

// 尺寸修改
var getScreen = function () {
    var nWidth = document.body.clientWidth;
    var nHeight = document.documentElement.clientHeight;
    var content = $$('body');
    content.style.width = nWidth + 'px';
    content.style.height = nHeight - 50 + 'px';
}

// 页面初始
window.onload = function () {
    getScreen();
    // fullScreen();
}

// 修改屏幕尺寸后进行div的更新
window.onresize = function () {
    getScreen();
}

// 获取时间
var GetDate = function () {
    var day2 = new Date();
    var sYear = day2.getFullYear();
    var sMonth = day2.getMonth() + 1;
    var sDate = day2.getDate();
    var sHour = day2.getHours();
    var sMin = day2.getMinutes();
    var sSec = day2.getSeconds();
    if ((sMonth.toString().length) == 1) {
        sMonth = '0' + sMonth.toString()
    }
    if ((sDate.toString().length) == 1) {
        sDate = '0' + sDate.toString()
    }
    if ((sHour.toString().length) == 1) {
        sHour = '0' + sHour.toString()
    }
    if ((sMin.toString().length) == 1) {
        sMin = '0' + sMin.toString()
    }
    if ((sSec.toString().length) == 1) {
        sSec = '0' + sSec.toString()
    }
    var dateTime = sYear + "-" + sMonth + "-" + sDate + ' ' + sHour + ':' + sMin + ':' + sSec;
    return dateTime
}

// 得到当前工段
var GetThisWork = function () {
    var thisURL = document.URL;
    var thisWorking = thisURL.split('/')[5];
    thisWorking = thisWorking.toUpperCase();
    if (thisWorking.indexOf('PS') != -1) {
        thisWorking = '预定';
    } else if (thisWorking.indexOf('SE') != -1) {
        thisWorking = '成定';
    }
    return thisWorking;
}

//得到当前机台
var GetThisEquipemnt = function () {
    var eqList = $$('eqLi').children;
    for (var i = 0; i < eqList.length; i++) {
        if (eqList[i].className.indexOf('active') != -1) {
            return eqList[i].children[0].id;
        }
    }
}

// 向上
var AJAXUp = function () {
    var ul = $$('SedData');
    var ulList = ul.children;
    for (var i = 0; i < ulList.length; i++) {
        var className = ulList[i].className;
        if (className.indexOf('currentli') != -1) {
            ul.insertBefore(ulList[i], ulList[i - 1]);
            break;
        }
    }
}

// 向下
var AJAXDown = function () {
    var ul = $$('SedData');
    var ulList = ul.children;
    for (var i = 0; i < ulList.length; i++) {
        var className = ulList[i].className;
        if (className.indexOf('currentli') != -1) {
            ul.insertBefore(ulList[i + 1], ulList[i]);
            break;
        }
    }
}

// 置顶
var AJAXTop = function () {
    var ul = $$('SedData');
    var ulList = ul.children;
    for (var i = 0; i < ulList.length; i++) {
        var className = ulList[i].className;
        if (className.indexOf('currentli') != -1) {
            ul.prepend(ulList[i]);
        }
    }
}

// 置底
var AJAXBottom = function () {
    var ul = $$('SedData');
    var ulList = ul.children;
    for (var i = 0; i < ulList.length; i++) {
        var className = ulList[i].className;
        if (className.indexOf('currentli') != -1) {
            ul.append(ulList[i])
        }
    }
}

// 保存
var AJAXSave = function () {
    var nHDRID = GetThisEquipemnt();
    if (nHDRID == undefined) {
        alert('未选择机台!');
        return;
    }

    var ulList = $$('SedData').children;
    var saveList = [];

    for (var i = 0; i < ulList.length; i++) {
        var uGUID = ulList[i].children[0].children[0].children[2].innerHTML;
        var sDict = {
            'nHDRID': GetThisEquipemnt(),
            'tTime': GetDate(),
            'nRowNumber': i,
            'uppTrackJobGUID': uGUID,
        }
        saveList.push(sDict);
    }

    console.log(saveList)
    console.log(type(saveList))
    $.ajax({
        type: 'POST',
        url: 'AJAXSave',
        data: JSON.stringify(saveList),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {
            console.log('--------------');
        },
    });


    return saveList;
}


// 点击table tr 后增加选中效果
var onclicktr = function (trVar) {

    var trValue = $$(trVar);
    var trClass = trValue.className;
    if (trClass == 'currentli') {
        trValue.className = '';
    } else {
        trValue.className = 'currentli';
    }
}

// 选择机台后执行AJAX 刷新右边数据
var onclickCurrentli = function (LiVar) {
    var LiList = $$(LiVar).parentNode.parentNode.children;
    for (var i = 0; i < LiList.length; i++) {
        LiList[i].className = '';
    }
    $$(LiVar).parentNode.className = 'active'
    $('#SedData').load('AJAXDtl/' + LiVar);
    cal();
}

// 转移的数据+原有的数据 返回
var GetAJAXData = function () {
    var sDateTime = GetDate()
    var ThisEq = $$('eqLi').children;
    var EqVar = ''
    for (var i = 0; i < ThisEq.length; i++) {
        if (ThisEq[i].className == 'active') {
            EqVar = ThisEq[i].children[0].id;
        }
    }
    if (EqVar == '') {
        alert('未选择机台号');
        return;
    }
    // 左侧主表的数据
    var trList = $$('dataTable').children[0].children;
    // 右侧预排过的数据
    var DtlList = $$('SedData').children;
    var returnList = []
    var nRow = 0;
    for (var i = 0; i < DtlList.length; i++) {
        var uppTrackJobGUID = DtlList[i].children[0].children[0].children[2].innerHTML;
        var sDict = {
            'nHDRID': EqVar,
            'uppTrackJobGUID': uppTrackJobGUID,
            'nRowNumber': i,
            'tTime': sDateTime,
        }
        returnList.push(sDict);
        nRow = i + 1;
    }

    // console.log(returnList);

    for (var i = 0; i < trList.length; i++) {
        if (trList[i].className.indexOf('currentli') != -1) {
            var uppTrackJobGUID = trList[i].children[10].innerHTML;
            var sdict = {
                'nHDRID': EqVar,
                'uppTrackJobGUID': uppTrackJobGUID,
                'nRowNumber': nRow + i,
                'tTime': sDateTime,
            }
            returnList.push(sdict)
        }
        // console.log(trList[i].classList);
    }
    // console.log(returnList)
    cal();
    return returnList
}

// 删除选中的数据
var DeleteCurrentLi = function () {
    var trHTML = ''
    var trList = $$('dataTable').children[0].children;
    for (var i = 0; i < trList.length; i++) {
        var trClass = trList[i].className;
        if (trClass != 'currentli') {
            trHTML += trList[i].outerHTML
        }
    }
    cal();
    $$('dataTable').innerHTML = trHTML;
}

// AJAX插入数据
var AJAXInsertData = function () {
    var InserData = GetAJAXData();
    var sEqID = InserData[0]['nHDRID'];
    console.log('--------------')
    console.log(InserData);
    console.log('--------------')
    $.ajax({
        type: 'POST',
        url: 'AJAXInsertData',
        data: JSON.stringify(InserData),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {
            AJAXRightPage();
            AJAXLeftPage();
            cal();
        },
        error: function () {
            AJAXRightPage();
            AJAXLeftPage();
            cal();
        },
    });

}

// 获得当前机台
var thisEqFun = function () {
    var liList = $$('eqLi').children;
    var sEqList = [];
    for (var i = 0; i < liList.length; i++) {
        if (liList[i].className == 'active') {
            var sEqID = liList[i].children[0].id;
            var sEqName = liList[i].children[0].innerHTML;
            var sDict = {
                'nHDRID': sEqID,
                'sEquipmentName': sEqName,
            }
            sEqList.push(sDict);
        }
    }
    if (sEqList == '') {
        alert('未选择机台');
        return;
    }
    return sEqList;
}

// 删除数据
var AJAXDeleteData = function () {
    var DeleteData = $$('SedData').children;
    var DeleteList = [];
    for (var i = 0; i < DeleteData.length; i++) {
        var LiClass = DeleteData[i].className;
        if (LiClass.indexOf('currentli') != -1) {
            var uppTrackJobGUID = DeleteData[i].children[0].children[0].children[2].innerHTML;
            sDict = {
                'uppTrackJobGUID': uppTrackJobGUID
            }
            DeleteList.push(sDict);
        }
    }
    console.log(DeleteList);
    console.log('++++++++++++++')
    $.ajax({
        type: 'POST',
        url: 'AJAXDelete',
        data: JSON.stringify(DeleteList),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {
            AJAXRightPage();
            AJAXLeftPage();
            cal();
        },
        error: function () {
            AJAXRightPage();
            AJAXLeftPage();
            cal();
        },
    });
    // AJAXRightPage();
    // AJAXLeftPage();

}

// 更新右侧页面
var AJAXRightPage = function () {
    var thisEqVar = thisEqFun()[0]['nHDRID'];
    // console.log(thisEqVar);
    // console.log('==========================')
    $('#SedData').load('AJAXRightPage/' + thisEqVar);
    // alert('123')
}

// 更新左侧页面
var AJAXLeftPage = function () {
    var thisURL = document.URL;
    var thisWorking = thisURL.split('/')[5];
    console.log(thisWorking);
    $('#dataTable').load('AJAXLeftPage/' + thisWorking);
}

// 上移下移操作
var onclickMove = function (uppTrackJobGUID) {
    var ThisClass = $$(uppTrackJobGUID).className;
    if (ThisClass.indexOf('currentli') == '-1') {
        $$(uppTrackJobGUID).className = ThisClass + ' currentli'
    } else {
        var nRow = ThisClass.indexOf('currentli');
        var ThisClass = ThisClass.slice(0, nRow);
        $$(uppTrackJobGUID).className = ThisClass;
    }
    console.log($$(uppTrackJobGUID).className)
}

// 搜索功能
var search = function () {
    var GetInput = $$('sInput').value.toUpperCase();
    var dataTable = $$('dataTable').children[0].children;
    for (var i = 0; i < dataTable.length; i++) {
        if (dataTable[i].className.indexOf('currentli') != -1) {
            dataTable[i].classList.remove('currentli')
        }
    }

    for (var i = 0; i < dataTable.length; i++) {
        var sCardNo = dataTable[i].children[0].innerHTML;
        var sMaterialNo = dataTable[i].children[1].innerHTML;
        var sColorNo = dataTable[i].children[2].innerHTML;
        var sWorkingProcedureName = dataTable[i].children[9].innerHTML;

        if (sCardNo.indexOf(GetInput) != -1 || sMaterialNo.indexOf(GetInput) != -1 || sColorNo.indexOf(GetInput) != -1 || sWorkingProcedureName.indexOf(GetInput) != -1) {
            dataTable[i].className += ' currentli';
        }
    }
}

jQuery(function ($) {
    $('#dragslot').dragslot({
        dropCallback: function (el) {
            //	alert(el);
        }
    });
});

// 刷新页面
var refresh = function () {
    location.reload()
}
// 打印
var printPage = function () {

}

//获取当前时间
var getDateTime = function () {
    var myDate = new Date()
    var myDay = myDate.getDate();
    var myMonth = myDate.getMonth() + 1;
    var myYear = myDate.getFullYear();
    if (myDay.toString().length < 2) {
        myDay = 0 + myDay.toString();
    }
    if (myMonth.toString().length < 2) {
        myMonth = 0 + (myMonth + 1).toString();
    }
    var DataTime = myYear + '-' + myMonth + '-' + myDay;
    return DataTime
}

function sheet2blob(sheet, sheetName) {
    sheetName = sheetName || 'sheet1';
    var workbook = {
        SheetNames: [sheetName],
        Sheets: {}
    };
    workbook.Sheets[sheetName] = sheet;
    // 生成excel的配置项
    var wopts = {
        bookType: 'xlsx', // 要生成的文件类型
        bookSST: false, // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
        type: 'binary'
    };
    var wbout = XLSX.write(workbook, wopts);
    var blob = new Blob([s2ab(wbout)], {
        type: "application/octet-stream"
    });
    // 字符串转ArrayBuffer
    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
    }
    return blob;
}

function openDownloadDialog(url, saveName) {
    if (typeof url == 'object' && url instanceof Blob) {
        url = URL.createObjectURL(url); // 创建blob地址
    }
    var aLink = document.createElement('a');
    aLink.href = url;
    aLink.download = saveName || ''; // HTML5新增的属性，指定保存文件名，可以不要后缀，注意，file:///模式下不会生效
    var event;
    if (window.MouseEvent) event = new MouseEvent('click');
    else {
        event = document.createEvent('MouseEvents');
        event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    }
    aLink.dispatchEvent(event);
}

// 定型导出EXCEL
var ExportExcel = function () {
    var ulList = $$('SedData').children;
    var sWork = GetThisWork();
    var sthisEqFun = thisEqFun()[0]['sEquipmentName'];
    var aoa = [];
    var excelT = [sWork + sthisEqFun + '预排', , , , ];
    aoa.push(excelT);

    var excelTitle = ['序号', '卡号', '物料编号', '色号', '幅宽', '克重', '投胚量', '预计花费时间', '温度', '速度', '工段', '类别'];
    aoa.push(excelTitle);

    var nSUMTime = 0;
    var nCount = 0;
    var nSumQty = 0;
    var nRow = 1;
    for (var i = 0; i < ulList.length; i++) {
        nRow += 1
        var sCardNo = ulList[i].children[0].children[0].children[4].innerHTML;
        var sMaterialNo = ulList[i].children[0].children[0].children[5].innerHTML;
        var sColorNo = ulList[i].children[0].children[0].children[6].innerHTML;
        var sProductWidth = ulList[i].children[0].children[0].children[7].innerHTML;
        var sProductGMWT = ulList[i].children[0].children[0].children[8].innerHTML;
        var nFactInPutQty = ulList[i].children[0].children[0].children[9].innerHTML;
        var nTime = ulList[i].children[0].children[0].children[10].innerHTML;
        var nTemp = ulList[i].children[0].children[0].children[11].innerHTML;
        var nSpeed = ulList[i].children[0].children[0].children[12].innerHTML;
        var sWorkingProcedureName = ulList[i].children[0].children[0].children[13].innerHTML;
        var excelVar = [
            nRow, sCardNo, sMaterialNo, sColorNo, sProductWidth, sProductGMWT, nFactInPutQty, nTime,
            nTemp, nSpeed, sWorkingProcedureName
        ];
        aoa.push(excelVar);
        nCount += 1;
        nSUMTime += parseFloat(nTime);
        nSumQty += parseFloat(nFactInPutQty);
    }
    var sumExcel = ['合计', , , , nCount, nSumQty, nSUMTime, , , ]
    aoa.push(sumExcel);
    console.log(aoa);
    var sheet = XLSX.utils.aoa_to_sheet(aoa);
    sheet['!merges'] = [
        // 设置A1-C1的单元格合并
        {
            s: {
                r: 0,
                c: 0
            },
            e: {
                r: 0,
                c: 11
            }
        }
    ];
    dateTime = getDateTime();
    var excelName = sWork + sthisEqFun + '排单' + dateTime + '.xlsx';
    openDownloadDialog(sheet2blob(sheet), excelName);
}

// 选择布种别
var checkMasterialType = function (sType) {
    var thisURL = document.URL;
    var thisWorking = thisURL.split('/')[5];
    if (thisWorking.indexOf('#') != -1) {
        thisWorking = thisWorking.split('#')[0]
    }
    var returnValue = thisWorking + '_' + sType
    $('#dataTable').load('AJAXMasterialType/' + returnValue);

}

// 定型预排过的数据前端清空
var AJAXClearDtl = function () {
    $('#SedData').load('AJAXClearDtl');
}

// AJAX更新数据
var ClearData = function () {
    console.log('----o0-212')
    var returnData;
    $.ajax({
        type: 'POST',
        url: 'AJAXClear',
        data: JSON.stringify(returnData),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {
            console.log('--------------');
        },
    });
    AJAXClearDtl();
    AJAXLeftPage();
}