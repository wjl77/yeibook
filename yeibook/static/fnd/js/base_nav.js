(function () {
    let url = window.location.pathname;
    // pc mobile
    if (url == '/my/gifts'){
        $('#gifts-nav').css({'color': 'purple'});
        $('#gifts-nav-mobile').css({'color': 'purple'});
    }

    if (url == '/my/wish'){
        $('#wishes-nav').css({'color': 'purple'});
        $('#wishes-nav-mobile').css({'color': 'purple'});
    }

    if (url == '/pending'){
        $('#pending-nav').css({'color': 'purple'});
        $('#pending-nav-mobile').css({'color': 'purple'});
    }

    if (url == '/login'){
        $('#login-nav').css({'color': 'purple'});
        $('#login-nav-mobile').css({'color': 'purple'});
    }

    if (url == '/register'){
        $('#register-nav').css({'color': 'purple'});
        $('#register-nav-mobile').css({'color': 'purple'});
    }
    // // mobile
    // if (url == '/my/gifts'){
    //     $('#gifts-nav-mobile').css({'color': 'purple'});
    // }
    //
    // if (url == '/my/wish'){
    //     $('#wishes-nav-mobile').css({'color': 'purple'});
    // }
    //
    // if (url == '/pending'){
    //     $('#pending-nav-mobile').css({'color': 'purple'});
    // }
    //
    // if (url == '/login'){
    //     $('#login-nav-mobile').css({'color': 'purple'});
    // }
    //
    // if (url == '/register'){
    //     $('#register-nav-mobile').css({'color': 'purple'});
    // }
})();