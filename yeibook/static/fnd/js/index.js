$(function () {
    let page = 1;
    let books = $('#books');
    let html = null;
    const more = $('#more');
    const recent_url = $('#recent-url').val();

    $('#end-notice').hide();

    $.get(recent_url, {page: page}, function (res) {

        if (!res.data) {
            books.html('<span style="font-size: 12px">暂无最近赠书</span>');
            more.css({'display': 'none'});
        } else {
            html = $(res.data);
            books.append(html);
        }
    });

    $('#load_more').click(function () {
        page += 1;

        $.get(recent_url, {page: page}, function (res) {
            if (!res.data) {
                more.css({'display': 'none'});
                $('#end-notice').show();
            } else {
                html = $(res.data);
                books.append(html);
            }
        })
    })
});