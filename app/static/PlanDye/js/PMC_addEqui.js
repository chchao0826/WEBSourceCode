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
        addData(iID);
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

// 点击清除机台
var clearEqui = function (ID) {
    var ulObj = $$(ID);
    $$('title_3').removeChild(ulObj);
    calwidth();
    deleteData(ID);
}

// 如果添加的机台超过7个进行提醒
var alert7 = function (ID) {
    console.log('=====================21212121')
    var title3len = $$('title_3').children.length;
    console.log(title3len);
    console.log('===-------------=====')
    var iFlag = false;
    if (title3len >= 7) {
        console.log('========')
        iFlag = true;
    }
    return iFlag
}


// 清除机台的同时,删除下面的详细信息
var deleteData = function (ID) {
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
        <div class="Top_Div"> \
            <li class="slot-item XG_li"> \
                <div class="clearfix XG_div"> \
                    <div> \
                        <div> \
                            <span></span> \
                        </div> \
                        <div> \
                            <span></span> \
                        </div> \
                    </div> \
                </div> \
            </li> \
        </div> \
        <div class="Split_Span" id="split_span_{{Eq}}"> \
        </div> \
        <div class="Bottom_Area"></div>';

    console.log(sHtml);
    ulObj.innerHTML = sHtml;

    $$(parentID).appendChild(ulObj);
}


// 选择机台群组
var btnEquiModel = function (ID) {
    addactive(ID);
    $('#title_2').load('AJAX/equipment/' + ID);
}

// 选择机台
var btnEqui = function (ID) {
    var iFlag = alert7(ID);
    if (iFlag == true) {
        alert('不能添加超过七个机台, 请修正');
        return;
    } else {
        console.log('=====================21212121')
        addactive(ID);
        var sName = $$(ID).children[0].innerHTML;
        addEuqi(sName, ID);
        UpdateSection();
    }
}

// 保存点击的机台, 放进cookie中, 开启网址后自动执行
var UpdateSection = function () {
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        var sesID = dragslotList[i].id;
        var nHDRID = dragslotList[i].children[0].id.split('_')[1];
        var Days = 30;
        var exp = new Date();
        exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
        document.cookie = sesID + '=' + nHDRID + ';expires = ' + exp.toGMTString();
    }
    console.log(document.cookie);
}

// cookie 读取sesID
var getSesCookie = function () {
    var cookieList = document.cookie.split(';');
    var nHDRIDList = ''
    for (var i = 0; i < cookieList.length; i++) {
        var cookies = cookieList[i].replace(/\s/ig, '');
        if (cookies.indexOf('section') != -1) {
            var sectionID = cookies.split('=')[0];
            var nHDRID = cookies.split('=')[1];
            var sWidth = Get_ID_Width('eq_' + nHDRID).split('_')[1];
            if (nHDRID != 'undefined') {
                nHDRIDList = nHDRIDList + nHDRID + ','
                $('#' + sectionID).load('SplitArea/AJAX/equipment/' + String(nHDRID) + '_' + String(sWidth));
            }
        }
    }
    console.log(nHDRIDList)
    console.log('=================')
    Update_Title_3(nHDRIDList);
}

// 更新 title_3 cookie中的机台信息
var Update_Title_3 = function (nHDRIDList) {
    console.log('=----===');
    console.log(nHDRIDList);
    $('#title_3').load('SplitArea/Title3/' + nHDRIDList)
}



// 