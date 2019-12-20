// 清空按钮
function clearSearch() {
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        var sEqID = dragslotList[i].children[0].id;
        if (sEqID.indexOf('Eq') != -1) {
            var sectionList = dragslotList[i].children[0].children;
            for (var a = 1; a < sectionList.length; a++) {
                var secClass = sectionList[a].className;
                if (secClass.indexOf('search_get') != -1)
                    sectionList[a].className = 'slot-item li_style';
            }
        }
    }
}


// 页内搜索
function SearchPage(inputValue) {
    var bIsFind = false;
    var dragslotList = $$('dragslot').children;
    for (var i = 0; i < dragslotList.length; i++) {
        var sEqID = dragslotList[i].children[0].id;
        if (sEqID.indexOf('Eq') != -1) {
            var sectionList = dragslotList[i].children[0].children;
            for (var a = 1; a < sectionList.length; a++) {
                var sOrderNo = sectionList[a].children[1].children[0].children[0].children[0].innerHTML;
                var sCardNo = sectionList[a].children[1].children[0].children[1].children[0].innerHTML;
                var sMaterialNo = sectionList[a].children[1].children[0].children[2].children[0].innerHTML;
                if (sOrderNo.indexOf(inputValue) != -1 ||
                    sCardNo.indexOf(inputValue) != -1 ||
                    sMaterialNo.indexOf(inputValue) != -1) {
                    bIsFind = true;
                    sectionList[a].className += ' search_get';
                }
            }
        }
    }
    return bIsFind;
};


// 数据库搜索
function SearchDataBase(inputValue) {
    OpenChoice(inputValue);

}

// 打开窗口
function OpenChoice(inputValue) {
    var new_url = 'sale/Search/' + inputValue;
    window.open(new_url, 'newindow', 'height=600,width=900,top=0,left=0,toolbar=no,menubar=no,scrollbars=no,resizable=no,location=no,status=no');
}


// 搜索主程序
function search_Main() {
    var inputValue = $$('searchValue').value;
    var bIsFind = SearchPage(inputValue);
    if (bIsFind == false) {
        SearchDataBase(inputValue);
    };
};


// 搜索按钮
function Search() {
    search_Main();
}

// 搜索返回后执行的函数
function SearchReturn(sModel, nHDRID, nIDList) {

    function SearchPageReturn (nIDList){
        for(var i = 0; i < nIDList.length; i++){
            var sCardNo = nIDList[i]['sCardNo'];
            console.log(sCardNo)
            SearchPage(sCardNo)
        }
    }

    btnEquiModel(sModel);
    console.log('-======1221212========121')
    console.log(nIDList)
    var t = setTimeout(function () {
        btnEqui(nHDRID);
        var s = setTimeout(function () {
            SearchPageReturn(nIDList);
        }, 3000);

    }, 3000);


}
