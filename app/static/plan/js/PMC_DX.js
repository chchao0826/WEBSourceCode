// 得到正在预排的工段
var GetCurrentWork = function () {
    var ThisLink = document.URL;
    var Working = ThisLink.split('/')[5];
    return Working
}

// 工段返回中文
var workToChinese = function (sWork) {
    if (sWork.indexOf('PS') != -1) {
        return '预定'
    } else if (sWork.indexOf('SXJ1') != -1) {
        return '水洗1'
    } else if (sWork.indexOf('SXJ2') != -1) {
        return '水洗2'
    } else if (sWork.indexOf('SE1') != -1) {
        return '成定型1'
    } else if (sWork.indexOf('SE2') != -1) {
        return '成定型2'
    }
}

// 取消上部分选中 // top-div      
var unCheck = function (UpOrDown) {
    var topli = '';
    if (UpOrDown == 'up') {
        topli = $$('top-div').children[0].children;
    } else if (UpOrDown == 'down') {
        topli = $$('bottom-div').children[0].children;
    }
    for (var i = 0; i < topli.length; i++) {
        topli[i].classList.remove("currentli");
    }
}

// 标记特急件
var GetLabel = function () {
    var topli = $$('top-div').children[0].children;
    for (var i = 0; i < topli.length; i++) {
        var iFlag = 0;
        var classListVar = topli[i].classList;
        for (var a = 0; a < classListVar.length; a++) {
            if (classListVar[a] == 'currentli') {
                var ThisClass = topli[i].className;
                // 标记急件
                if (ThisClass.indexOf('sUrgent') == -1) {
                    topli[i].className += ' sUrgent';
                    topli[i].classList.remove('currentli');
                    // 得到标记预排的卡号和盒车,去对应相同的盒车,现将相同的盒车找到,去除标记的卡号进行置顶,标记的卡号最后置顶,起到连带的作用
                    var sThisLocation = topli[i].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                    var sThisCardNo = topli[i].children[0].children[0].children[0].children[0].children[0].children[5].innerHTML;
                    for (var v = 0; v < topli.length; v++) {
                        var sLocation = topli[v].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                        var sCardNo = topli[v].children[0].children[0].children[0].children[0].children[0].children[5].innerHTML;
                        if (sLocation == sThisLocation && sCardNo != sThisCardNo) {
                            // var newli = topli[v];
                            // topli[v].remove();
                            topli[0].before(topli[v]);
                        }
                    }
                    for (var v = topli.length - 1; v >= 0; v--) {
                        var sLocation = topli[v].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                        var sCardNo = topli[v].children[0].children[0].children[0].children[0].children[0].children[5].innerHTML;
                        if (sLocation == sThisLocation && sCardNo == sThisCardNo) {
                            // var newli = topli[v];
                            // topli[v].remove();
                            topli[0].before(topli[v]);
                        }
                    }

                    // // $$('top-div').children[0].insertBefore(newli);
                    // topli[i].remove()
                    // $('ul_var').insertBefore(moveLi, 0);
                }
                // 取消急件
                else if (ThisClass.indexOf('sUrgent') != -1) {
                    var moveLi = topli[i];
                    var sThisLocation = topli[i].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                    topli[i].classList.remove('sUrgent');
                    topli[i].classList.remove('currentli');
                    var nRow1 = 0;
                    var nRow2 = 0;
                    for (var v = topli.length - 1; v >= 0; v--) {
                        var sLocation = topli[v].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                        console.log(sLocation)
                        console.log(sThisLocation)
                        if (topli[v].className.indexOf('sUrgent') != -1 && sLocation == sThisLocation) {
                            nRow1 = v;
                            break;
                        } else if (topli[v].className.indexOf('sUrgent') != -1 && sLocation != sThisLocation) {
                            nRow2 = v;
                        }
                    }
                    for (var v = 0; v < topli.length; v++) {
                        var sLocation1 = topli[nRow1].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                        var sLocation2 = topli[nRow2].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                        var sThisLocation2 = topli[v].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                        if (sLocation1 == sThisLocation2) {
                            nRow1 = v;
                        }
                        if (sLocation2 == sThisLocation2) {
                            nRow2 = v;
                        }
                    }
                    // 同布车内有急件,且为最后一个,需要将取消的急件,放置到最后,其他不变
                    if (nRow1 > nRow2) {
                        topli[nRow1 + 1].before(topli[i]);
                        // console.log(topli[nRow1])
                    } else if (nRow1 < nRow2) {
                        console.log('-------------')
                        for (var v = topli.length - 1; v >= 0; v--) {
                            var sLocation = topli[v].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                            if (sLocation == sThisLocation) {
                                topli[nRow2 + 1].before(topli[v])
                                // console.log(topli[nRow2])
                            }
                        }
                    } else if (nRow1 == nRow2 == 0) {
                        topli[i].className.remove('sUrgent');
                    }

                }
            }
        }
    }
}


// 删除数据
var DeleteLabelData = function () {
    var topli = $$('top-div').children[0].children;
    var removeLi = []
    var returnGUID = []
    for (var i = 0; i < topli.length; i++) {
        if (topli[i].className.indexOf('currentli') != -1) {
            var thisLi = topli[i];
            var thisLocation = topli[i].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
            var thisGUID = topli[i].children[0].children[0].children[0].children[0].children[0].children[16].innerHTML;
            returnGUID.push(thisGUID)
            for (var a = topli.length - 1; a >= 0; a--) {
                var varLocation = topli[a].children[0].children[0].children[0].children[0].children[0].children[2].innerHTML;
                if (thisLocation == varLocation) {
                    removeLi.push(topli[a]);
                    topli[a].remove()
                }
            }
        }
    }

    $.ajax({
        type: 'POST',
        url: 'Delete',
        data: JSON.stringify(returnGUID),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {},
    });


    for (var i = removeLi.length - 1; i >= 0; i--) {
        removeLi[i].classList.remove("currentli");
        removeLi[i].className += ' noPlan';
        $$('bottom_ul').append(removeLi[i])
    }
}


// 查找数据函数
var findInBrowser = function (findData, inputVar, sFlag) {
    var iFlag = 0
    for (var i = 0; i < findData.length; i++) {
        findData[i].classList.remove('findOut');
    }
    for (var i = 0; i < findData.length; i++) {
        var sCardNo = findData[i].children[0].children[0].children[0].children[0].children[0].children[5].innerHTML;
        var sMaterialNo = findData[i].children[0].children[0].children[0].children[0].children[0].children[3].innerHTML;
        var sWoring = findData[i].children[0].children[0].children[0].children[0].children[0].children[9].innerHTML;
        var sSalesGroupName = findData[i].children[0].children[0].children[0].children[0].children[0].children[14].innerHTML;
        if (sCardNo.indexOf(inputVar) != -1 || sMaterialNo.indexOf(inputVar) != -1 ||
            sWoring.indexOf(inputVar) != -1 || sSalesGroupName.indexOf(inputVar) != -1) {
            if (sFlag == 'top') {
                $$('showviews').innerHTML = sCardNo + '已预排'
                findData[i].className += ' findOut';
                $$('top-div').scrollTop = (i - 5) * 40;
                iFlag = 1
            } else if (sFlag == 'bottom') {
                $$('showviews').innerHTML = sCardNo + '未预排'
                findData[i].className += ' findOut';
                $$('bottom-div').scrollTop = (i - 5) * 40;
                iFlag = 1
            }
        }
    }
    return iFlag
}

// 得到最后一个卡号
var GetLastCardNo = function (findData) {
    for (var i = findData.length; i >= 0; i--) {
        var sCardNo = findData[i].children[0].children[0].children[0].children[0].children[0].children[5].innerHTML;
        return sCardNo
    }
}

// 搜索按钮
var SearchInput = function () {
    var thisWorking = GetCurrentWork()

    // 搜索按钮事件
    var inputVar = $$('sSearchInput').value;
    // 上部
    var topLi = $$('ul_var').children;
    // 下部
    // var bottomLi = $$('bottom_ul').children;

    // console.log(inputVar)
    // 初始化颜色

    var iflag = 0
    // 已经预排的数据
    var iflag = findInBrowser(topLi, inputVar, 'top');

    // 未预排的数据
    var iflag = findInBrowser(bottomLi, inputVar, 'bottom');

    // 数据里面的数据
    console.log(inputVar)
    if (iflag == 0) {
        $('#bottom-div').load('Search/' + inputVar + '_' + thisWorking);
        var Exec = function (bottomLi) {
            var sCardNo = GetLastCardNo(bottomLi)
            $$('showviews').innerHTML = sCardNo + '未预排'
            $$('bottom-div').scrollTo(0, 40 * bottomLi.length + 40);

        }
        var t = setTimeout(Exec(bottomLi), 50000);
    }
    // 重新计数
    getScreen();
}

// 点击备注按钮
var btnRemark = function () {
    var url = "http://198.168.6.56:5000/plan/PMC/Operation";
    window.open(url, '说明', 'height=400, width=320, top=270%, left=600%')
}

// 打印
var btnPrint = function () {
    var sWork = GetCurrentWork();
    var url = "http://198.168.6.56:5000/plan/PMC/ZL/Print/" + sWork;
    window.open(url)
}

// 保留两位小数
function changeTwoDecimal(x) {
    var f_x = parseFloat(x);
    if (isNaN(f_x)) {
        alert('function:changeTwoDecimal->parameter error');
        return false;
    }
    f_x = Math.round(f_x * 100) / 100;
    return f_x;
}

// 求和以及计数
var getCount = function () {
    var liList = $$('ul_var').children;
    var nCount = liList.length;
    var nCountVar = nCount - 1;
    var PSTimeList = __$('PSTime');
    var nSumPSTime = 0
    for (var i = 0; i < liList.length; i++) {
        nPSTime = liList[i].children[0].children[0].children[0].children[0].children[0].children[13]
            .innerText;
        nSumPSTime += parseFloat(nPSTime);
    }
    if (isNaN(nSumPSTime)) {
        nSumPSTime = 0
    }
    $$('sum_time').innerHTML = changeTwoDecimal(nSumPSTime);
    $$('count_tr').innerHTML = nCountVar;
}


// 保存按钮
var saveData = function () {
    var sWork = GetCurrentWork();
    var sWoring = workToChinese(sWork);
    var ulLi = $$('ul_var').children;
    var GetThisDate = GetDate();
    var PostLi = []
    for (var i = 0; i < ulLi.length; i++) {
        var uppTrackJobGUID = ulLi[i].children[0].children[0].children[0].children[0].children[0].children[16].innerHTML;
        var sLabel = 0
        if (ulLi[i].className.indexOf('sUrgent') != -1) {
            sLabel = 2
        }
        if (uppTrackJobGUID != "") {
            sDict = {
                'sType': sWoring,
                'uppTrackJobGUID': uppTrackJobGUID,
                'nRowNumber': i,
                'sLabel': sLabel,
                'tUpdateTime': GetThisDate,
            }
            PostLi.push(sDict);
        }

        ulLi[i].classList.remove('currentli');
        ulLi[i].classList.remove('findOut');
        ulLi[i].classList.remove('nowPlan');
    }
    $.ajax({
        type: 'POST',
        url: 'PostData',
        data: JSON.stringify(PostLi),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {},
    });
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

// 导出加载
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

// EXCEL导出功能
var ExportExcel = function () {
    var ulList = $$('ul_var').children;
    var sWork = GetCurrentWork();
    var sWork = workToChinese(sWork);
    var aoa = [];

    var excelT = [sWork + '预排', null, null, null, null, null, null, null, null, null, null, null, null,
        null, null, null, null
    ];
    aoa.push(excelT);

    var excelTitle = ['工段名称', '超时', '客户名称', '布车号', '物料编号', 'LOT', '卡号', '色号', '投胚', '上工段', '现工段', '下工段',
        '生交期', '业交期', '耗时', '营业课别', '工卡备注'
    ];
    aoa.push(excelTitle);

    for (var i = 0; i < ulList.length; i++) {
        var liList = ulList[i].children[0].children[0].children[0].children[0].children;
        for (var a = 0; a < liList.length; a++) {
            var tdList = liList[a].children;
            var nOverTime = tdList[0].innerText; //超时
            var sCustomerName = tdList[1].innerText; //客户名称
            var sLocation = tdList[2].innerText; //布车号	
            var sMaterialNo = tdList[3].innerText; //物料编号
            var sMaterialLot = tdList[4].innerText; //LOT
            var sCardNo = tdList[5].innerText; //卡号
            var sColorNo = tdList[6].innerText; //色号
            var nFactInputQty = tdList[7].innerText; //投胚	
            var sWorkingProcedureNameLast = tdList[8].innerText; //上工段	
            var sWorkingProcedureNameCurrent = tdList[9].innerText; //现工段
            var sWorkingProcedureNameNext = tdList[10].innerText; //下工段
            var dReplyDate = tdList[11].innerText; //生交期
            var dDeliveryDate = tdList[12].innerText; //业交期
            var nPSTime = tdList[13].innerText; //耗时	
            var sSalesGroupName = tdList[14].innerText; //营业课别
            var sRemark = tdList[15].innerText; //工卡备注
            var excelVar = [
                sWork, nOverTime, sCustomerName, sLocation, sMaterialNo, sMaterialLot, sCardNo,
                sColorNo, nFactInputQty, sWorkingProcedureNameLast, sWorkingProcedureNameCurrent,
                sWorkingProcedureNameNext, dReplyDate, dDeliveryDate, nPSTime, sSalesGroupName, sRemark
            ];
            aoa.push(excelVar);
        }

    }
    console.log(aoa);
    var sheet = XLSX.utils.aoa_to_sheet(aoa);
    sheet["A3"].s = {
        background: '#efefef';
    };
    dateTime = getDateTime();
    var excelName = sWork + '排单' + dateTime + '.xlsx';
    openDownloadDialog(sheet2blob(sheet), excelName);
}

//判断表格中是否少字段
var IsHaveFeild = function (exelData) {
    var nMaxRow = exelData.length - 1;
    if (exelData[nMaxRow]['TrackJob'] == undefined) {
        alert('导入失败, 没有TrackJob列');
        return false;
    }
    if (exelData[nMaxRow]['加急'] == undefined) {
        alert('导入失败,没有加急列');
        return false;
    }
    return true;
}

//开始导入
function importf(obj) {
    // 导入EXCEL
    var wb;
    var fileType = obj.value.split('.')[1]
    if (fileType != 'xlsx' && fileType != 'xls') {
        alert('传入文件格式错误,请重新传入');
        return;
    }
    var f = obj.files[0];
    var bUable = true;
    var reader = new FileReader();
    reader.onload = function (e) {
        var data = e.target.result;
        wb = XLSX.read(data, {
            type: 'binary'
        });
        // 获得EXCEL中第一个Sheet中的数据
        var sSheetNames = wb.SheetNames;
        var GetJsonData = [];
        for (var i = 0; i < sSheetNames.length; i++) {
            var sSheetName = sSheetNames[i];
            if (sSheetName.indexOf('水洗') != -1) {
                var excelJson = XLSX.utils.sheet_to_json(wb.Sheets[sSheetName]);
                bUable = IsHaveFeild(excelJson);
                var returnJson = {
                    'sType': sSheetName,
                    'Data': excelJson,
                }
                GetJsonData.push(returnJson);
            } else if (sSheetName == '预定' || sSheetName == '預定') {
                var excelJson = XLSX.utils.sheet_to_json(wb.Sheets[sSheetName]);
                bUable = IsHaveFeild(excelJson);
                var returnJson = {
                    'sType': '预定',
                    'Data': excelJson,
                }
                GetJsonData.push(returnJson);
            } else if (sSheetName.indexOf('成定型') != -1) {
                var excelJson = XLSX.utils.sheet_to_json(wb.Sheets[sSheetName]);
                bUable = IsHaveFeild(excelJson);
                var returnJson = {
                    'sType': sSheetName,
                    'Data': excelJson,
                }
                GetJsonData.push(returnJson);
            }
        }
        console.log(GetJsonData)
        if (bUable == true) {
            $.ajax({
                async: false,
                cache: false,
                type: 'POST',
                url: 'ImportData',
                data: JSON.stringify(GetJsonData),
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (data) {
                    alert('导入成功');
                },
                error: function (data) {
                    alert('导入成功');
                },
            });
            Refresh();
        }
    };
    reader.readAsBinaryString(f);
}