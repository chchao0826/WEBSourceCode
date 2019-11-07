
// 获取时间
var GetDate = function () {
    var day2 = new Date();
    var sYear = day2.getFullYear();
    var sMonth = day2.getMonth() + 1;
    var sDate = day2.getDate();
    var sHour = day2.getHours();
    var sMin = day2.getMinutes();
    var sSec = day2.getSeconds();
    if ((sMonth.toString().length) == 1) {
        sMonth = '0' + sMonth.toString()
    }
    if ((sDate.toString().length) == 1) {
        sDate = '0' + sDate.toString()
    }
    if ((sHour.toString().length) == 1) {
        sHour = '0' + sHour.toString()
    }
    if ((sMin.toString().length) == 1) {
        sMin = '0' + sMin.toString()
    }
    if ((sDate.toString().length) == 1) {
        sSec = '0' + sSec.toString()
    }
    var dateTime = sYear + "-" + sMonth + "-" + sDate + ' ' + sHour + ':' + sMin + ':' + sSec;
    return dateTime
}