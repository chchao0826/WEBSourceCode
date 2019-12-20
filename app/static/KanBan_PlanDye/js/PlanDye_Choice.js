// 从打开的新页面中得到回传的值
function ReturnValue() {
    var tableTr = $$('choiceTable').children[0].children;
    var sList = [];
    for (var i = 1; i < tableTr.length; i++) {
        var tdList = tableTr[i].children;
        var bIsTrue = tdList[5].children[0].checked;
        if (bIsTrue == true) {
            var sOrderNo = tdList[0].innerHTML;
            var sCardNo = tdList[1].innerHTML;
            var sMaterialNo = tdList[2].innerHTML;
            var sEquipmentNo = tdList[3].innerHTML;
            var ID = tdList[6].innerHTML;
            var nHDRID = tdList[7].innerHTML;
            var sDict = {
                'sOrderNo': sOrderNo,
                'sCardNo': sCardNo,
                'sMaterialNo': sMaterialNo,
                'sEquipmentNo': sEquipmentNo,
                'sEquipmentNo': sEquipmentNo,
                'ID': ID,
                'nHDRID': nHDRID,
            }
            console.log(sDict)
            sList.push(sDict);
            console.log(sList)
        }
    }
    return sList
}

// 关闭窗口
function closeWindow() {
    window.close();
}

// 由机台ID得到机台组别
function GetEquiModel(nHDRID) {
    var returnValue
    switch (nHDRID) {
        case 6:
        case 8:
        case 9:
        case 10:
        case 11:
            returnValue = 'A';
            break;
        case 12:
        case 13:
        case 14:
        case 15:
            returnValue = 'B';
            break;
        case 16:
        case 17:
        case 18:
        case 19:
        case 20:
        case 21:
            returnValue = 'C';
            break;
        case 22:
        case 23:
        case 24:
        case 25:
            returnValue = 'D';
            break;
        case 27:
        case 28:
        case 29:
        case 30:
        case 31:
        case 32:
            returnValue = 'E';
            break;
    }
    return returnValue
}


// 点击确认按钮
function btnConfirm() {
    var GetReturnValue = ReturnValue();
    var ModelList = []
    for (var i = 0; i < GetReturnValue.length; i++) {
        var nID = GetReturnValue[i]['ID'];
        var nHDRID = 'equ_' + GetReturnValue[i]['nHDRID'];
        var nIDVar = parseInt(GetReturnValue[i]['nHDRID']);
        var sModel = GetEquiModel(nIDVar);
        if (ModelList.indexOf(sModel) == -1) {
            ModelList.push(sModel);
            window.opener.SearchReturn(sModel, nHDRID, GetReturnValue);
        }
    }
    console.log(GetReturnValue);
    closeWindow();
}