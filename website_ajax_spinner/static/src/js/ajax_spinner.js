odoo.define('your_module_name.loading_spinner', function(require) {
    'use strict';

    var rpc = require('web.rpc');
    var AjaxService = require('web.AjaxService');
    var $spinner = $('#spinner');
    $spinner.hide();

    var rpcCounter = 0;

    var originalRpc = rpc.query;
    var originalAjaxRpc = AjaxService.prototype.rpc;

    rpc.query = function(options, kwargs) {
        rpcCounter++;

        if ($spinner.css('display') !== 'block') {
            $spinner.show();
        }

        var promise = originalRpc.apply(this, arguments);

        promise.finally(function() {
            rpcCounter--;

            if (rpcCounter === 0) {
                setTimeout(function() {
                    $spinner.hide();
                }, 300);
            }
        });

        return promise;
    };

    AjaxService.prototype.rpc = function(route, args) {
        rpcCounter++;

        if ($spinner.css('display') !== 'block') {
            $spinner.show();
        }

        var promise = originalAjaxRpc.apply(this, arguments);

        promise.finally(function() {
            rpcCounter--;

            if (rpcCounter === 0) {
                setTimeout(function() {
                    $spinner.hide();
                }, 300);
            }
        });

        return promise;
    };
});
