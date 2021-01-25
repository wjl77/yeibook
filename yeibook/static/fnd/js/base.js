$(function () {

    const realBox = $('#real-box');
    let result = null;
    let dataArr = null;
    let realList = [];
    let realIdx = 0;


    $('[data-toggle="tooltip"]').tooltip();

    $('#pc_search_btn').click(function () {
        if ($('.search').val().trim() === '') {
            return false;
        }
    });

    $('#mobile_search_btn').click(function () {
        if ($('.mobile_q').val().trim() === '') {
            return false;
        }
    });

    // $('#mobile-nav1 > a').click(function () {
    //     $('#mobile-nav1 > a').eq($(this).index()).css({'color': 'purple'})
    //         .siblings().css({'color': '#17A2B8'});
    // });

    // setInterval(function () {
    //     $.ajax({
    //         url: '/current/gifts',
    //         method: 'GET',
    //         complete: function (res) {
    //             result = res.responseJSON;
    //             if (result.code === 1) {
    //                 dataArr = result.data;
    //                 for (let i = 0; i < dataArr.length; i++) {
    //                     let str = dataArr[i]['nickname'] + '将《 ' + dataArr[i]['book_name'] + '》加入到了赠送清单';
    //                     realList.push(str);
    //                 }
    //                 realIdx = realList.length - 1;
    //             }
    //         }
    //     });
    // }, 30000);

    $.ajax({
        url: '/current/gifts',
        method: 'GET',
        complete: function (res) {
            result = res.responseJSON;
            if (result.code === 1) {
                dataArr = result.data;
                for (let i = 0; i < dataArr.length; i++) {
                    let str = dataArr[i]['nickname'] + '将《 ' + dataArr[i]['book_name'] + '》加入到了赠送清单';
                    realList.push(str);
                }
                realIdx = realList.length - 1;
            } else {
                realBox.html('暂无最新赠送信息');
            }
        }
    });

    // console.log(realList, typeof realList);

    setInterval(function () {
        // randomNum = parseInt(Math.random() * realList.length);
        realBox.html(realList[realIdx]);
        --realIdx;
        if (realIdx < 0) realIdx = realList.length - 1;
    }, 3000)
});