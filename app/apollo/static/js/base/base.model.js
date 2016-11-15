(function($){

    'use strict';

    $.baseModel = {

        _dispatch: function(method, data, success, error) {
            var dispatcher = this;
            $.ajax({
                url: '/base/',
                type: method,
                data: JSON.stringify(data),
                dataType: 'json',
                headers: {
                    'X-CSRFToken': $.fn.getCookie('csrftoken')
                },
                success: function (response) {
                    if (response['status'] == 200) {
                        if (success) {
                            success(response['data']);
                        } else {
                            dispatcher._success(response['data']);
                        }
                    } else {
                        if (error) {
                            error(response['message']);
                        } else {
                            dispatcher._error(response['data']);
                        }
                    }
                },
                error: function(jqXHR) {
                    if (error) {
                        error(jqXHR.responseText);
                    } else {
                        dispatcher._error(jqXHR.responseText);
                    }
                }
            });
        },

        _success: function(data) {
            console.info(data);
        },

        _error: function(data) {
            $.fn.showError(message);
        },

        all: function(data, success, error) {
            this._dispatch('get', data, success, error);
        },

        create: function(data, success, error) {
            this._dispatch('post', data, success, error);
        },

        update: function(data, success, error) {
            this._dispatch('patch', data, success, error);
        },

        remove: function(data, success, error) {
            this._dispatch('delete', data, success, error);
        }
    };
})(jQuery);
