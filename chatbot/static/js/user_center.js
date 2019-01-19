function changePsw() {
    let old_psw = $("#old-psw").val();
    let psw1 = $("#new-psw1").val();
    let psw2 = $("#new-psw2").val();
    if (old_psw === "") {
        uperr("必须填写旧密码");
        return
    }
    if (psw1 === "") {
        uperr("必须填写密码");
        return
    }
    if (psw1 !== psw2) {
        uperr("两次输入密码不一致");
        return;
    }
    $.ajax({
        url: "changepsw",
        method: "POST",
        data: {
            csrfmiddlewaretoken: Cookies.get('csrftoken'),
            old_psw: old_psw,
            new_psw: psw1
        },
        dataType: 'json',
        success: function (response) {
            console.log(response);
            if (response.result === 'success') {
                $("#fail").hide();
                $("#success").show();
                Cookies.set('uid', response.uid);
                setTimeout(function () {
                    window.location.href='/';
                }, 2000);
            } else {
                $("#fail").html(response.msg).show();
            }
        },
        error: function (err) {
            let t = $("#fail");
            t.html("内部错误");
            t.show();
        }
    })
}

$(document).ready(function () {
    $("#upload-avatar").fileinput({
        language: 'zh',
        theme: 'fas',
        allowedFileExtensions: ['jpg', 'png', 'gif'],
        resizeImage: true,
        maxFileCount: 1,
        autoReplace: true,
        uploadUrl: 'uploadavatar',
        uploadExtraData: {csrfmiddlewaretoken: Cookies.get('csrftoken')}
    }).on('fileuploaded', function(event, data, previewId, index) {
        window.location.reload();
    });
});