(function ($) {
    let $content_md = $('#div_id_content_md');
    let $content_ck = $('#div_id_content_ck');
    let $is_md = $('input[name=is_md]');
    let switch_editor = function (is_md) {
        if (is_md) {
            $content_md.show();
            $content_ck.hide();
        }else {
            $content_md.hide();
            $content_ck.show();
        }
    }
    $is_md.on('click', function () {
        switch_editor($(this).is(':checked'));
    });
    switch_editor($is_md.is(':checked'));
})(jQuery);
