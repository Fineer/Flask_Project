function submit_change(mail, where) {
    var eles = document.getElementsByClassName(mail);
    var go = 0;
    if (eles.length > 5 && where > 0) {
        go = 5;
    }

    var mmail = eles[0 + go];
    var mname = eles[1 + go];
    var mphone = eles[2 + go];
    var mpwd = eles[3 + go];
    var mprivilege = eles[4 + go];

    $.post("/admin_modify/", {
        mmail: mmail.value,
        mname: mname.value,
        mphone: mphone.value,
        mpwd: mpwd.value,
        mprivilege: mprivilege.value,
        who: where
    }, function (data) {
        location.reload();
    });
    location.reload();
}

function buy_info_service() {
    if (confirm("确认购买信息管理系统？")) {
        $.post("/buy_info_service/", {}, function (data) {
            location.reload();
        });
    }
    location.reload();
}

function buy_course_service() {
    if (confirm("确认购买课程管理系统？")) {
        $.post("/buy_course_service/", {}, function (data) {
            location.reload();
        });
    }
    location.reload();
}

function buy_score_service() {
    if (confirm("确认购买成绩管理系统？")) {
        $.post("/buy_score_service/", {}, function (data) {
            location.reload();
        });
    }
    location.reload();
}
