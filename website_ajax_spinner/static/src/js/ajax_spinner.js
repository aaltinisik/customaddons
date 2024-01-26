odoo.define('your_module_name.loading_spinner', function (require) {
    'use strict';

    // Check if the current URL contains '/shop/confirmation'
    if (window.location.pathname.includes('/shop/confirmation')) {
        return;  // Exit the module early, doing nothing
    }

    var rpc = require('web.rpc');
    var AjaxService = require('web.AjaxService');
    var $loading_toast = $('.o_loading_toast');
    $loading_toast.hide();

    var rpcCounter = 0;

    var originalRpc = rpc.query;
    var originalAjaxRpc = AjaxService.prototype.rpc;

    rpc.query = function (options, kwargs) {
        rpcCounter++;

        if ($loading_toast.css('display') !== 'block') {
            $loading_toast.show();
        }

        var promise = originalRpc.apply(this, arguments);

        promise.finally(function () {
            rpcCounter--;

            if (rpcCounter === 0) {
                setTimeout(function () {
                    $loading_toast.hide();
                }, 300);
            }
        });

        return promise;
    };

    AjaxService.prototype.rpc = function (route, args) {
        rpcCounter++;

        if ($loading_toast.css('display') !== 'block') {
            $loading_toast.show();
        }

        var promise = originalAjaxRpc.apply(this, arguments);

        promise.finally(function () {
            rpcCounter--;

            if (rpcCounter === 0) {
                setTimeout(function () {
                    $loading_toast.hide();
                }, 300);
            }
        });

        return promise;
    };
});
