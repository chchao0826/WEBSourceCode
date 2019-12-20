// 增加机台的同时,下方数据列进行AJAX更新
var addData = function (ID) {
    var sectionList = $$('dragslot').children;
    for (var i = 0; i < sectionList.length; i++) {
        var varID = '#' + sectionList[i].id;
        if (sectionList[i].children[0].id == '' && sectionList[i].children[0].id.indexOf('-') == -1) {
            $(varID).load('AJAX/SaleData/' + ID);
            break;
        }
    }
}

// 如果添加的机台超过7个进行提醒
var alert7 = function (ID) {
    var nCount = GetCount();
    console.log('=====================21212121');
    var title3len = $$('title_3').children.length;
    console.log(title3len);
    console.log('===-------------=====')
    var iFlag = false;
    if (title3len >= nCount) {
        console.log('========')
        iFlag = true;
    }
    return iFlag
}

// 选择机台
var btnEqui = function (ID) {
    var iFlag = alert7(ID);
    var nCount = GetCount();
    if (iFlag == true) {
        alert('不能添加超过' + nCount + '个机台, 请修正');
        return;
    } else {
        console.log('=====================21212121')
        addactive(ID);
        var sName = $$(ID).children[0].innerHTML;
        addEuqi(sName, ID);
    }
}

// 重新计算width
var calwidth = function () {
    var title3 = $$('title_3').children;
    var nLength = (99 / title3.length).toFixed(2);
    for (var i = 0; i < title3.length; i++) {
        title3[i].style.width = nLength + '%';
    }
}

//选择机台后在右侧增加点击的机台,并且执行AJAX
var addEuqi = function (sName, iID) {
    var rightEq = $$('title_3').children;
    console.log(rightEq);
    var nLength = rightEq.length + 1;
    console.log('====2323312');
    var iFlag = false;
    for (var i = 0; i < rightEq.length; i++) {
        var eqID = rightEq[i].id;
        if (eqID == 'addEuqi_' + iID) {
            iFlag = true;
        }
    }

    if (iFlag == true) {
        alert('已经添加该机台,请确认!');
    } else {
        var ulObj = document.createElement("li");
        ulObj.style = 'width: ' + ((100 / nLength).toFixed(2) + '%');
        ulObj.id = 'addEuqi_' + iID
        ulObj.innerHTML = '<a onclick="clearEqui(\'addEuqi_' + iID + '\')">' + sName + '</a>';
        // 判断机台列表中是否包含

        $$('title_3').appendChild(ulObj);
        calwidth();
        console.log('================')
        addData(iID);
    }
}

// 增加活动标识
var addactive = function (ID) {
    var chidList = $$(ID).parentNode.children;
    for (var i = 0; i < chidList.length; i++) {
        if (chidList[i].className.indexOf('active') != -1) {
            chidList[i].className = '';
        }
    }
    $$(ID).className += 'active';
}

// 选择机台群组
var btnEquiModel = function (ID) {
    addactive(ID);
    $('#title_2').load('AJAX/equipment/' + ID);
}

// 更改预排数量
function GetCount() {
    var sWidth = $$('body').clientWidth;
    var nCount = parseInt(sWidth / 310);
    return nCount;
}

// 根据个数,计算显示多少个section
function calSec() {
    sCount = GetCount();
    sCount -= 1;
    console.log(sCount);
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        if (i > sCount) {
            dragslotList[i].className += ' hidden';
        }
    }
}

//删除按钮
// 点击清除机台
function clearEqui(ID) {
    var ulObj = $$(ID);
    $$('title_3').removeChild(ulObj);
    calwidth();
    deleteData(ID);
}


// 清除机台的同时,删除下面的详细信息
function deleteData(ID) {
    // var sectionList = $$('dragslot').children;
    var eqID = 'Eq_' + ID.split('_')[2];
    var VarID = ID.split('_')[2];
    // console.log('============')
    // console.log(eqID)
    var parentID = $$(eqID).parentNode.id;
    $$(parentID).removeChild($$(eqID));
    var ulObj = document.createElement("ul");
    ulObj.className = 'slot-list';
    sHtml = '<div> \
            <input class="title_var" type="text" readOnly="true" value=待选择> \
            <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:310px; font-size: 12px;" id="basic-addon1">待选择</span> \
        </div> \
        <li class="slot-item XG_li" id="Card_' + VarID + '"> \
            <div class="clearfix XG_div"> \
                <div> \
                    <div> \
                        <span>待选择</span> \
                    </div> \
                    <div> \
                        <span></span> \
                    </div> \
                </div> \
            </div> \
        </li>';
    console.log(sHtml);
    ulObj.innerHTML = sHtml;
    $$(parentID).appendChild(ulObj);
}

// 搜索数据
function SearchMain(value, sList, sType, sEquipmentID) {
    var iFlag = 0;
    for (var a = 0; a < sList.length; a++) {
        var sCardNo = sList[a].children[0].children[0].children[0].children[0].innerHTML;
        var sMaterialNo = sList[a].children[0].children[0].children[1].children[0].innerHTML;
        if (sMaterialNo.indexOf(value) != -1 || sCardNo.indexOf(value) != -1) {
            var nHeight = GetHeight(sEquipmentID)
            sList[a].className += ' search_get';
            var sEqui = sList[0].children[0].value
            $$('search_value').innerHTML += sCardNo + '/' + sEqui + '/' + sMaterialNo + '&nbsp|||';
            if (sType == 'Top') {
                iFlag = (100) + ((a + 2) * 80);
                break;
            } else if (sType == 'Bottom') {
                iFlag = ((a) * 110);
                break;
            }
        }
    }
    console.log(iFlag)
    return iFlag
}

function SearchPage(value) {
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        var UlList = dragslotList[i].children[0];
        if (UlList != undefined && UlList.id.indexOf('Eq') != -1) {
            var sEquipmentID = UlList.id;
            var childrenList = UlList.children
            var sTopList = childrenList[1].children;
            var sBottomList = childrenList[3].children;
            var sTopValue = SearchMain(value, sTopList, 'Top', sEquipmentID);
            var sBootomValue = SearchMain(value, sBottomList, 'Bottom', sEquipmentID);

            if (sTopValue != 0) {
                var sTopScroll = sTopValue;
                childrenList[1].scrollTop = sTopScroll;
            }
            if (sBootomValue != 0) {
                var sBootomScroll = sBootomValue;
                childrenList[3].scrollTop = sBootomScroll;
            }
        }
    }
    if (sTopValue == 0 || sBootomValue == 0) {
        return false;
    } else {
        return true;
    }
}

// 是否按回车键 
$('#searchValue').bind('keydown', function (event) {
    if (event.keyCode == "13") {
        var sValue = $$('searchValue').value;
        var iFlag = SearchPage(sValue);
        console.log(sValue)
        console.log('============')
        if (iFlag == false) {
            // findEqui(sValue);
            // innerRightEqui(sValue)
            SearchMain(sValue)
        }
    }
});