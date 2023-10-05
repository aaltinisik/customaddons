// Copyright 2023 Yiğit Budak (https://github.com/yibudak)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

odoo.define('website_cart_multi_currency.website_sale_delivery', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    publicWidget.registry.websiteSaleDelivery.include({
        /**
         * We need to override this method to prevent the default behavior of
         * the website_sale_delivery module.
         * @override
         */
        _handleCarrierUpdateResult: function (result) {
            var $amountCurrency = $('#order_amount_total_currency .monetary_field');
            $amountCurrency.html(result.new_amount_total_company_currency);
            return this._super.apply(this, arguments);
        },

    });
});
