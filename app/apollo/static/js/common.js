(function($){

    'use strict';

    $.fn.getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    $.fn.registerHandlebarHelpers = function() {
        Handlebars.registerPartial('item', function(data) {
            var source = $('#t-item').html(),
                template = Handlebars.compile(source);
            return template(data);
        });
    };

    $.fn.renderTemplate = function(template_name, data) {
        var source   = $('#' + template_name).html(),
            template = Handlebars.compile(source);
        $(this).html(template(data));
    };

    $.fn.showError = function(message) {
        var dialog = $('#dialog');

        dialog.removeClass('hidden');
        dialog.find('.content').html(message);
        dialog.find('.close').on('click', function() {
            dialog.addClass('hidden');
        });
    };

})(jQuery);
