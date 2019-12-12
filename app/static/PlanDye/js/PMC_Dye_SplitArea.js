//元素的鼠标落下事件
var mouseDownMove = function (ID) {
    var ev = ID || event;
    var split_width = $$(ID).parentNode.children[1].offsetHeight;
    document.onmousemove = function (ev) {
        var ev = ev || event;
        split_width = ev.clientY - 164;
        $$(ID).parentNode.children[1].style.height = split_width + 'px';
    }
    document.onmouseup = function (ev) {
        $$(ID).parentNode.children[1].style.height = split_width + 'px';
        setCookies(ID, split_width);
        document.onmousemove = null;
    }
}

// cookies 写入 / 读取
var setCookies = function (ID, sWidth) {
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = ID + '=' + sWidth + ';expires = ' + exp.toGMTString();
}

// cookie 读取
var getCookie = function (ID) {
    var cookieList = document.cookie.split(';');
    for (var i = 0; i < cookieList.length; i++) {
        var cookies = cookieList[i].replace(/\s/ig, '');
        if (cookies.indexOf(ID) != -1) {
            console.log(ID)
            return cookies.split('=')[1];
        }
    }
}

// 读取cookie 刷新执行
var UpdateWidth = function (ID) {
    var split_width = getCookie(ID);
    return split_width;
}

////////////////////////////////////

// 通过eq_ID 得到ID_width 传入后端
var Get_ID_Width = function (ID) {
    var sEquipmentID = ID.split('_')[1];
    var splitName = 'split_span_' + sEquipmentID;
    var sWidth = UpdateWidth(splitName);
    if (sWidth == undefined) {
        return sEquipmentID + '_' + '660';
    } else {
        return sEquipmentID + '_' + sWidth;

    }
}

// 增加机台的同时,下方数据列进行AJAX更新
var addData = function (ID) {
    var sectionList = $$('dragslot').children;
    var sGet_ID_Width = Get_ID_Width(ID);
    for (var i = 0; i < sectionList.length; i++) {
        var varID = '#' + sectionList[i].id;
        if (sectionList[i].children[0].id == '' && sectionList[i].children[0].id.indexOf('-') == -1) {
            $(varID).load('SplitArea/AJAX/equipment/' + sGet_ID_Width);
            break;
        }
    }
}

// 清空选中
var clearCheck = function () {
    var funClearCheck = function (li) {
        if (li.className.indexOf('currentli') != -1) {
            li.className = 'slot-item li_style';
        }
    }
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        var topList = dragslotList[i].children[0].children[1].children;
        var bottomList = dragslotList[i].children[0].children[3].children;
        for (var a = 0; a < topList.length; a++) {
            funClearCheck(topList[a]);
        }
        for (var a = 0; a < bottomList.length; a++) {
            funClearCheck(bottomList[a]);
        }
    }
}

// 执行更新页面的AJAX
var UpdataPage = function () {
    var dragslotList = $$('dragslot').children;
    var sUpdateList = [];
    for (var i = 0; i < dragslotList.length; i++) {
        var sectionID = dragslotList[i].id;
        var nHDRID = dragslotList[i].children[0].id.split('_')[1];
        if (nHDRID != undefined) {
            sDict = {
                'sectionID': sectionID,
                'nHDRID': nHDRID,
            }
            sUpdateList.push(sDict);
        }
    }
    for (var i = 0; i < sUpdateList.length; i++) {
        var sectionID = sUpdateList[i].sectionID;
        var nHDRID = sUpdateList[i].nHDRID;

        var sWidth = Get_ID_Width('eq_' + nHDRID).split('_')[1];
        $('#' + sectionID).load('SplitArea/AJAX/equipment/' + +nHDRID + '_' + sWidth)
    }
}

// 保存操作
var saveData = function () {
    // 得到上方的数据
    var dragslotList = $$('dragslot').children;
    var sList = []
    var sUpdateTime = GetDate()
    for (var i = 0; i < dragslotList.length; i++) {
        var nHDRID = dragslotList[i].children[0].id.split('_')[1];
        var topList = dragslotList[i].children[0].children[1].children;
        for (var a = 0; a < topList.length; a++) {
            var LiID = topList[a].id.split('_')[1];
            var sDict = {
                'nHDRID': nHDRID,
                'ID': LiID,
                'nRowNumber': a,
                'tUpdateTime': sUpdateTime,
            }
            if (LiID != '' && nHDRID != undefined && LiID != undefined) {
                sList.push(sDict);
            }
        }
    }
    UpdateSection();
    if (sList.length > 0) {
        $.ajax({
            type: 'POST',
            url: 'SplitArea/AJAXPOST',
            data: JSON.stringify(sList),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            success: function (data) {
                UpdataPage();
                alert('保存成功');
            },
            error: function (data) {
                if (data['status'] == 200) {
                    UpdataPage();
                    alert('保存成功');
                } else {
                    UpdataPage();
                    alert('保存失败');
                }
            }
        });
    }
}

// 预排按钮
var InsertPlan = function () {
    // 得到下方选中的数据
    var dragslotList = $$('dragslot').children;
    var sList = []
    var tUpdateTime = GetDate()
    for (var i = 0; i < dragslotList.length; i++) {
        var nHDRID = dragslotList[i].children[0].id.split('_')[1];
        var bottomList = dragslotList[i].children[0].children[3].children;
        for (var a = 0; a < bottomList.length; a++) {
            if (bottomList[a].className.indexOf('currentli') != -1) {
                var LiID = bottomList[a].id.split('_')[1];
                var sDict = {
                    'nHDRID': nHDRID,
                    'ID': LiID,
                    'nRowNumber': a + 1,
                    'tUpdateTime': tUpdateTime,
                }
                if (LiID != '' && nHDRID != undefined && LiID != undefined) {
                    sList.push(sDict);
                }
            }
        }
    }
    if (sList.length > 0) {
        $.ajax({
            type: 'POST',
            url: 'SplitArea/AJAXInsert',
            data: JSON.stringify(sList),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            success: function (data) {
                UpdataPage();
                alert('保存成功');
            },
            error: function (data) {
                if (data['status'] == 200) {
                    UpdataPage();
                    alert('保存成功');
                } else {
                    UpdataPage();
                    alert('保存失败');
                }
            }
        });
    }
    console.log(sList)
}

// 取消预排按钮
var DeletePlan = function () {
    // 得到上方选中的数据
    var dragslotList = $$('dragslot').children;
    var sList = []
    var sUpdateTime = GetDate()

    for (var i = 0; i < dragslotList.length; i++) {
        var nHDRID = dragslotList[i].children[0].id.split('_')[1];
        var topList = dragslotList[i].children[0].children[1].children;
        for (var a = 0; a < topList.length; a++) {
            if (topList[a].className.indexOf('currentli') != -1) {
                var LiID = topList[a].id.split('_')[1];
                var sDict = {
                    'nHDRID': nHDRID,
                    'ID': LiID,
                    'tUpdateTime': sUpdateTime,
                }
                if (LiID != '' && nHDRID != undefined && LiID != undefined) {
                    sList.push(sDict);
                }
            }
        }
    }
    if (sList.length > 0) {
        $.ajax({
            type: 'POST',
            url: 'SplitArea/AJAXDelete',
            data: JSON.stringify(sList),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            success: function (data) {
                UpdataPage();
                alert('保存成功');
            },
            error: function (data) {
                if (data['status'] == 200) {
                    UpdataPage();
                    alert('保存成功');
                } else {
                    UpdataPage();
                    alert('保存失败');
                }
            }
        });
    }
}


// 洗缸名称变更
var InsertXG = function (currentli) {
    var dragslot = $$('dragslot').children;
    var returnList = [];
    var sConfirmMessage = '确定在 \n'
    for (var i = 0; i < dragslot.length; i++) {
        var nHDRID = dragslot[i].children[0].id.split('_')[1],
            sEquipmentNo = dragslot[i].children[0].children[0].children[0].value;
        var liList = dragslot[i].children[0].children[1].children;
        for (var a = 0; a < liList.length; a++) {
            if (liList[a].className.indexOf('currentli') !== -1) {
                sDict = {
                    'nHDRID': nHDRID,
                    'sEquipmentNo': sEquipmentNo,
                    'nRowNumber': a,
                    'tUpdateTime': GetDate(),
                }
                returnList.push(sDict);
                sConfirmMessage += sEquipmentNo + '第' + (a + 1) + '回 \n';
            }
        }
    }
    sConfirmMessage += "插入洗缸么?";
    console.log(returnList)
    if (returnList.length != 0) {

        // 弹窗进行确定是否插入洗缸
        var truthBeTold = window.confirm(sConfirmMessage);
        if (truthBeTold) {
            $.ajax({
                type: 'POST',
                url: 'SplitArea/InsertXG',
                data: JSON.stringify(returnList),
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function (data) {
                    UpdataPage();
                    alert('插入洗缸成功');
                },
                error: function (data) {
                    if (data['status'] == 200) {
                        UpdataPage();
                        alert('插入洗缸成功');
                    } else {
                        UpdataPage();
                        alert('插入洗缸失败');
                    }
                }
            });
        }
    } else {
        alert('未选择数据,无法插入洗缸,请确认!!!')
    }
    console.log(sConfirmMessage)
}


// 如果点击洗缸文字插入洗缸修改为取消洗缸
// var updateXGBtn = function (sDragText) {
//     var sXGvar = $$('XG_li').children[0].innerHTML;
//     if (sXGvar == '插入洗缸') {
//         $$('XG_li').innerHTML = '<a>取消洗缸</a>';
//         $$('XG_li').onclick = deleteXG();
//     }
//     console.log(sXGvar);

// }