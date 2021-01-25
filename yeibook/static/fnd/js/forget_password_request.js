$(function () {
        const form = $('#request-password-form');
        const email = $('#id-email');
        const email_reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        let email_flag = false;

        email.blur(function () {
           if (email.val().trim() === '') {
               email_flag = false;
           } else if (!email_reg.test(email.val().trim())) {
               email_flag = false;
               $('.check-username').html('邮箱帐号格式错误');
           } else {
               email_flag = true;
           }
        });

        form.submit(function () {
            if (!email_flag) {
                return false;
            }
        })
});