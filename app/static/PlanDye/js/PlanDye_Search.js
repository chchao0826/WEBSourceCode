// 显示或隐藏标签 #完成
// var showORhidden = function (btnID, divID) {
//     // 按钮的文字选择
//     var choose = function (iFlag) {
//         if (iFlag != -1) {
//             if (btnID == 'showsRemark') {
//                 $$(btnID).innerHTML = '隐藏备注';
//             } else {
//                 $$(btnID).innerHTML = '隐藏搜索';
//             }
//         } else {
//             if (btnID == 'showsRemark') {
//                 $$(btnID).innerHTML = '显示备注';
//             } else {
//                 $$(btnID).innerHTML = '显示搜索';
//             }
//         }
//     }

//     var iFlag = $$(divID).className.indexOf('hidden');
//     if (iFlag != -1) {
//         // IsOpen();
//         $$(divID).className = 'panel-footer';
//         $$('main_var').style.marginTop = 180 + 'px';
//     } else {
//         $$(divID).className = 'panel-footer hidden';
//         $$('main_var').style.marginTop = 105 + 'px';
//     }
//     choose(iFlag);
// }

// 搜索后判断是否加载搜索的机台
// var findEqui = function (input_value) {
    // var sEquiListVal = $$('dragslot').children;
    // var bISNoneList = [];
    // for (var i = 0; i < sEquiListVal.length; i++) {
    //     if (sEquiListVal[i].children[0].id == '') {
    //         bISNoneList.push(sEquiListVal[i].id);
    //     }
    // }

    // $('#' + bISNoneList[0]).load('SearchUpdateEqui/' + input_value)
// }

// var innerRightEqui = function (input_value) {
//     var title3 = $$('title_3').children;
//     var nHdrList = []
//     for (var i = 0; i < title3.length; i++) {
//         var nHdrID = title3[i].id.split('_')[2];
//         nHdrList.push(nHdrID)
//     }
//     console.log(title3);
//     // $('#title_3').load('SearchUpdateRightEqui/' + input_value + '_' + nHdrList)
// }

// 清空搜索 完成
var ClearSearch = function () {
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        var childrenList = dragslotList[i].children[0].children;
        for (var a = 1; a < childrenList.length; a++) {
            document.documentElement.scrollTop = 0;
            var sClassName = childrenList[a].className;
            if (sClassName.indexOf('search_get') != -1) {
                childrenList[a].className = 'slot-item li_style'
                $$('search_value').innerHTML = ''
            }
        }
    }
}

// 得到搜索到的对应的height
var GetHeight = function (id) {
    var sCookieList = document.cookie.split(';');
    var nHeight = 660;
    for (var i = 0; i < sCookieList.length; i++) {
        var cookies = sCookieList[i].replace(/\s/ig, '');
        var spanName = 'split_span' + id;
        if (cookies.indexOf(spanName) != -1) {
            nHeight = cookies.split('=')[1];
        }
    }
    return nHeight;
}


// 页内搜索函数
var SearchMain = function (value, sList, sType, sEquipmentID) {
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
                iFlag =  ((a) * 110);
                break;
            }
        }
    }
    console.log(iFlag)
    return iFlag
}


// 页内搜索 #完成
var SearchPage = function (value) {
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
            SearchValueUpdate(sValue)
        }

    }
});

// 是否点击搜索按钮
var IsSearch = function () {
    var sValue = $$('searchValue').value;
    var iFlag = SearchPage(sValue);
    console.log(iFlag)
    console.log(sValue)
    console.log('============')
    if (iFlag == false) {
        // findEqui(sValue);
        // innerRightEqui(sValue)
        SearchValueUpdate(sValue)
    }

}

// 搜索结果中搜索资料更新
var SearchValueUpdate = function (inputValue) {
    $('#search_value').load('Search/' + inputValue)
}