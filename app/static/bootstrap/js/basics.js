// ClassName
var _$ = function (id) {
    return document.getElementsByClassName(id);
}

// ID
var $$ = function (id) {
    return document.getElementById(id);
}

// Name
var __$ = function (id) {
    return document.getElementsByName(id);
}

// 尺寸修改
var getScreen = function () {
    var nWidth = document.body.clientWidth;
    var nHeight = document.documentElement.clientHeight;
    var content = $$('body');

    $$('top-div').style.height = nHeight - 140 + 'px';
    // $$('bottom-div').style.height = (nHeight / 2) - 80 + 'px';
    $$('top-div').style.nWidth = nWidth + 'px';
    $$('dragslot').style.nWidth = nWidth + 'px';
    $$('dragslot').style.height = nHeight - 92 + 'px';

    content.style.width = nWidth + 'px';
    content.style.height = nHeight - 5 + 'px';
}

// 页面初始
window.onload = function () {
    getScreen();
    getCount();
}

// 修改屏幕尺寸后进行div的更新
window.onresize = function () {
    getScreen();
}

//刷新页面
var Refresh = function () {
    location.reload();
}