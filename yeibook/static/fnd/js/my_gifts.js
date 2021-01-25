$(function () {
    $('.confirm-btn').click(function () {
        let did = $(this).parents('.item').data('id');
        window.location.href = '/gifts/' + String(did) + '/redraw';
    })
});