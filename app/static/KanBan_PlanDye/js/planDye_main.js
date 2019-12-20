// 增加机台的同时,下方数据列进行AJAX更新
var addData = function (ID) {
    var sectionList = $$('dragslot').children;
    for (var i = 0; i < sectionList.length; i++) {
        var varID = '#' + sectionList[i].id;
        if (sectionList[i].children[0].id == '' && sectionList[i].children[0].id.indexOf('-') == -1) {
            $(varID).load('AJAX/Data/' + ID);
            break;
        }
    }
}