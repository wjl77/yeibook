$(function () {
    // 撤销按钮
    $('.redraw-btn', document).click(function () {
        let did = $(this).parents('.drift-item').data('id');
        // console.log(did);
        window.location.href = '/drift/' + String(did) + '/redraw';
    });
    // 已邮寄
    $('.mailed-btn', document).click(function () {
        let did = $(this).parents('.drift-item').data('id');
        // console.log(did);
        window.location.href = '/drift/' + did + '/mailed';
    });
    // 据绝
    $('.deny-btn', document).click(function () {
        let did = $(this).parents('.drift-item').data('id');
        // console.log(did);
        window.location.href = '/drift/' + did + '/reject';
    });
});
