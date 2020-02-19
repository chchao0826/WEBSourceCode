function findBrowser() {
    var iFlag = false;
    var fso, filespec;
    filespec = 'C:/Progra~1/Mozill~1/firefox.exe';
    fso = new ActiveXObject("Scripting.FileSystemObject");
    if (fso.FileExists(filespec) == false) {
        // alert('无法打开, 请联系资讯部门安装浏览器!!');
        iFlag = true;
    }
    return iFlag
}


var openNewWindow = function (sUrl) {
    function start(strPath) {
        var objShell = new ActiveXObject("wscript.shell");
        var cmd = "cmd /c start C:/Progra~1/Mozill~1/firefox " + sUrl;
        var f = objShell.Run(cmd, 0);
        objShell = null;

    }
    start("C:/Progra~1/Mozill~1/firefox"); //应用程序路径
}