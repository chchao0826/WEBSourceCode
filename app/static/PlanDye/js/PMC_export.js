// 准备数据
var btnReadyData = function () {
    $('#divExport').load('AJAXExport', function (responseTxt, statusTxt, xhr) {
        if (statusTxt == "success")
            $$('btnExport').removeChild($$('btnExport').children[0]);
        var aObj = document.createElement("a");
        aObj.setAttribute("onclick", "ExportExcel()");
        aObj.innerHTML = '导出数据';
        aObj.className = 'saveLi';
        $$('btnExport').appendChild(aObj);
        if (statusTxt == "error")
            alert("加载数据失败");
    })
}

// 导出EXCEL
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

// 将workbook装化成blob对象
function workbook2blob(workbook) {
    // 生成excel的配置项
    var wopts = {
        // 要生成的文件类型
        bookType: "xlsx",
        // // 是否生成Shared String Table，官方解释是，如果开启生成速度会下降，但在低版本IOS设备上有更好的兼容性
        bookSST: false,
        type: "binary"
    };
    var wbout = XLSX.write(workbook, wopts);
    // 将字符串转ArrayBuffer
    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xff;
        return buf;
    }
    var blob = new Blob([s2ab(wbout)], {
        type: "application/octet-stream"
    });
    return blob;
}

// 导出EXCEL
var ExportExcel = function () {
    var tableData = $$('divExport').children[0].children[0].children;

    var excelTitle = ['机台号', '滞留时间', '客户名', '生产卡号', '物料编号', 'LOT号', '色号', '实际投胚', '上工段', '当前工段', '下工段', '染色预计花费', '布车号', '工卡备注', '订单号'];

    var a = 0;
    var c = 0;
    var sVar = '';
    var dDate = getDateTime();

    var titleRow = []

    var sheetAName, sheetBName, sheetCName, sheetDName

    var aoaA = [],
        aoaB = [],
        aoaC = [],
        aoaD = []

    for (var i = 1; i < tableData.length; i++) {
        var trList = tableData[i].children;
        var sEquipmentNo = trList[0].innerHTML;
        var sPlanEquipmentNo = trList[1].innerHTML;
        var sOverTime = trList[2].innerHTML;
        var sCustomerName = trList[3].innerHTML;
        var sCardNo = trList[4].innerHTML;
        var sMaterialNo = trList[5].innerHTML;
        var sMaterialLot = trList[6].innerHTML;
        var sColorNo = trList[7].innerHTML;
        var nFactInputQty = trList[8].innerHTML;
        var sWorkingProcedureNameLast = trList[9].innerHTML;
        var sWorkingProcedureNameCurrent = trList[10].innerHTML;
        var sWorkingProcedureNameNext = trList[11].innerHTML;
        var nDyeingTime = trList[12].innerHTML;
        var sLocation = trList[13].innerHTML;
        var sRemark = trList[14].innerHTML;
        var sOrderNo = trList[15].innerHTML;

        var excelVar = [
            sEquipmentNo, sOverTime, sCustomerName, sCardNo, sMaterialNo, sMaterialLot, sColorNo,
            nFactInputQty, sWorkingProcedureNameLast, sWorkingProcedureNameCurrent, sWorkingProcedureNameNext, nDyeingTime, sLocation, sRemark, sOrderNo
        ];

        var excelT = [dDate + sEquipmentNo + '染色排单'];
        if (sVar != sEquipmentNo) {
            sVar = sEquipmentNo
            a = 0
        }
        // console.log(sEquipmentNo)
        // console.log(excelVar)
        if (sEquipmentNo.indexOf('A') != -1) {
            if (a == 0) {
                aoaA.push(excelT);
                aoaA.push(excelTitle);
                if (sheetAName == undefined) {
                    c = 0
                }
                titleRow.push({
                    'sEquipmentNo': sEquipmentNo,
                    'nROw': c,
                })

                sheetAName = 'A群组';

            }
            aoaA.push(excelVar);
            a += 1
            c += 1

        } else if (sEquipmentNo.indexOf('B') != -1) {
            if (a == 0) {
                aoaB.push(excelT);
                aoaB.push(excelTitle);

                if (sheetBName == undefined) {
                    c = 0
                }
                titleRow.push({
                    'sEquipmentNo': sEquipmentNo,
                    'nROw': c,
                })


                sheetBName = 'B群组';
            }
            aoaB.push(excelVar);
            a += 1
            c += 1

        } else if (sEquipmentNo.indexOf('C') != -1) {
            if (a == 0) {
                aoaC.push(excelT);
                aoaC.push(excelTitle);

                if (sheetCName == undefined) {
                    c = 0;
                }
                titleRow.push({
                    'sEquipmentNo': sEquipmentNo,
                    'nROw': c,
                })

                sheetCName = 'C群组';
            }
            aoaC.push(excelVar);
            a += 1;
            c += 1;

        } else if (sEquipmentNo.indexOf('D') != -1) {
            if (a == 0) {
                aoaD.push(excelT);
                aoaD.push(excelTitle);

                if (sheetCName == undefined) {
                    c = 0;
                }
                titleRow.push({
                    'sEquipmentNo': sEquipmentNo,
                    'nROw': c,
                })

                sheetDName = 'D群组';
            }
            aoaD.push(excelVar);
            a += 1;
            c += 1;

        }

    }

    var sheetA = XLSX.utils.aoa_to_sheet(aoaA);
    var sheetB = XLSX.utils.aoa_to_sheet(aoaB);
    var sheetC = XLSX.utils.aoa_to_sheet(aoaC);
    var sheetD = XLSX.utils.aoa_to_sheet(aoaD);
    console.log(titleRow)
    var wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, sheetA, sheetAName);
    XLSX.utils.book_append_sheet(wb, sheetB, sheetBName);
    XLSX.utils.book_append_sheet(wb, sheetC, sheetCName);
    XLSX.utils.book_append_sheet(wb, sheetD, sheetDName);


    const workbookBlob = workbook2blob(wb);

    var excelName = getDateTime() + '染色排单.xlsx';

    openDownloadDialog(workbookBlob, excelName);


    // openDownloadDialog(sheet2blob(sheetB), sheetBName);
    // openDownloadDialog(sheet2blob(sheetC), sheetCName);
    // openDownloadDialog(sheet2blob(sheetD), sheetDName);
    // console.log(tableData);
}

