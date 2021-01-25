const login_form = $('#login-form');
const email = $('#id-email');
const password = $('#id-password');
const email_reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
let email_flag = false;
let password_flag = false;

email.blur(function () {
    let _this = $(this);
    if (_this.val().trim() === '') {
        $('.check-username').html('用户名不得为空');
        email_flag = false;
    } else if (!email_reg.test(_this.val())) {
        $('.check-username').html('邮箱帐号格式错误');
        email_flag = false;
    } else {
        $('.check-username').html('');
        email_flag = true;
    }
});

password.blur(function () {
    let _this = $(this);
    if (_this.val().trim() === '') {
        $('.check-password').html('密码不得为空');
        password_flag = false;
    } else if (_this.val().trim().length < 6) {
        $('.check-password').html('密码至少需要6位喔');
        password_flag = false;
    } else {
        $('.check-password').html('');
        password_flag = true;
    }
});


// email.focus(function () {
//     $('.check-username').html('');
// });
//
// password.focus(function () {
//     $('.check-password').html('');
// });

login_form.submit(function () {
    if (!email_flag && !password_flag) {
        // $('.check-password').html('帐号或密码不得为空');
        return false;
    } else if (email.val().trim() === '' || !email_reg.test(email.val().trim())) {
        $('.check-username').html('邮箱帐号格式错误');
        return false;
    } else if (password.val().trim() === '' || password.val().trim().length < 6) {
        $('.check-password').html('密码至少需要6位喔');
        return false
    }
    return true;
});