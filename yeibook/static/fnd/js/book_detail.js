$(function () {
    $('#confirmed').click(function () {
        let isbn = $('#isbn').val();
        window.location.href = '/gifts/book/' + isbn;
    });

    $('#wish-confirmed').click(function () {
        let isbn = $('#isbn').val();
        window.location.href = '/wish/book/' + isbn;
    });
});
