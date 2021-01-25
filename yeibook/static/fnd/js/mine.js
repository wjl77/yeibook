$(function () {
    let file = null;
    let fileFormat = null;
    let fileSize = null;

    $('.msg').html('');

    $('input[type="file"]').change(function () {
        const reader = new FileReader();
        file = this.files[0];

        if (file) {
            fileFormat = file.name.split('.').slice(-1)[0];
            fileSize = file.size;
            if (fileFormat.indexOf('jpeg') >= 0 || fileFormat.indexOf('jpg') >= 0 || fileFormat.indexOf('png') >= 0  || fileFormat.indexOf('gif') >= 0) {
                if (fileSize > 1000000) {
                    $('.msg').html('错误，大小超过1M');
                    file = null;
                    return false;
                }
                $('.msg').html('');
            } else {
                $('.msg').html('必须是jpeg/jpg/png/gif的格式');
                file = null;
                return false;
            }

            $('.display-avatar').html('');
            reader.onload = function () {
                $('.display-avatar').css({'background-image': 'url(' + reader.result + ')'});
            };
            reader.readAsDataURL(file);
        } else {
            file = null;
        }
    });

    $('#avatar-form').submit(function () {
        if (file === null) {
            return false;
        }
    });
});