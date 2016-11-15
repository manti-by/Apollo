(function($){

    'use strict';

    $(document).ready(function () {
        // Init shot view
        $.baseView.init();

        // Handlebars
        $.fn.registerHandlebarHelpers();
    });
})(jQuery);
