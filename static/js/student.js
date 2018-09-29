function modify_my_infos() {
    var phonee = document.getElementById("my_phone");
    var pwde = document.getElementById("my_pwd");
    $.post("/student_modify/", {
        mphone: phonee.value,
        mpwd: pwde.value
    }, function (data) {
        location.reload();
    });
}