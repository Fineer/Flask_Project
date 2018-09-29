function withdraw_course(cid) {
    if (confirm("确认退课？")) {
        $.post("/student_withdraw_course/", {
            course_id: cid
        }, function (data) {
            location.reload();
        });
    }
}

function choose_course(cid) {
    if (confirm("确认选课？")) {
        $.post("/student_choose_course/", {
            course_id: cid
        }, function (data) {
            location.reload();
        });
    }
}