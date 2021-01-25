$(function () {
    $('.confirm-btn').click(function () {
        let isbn = $(this).parents('.item').data('id');
        window.location.href = '/wish/book/' + String(isbn) + '/redraw';
    })
});