function modify_my_pp() {
    var pn = document.getElementById("my_phone_t").value;
    var pw = document.getElementById("my_pwd_t").value;

    $.post("/teacher_modify/", {
        mphone: pn,
        mpwd: pw
    }, function (data) {
        location.reload();
    });
}