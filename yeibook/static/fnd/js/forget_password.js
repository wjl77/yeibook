$(function () {
        const reset_password_form = $('#reset-password-form');
        const password1 = $('#id-password1');
        const password2 = $('#id-password2');
        let password_flag = false;
        let confirm_password_flag = false;


        password1.blur(function () {
            if ($(this).val().trim() === '') {
                password_flag = false;
            } else if ($(this).val().trim().length < 6) {
                $('.check-password').html('密码至少需要6位喔');
                password_flag = false;
            } else {
                $('.check-password').html('');
                password_flag = true;
            }
        });

        password2.blur(function () {
            if ($(this).val() !== password1.val()) {
                $('.check-confirm-password').html('两次密码不同');
                password_flag = false;
                confirm_password_flag = false;
            } else {
                $('.check-confirm-password').html('');
                password_flag = true;
                confirm_password_flag = true;
            }
        });

        reset_password_form.submit(function () {
            if (!password_flag || !confirm_password_flag) {
                return false;
            }
        })
});