// 点击页码
function btnPage(sPageNumber){
    var sGetURL = window.location.href;
    var sList = sGetURL.split('/');
    var sInputValue = sList[sList.length - 1];
    var nPageNumber = sPageNumber.split('_')[1];
    console.log(nPageNumber);
    console.log(sInputValue);
    console.log(sPageNumber);
    clearActive(sPageNumber);
    var sUrlValue = sInputValue + '_' + nPageNumber;
    $$(sPageNumber).className = 'active'
    $('#choiceTable').load('Page/' + sUrlValue);
}

// 清空页码active的状态
function clearActive(sPageNumber){
    var schildList = $$(sPageNumber).parentNode.children;
    for (var i = 0; i < schildList.length; i++){
        var sChildClassName = schildList[i].className;
        if (sChildClassName.indexOf('active') != -1){
            schildList[i].className = '';
        }
    }
}
