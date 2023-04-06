// Copyright 2023 Yiğit Budak (https://github.com/yibudak)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

odoo.define('product_qty_increment_step.qty_step', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var VariantMixin = require('sale.VariantMixin');
    var WebsiteSale = require('website_sale.website_sale');

    /*
        * We need to override this method to prevent the default behavior of
        * the website_sale module.
     */
    VariantMixin.onClickAddCartJSON = function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $incrementSize = $link.closest('.input-group').find("span[data-increment-step]").data("increment-step");
        var $input = $link.closest('.input-group').find("input");

        var max = parseFloat($input.data("max") || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = ($link.has(".fa-minus").length ? -$incrementSize : $incrementSize) + previousQty;
        var newQty = quantity > $incrementSize ? (quantity < max ? quantity : max) : $incrementSize;

        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    };

    publicWidget.registry.QtyIncrementStep = publicWidget.Widget.extend(VariantMixin, WebsiteSale, {
        selector: '.oe_website_sale',
        events: {
            'change form .js_product:first input[name="add_qty"]': '_formatQtyWithStep',
        },

        /**
         * @constructor
         */
        init: function ($parent) {
            this._super.apply(this, arguments);
        },

        start() {
            return this._super(...arguments);
        },

        _formatQtyWithStep: function (ev) {
            // Format the quantity with the increment step value.
            // Example: If the increment step is 50, the quantity will be 50, 100, 150, etc.
            // If the quantity is 75, it will be rounded to 100.
            const $input = $(ev.currentTarget);
            const $incrementSize = $input.closest('.input-group').find("span[data-increment-step]").data("increment-step");
            let qty = parseInt($input.val(), 10); // Parse input value to integer

            qty = isNaN(qty) ? $incrementSize : qty;

            const remainder = qty % $incrementSize;
            if (remainder !== 0) {
                // Round up to the nearest increment step value
                qty += $incrementSize - remainder;
            }

            $input.val(qty); // Update input value to formatted quantity
        }

    });

});
