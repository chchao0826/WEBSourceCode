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
    cal();
    getScreen();
    getCount();
}


$(document).ready(function(){ 
    getSesCookie();
});


// 修改屏幕尺寸后进行div的更新
window.onresize = function () {
    getScreen();
}

//刷新页面
var Refresh = function () {
    location.reload();
}


//获取当前时间
var getDateTime = function () {
    var myDate = new Date()
    var myDay = myDate.getDate();
    var myMonth = myDate.getMonth() + 1;
    var myYear = myDate.getFullYear();
    if (myDay.toString().length < 2) {
        myDay = 0 + myDay.toString();
    }
    if (myMonth.toString().length < 2) {
        myMonth = 0 + (myMonth + 1).toString();
    }
    var DataTime = myYear + '-' + myMonth + '-' + myDay;
    return DataTime
}