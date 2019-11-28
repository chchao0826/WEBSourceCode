// 判断虚拟机台有无洗缸没有进行添加
var addClear = function () {
    var sList = $$('Eq_35').children;

    var ulObj = document.createElement("li");
    ulObj.className = 'slot-item li_style';
    ulObj.style = 'line-height: 80px;';
    ulObj.innerHTML = '<div><div><div><span>空白</span></div></div></div>';
    if (sList.length < 2) {
        $$('Eq_35').appendChild(ulObj);
    }
}

// 保存后更新列
var updateCol = function () {
    console.log('刷新列')
    var getList = $$('dragslot').children;
    console.log(getList)
    for (var i = 0; i < getList.length; i++) {
        var updateColID = '#' + getList[i].id;
        var iEquipmentID = getList[i].children[0].id;
        console.log(updateColID);
        console.log(iEquipmentID);
        if (iEquipmentID != '') {
            $(updateColID).load('AJAX/Data/' + iEquipmentID);
        }
    }
}

// 保存按钮
var saveData = function () {
    var getList = $$('dragslot').children;
    var saveList = [];
    for (var i = 0; i < getList.length; i++) {
        var sEquipmentNo = getList[i].children[0].id;
        if (sEquipmentNo.indexOf('待选择') == -1 && sEquipmentNo != '') {
            var liList = getList[i].children[0].children;
            for (var a = 1; a < liList.length; a++) {
                console.log(sEquipmentNo);
                var nHDRID = sEquipmentNo.split('_')[1];
                var tTime = GetDate();
                var id = liList[a].id.split('_')[1];
                var sCardNo = liList[a].children[0].children[0].children[0].innerText;
                var sDict = {
                    'id': id,
                    'nHDRID': nHDRID,
                    'sCardNo': sCardNo,
                    'nRowNumber': a,
                    'tUpdateTime': tTime,
                }
                saveList.push(sDict);
            }
        }
    }
    console.log(saveList);
    $.ajax({
        type: 'POST',
        url: 'AJAXPOST',
        data: JSON.stringify(saveList),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function (data) {
            alert('保存成功!!');
            updateCol();
        },
        error: function (data) {
            alert('保存失败!!');
        }
    });
}

// 机台中未有数据的写空机台
var addEmpty = function () {
    var lotList = $$('dragslot').children;
    for (var i = 0; i < lotList.length; i++) {
        var eachList = lotList[i].children[0].children;
        if (eachList.length < 2) {
            var ulObj = document.createElement("li");
            ulObj.className = 'slot-item li_style';
            ulObj.style = 'line-height: 80px;';
            ulObj.innerHTML = '<div><div><div><span>空机台</span></div></div></div>';
            $$('dragslot').children[i].children[0].appendChild(ulObj);
            ulObj = undefined;
        }
    }
}