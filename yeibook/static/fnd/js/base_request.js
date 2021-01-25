$(function () {
    const right_url = $('#right-url').val();
    const right_menus = $('#right-menus');

    $.ajax({
        url: right_url,
        method: 'GET',
        complete: function (res) {
            let html = $(res.responseJSON.data);
            right_menus.append(html);
        }
    })
})