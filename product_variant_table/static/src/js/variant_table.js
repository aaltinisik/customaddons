// Copyright 2022 Yiğit Budak (https://github.com/yibudak)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

odoo.define('product_variant_table.variant_handle', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var VariantMixin = require('sale.VariantMixin');
    require('website_sale.website_sale');

    publicWidget.registry.VariantTableMixin = publicWidget.Widget.extend(VariantMixin, {
        selector: '.oe_website_sale',
        events: {
            'change input[name="product-variant-table-select"]': '_getCombinationInfoVariantTable'
        },

        /**
         * @constructor
         */
        init: function (parent) {
            this._super.apply(this, arguments);
        },

        start() {
            const def = this._super(...arguments);
            this._applyHash();
            this.$el.find('input[name="product-variant-table-select"]').trigger('change');

            return def;
            // this.$el.find('input[name="product-variant-table-select"]').trigger('change');
        },
        /**
         * @see onChangeVariant
         *
         * @private
         * @param {Event} ev
         * @returns {Deferred}
         */

        _setUrlHash: function ($parent) {
            var $attributes = $parent.find('input.form-check-input.product-select:checked');
            window.location.hash = 'attr=' + $attributes.attr('vals');
        },

        _applyHash: function () {
            var hash = window.location.hash.substring(1);
            if (hash) {
                var params = $.deparam(hash);
                if (params['attr']) {
                    var attributeIds = params['attr'].split(',');
                    var $inputs = this.$('input.form-check-input.product-select');
                    _.each(attributeIds, function (id) {
                        var $toSelect = $inputs.filter('[vals="' + id + '"]');
                        if ($toSelect.is('input[type="radio"]')) {
                            $toSelect.prop('checked', true);
                        } else if ($toSelect.is('option')) {
                            $toSelect.prop('selected', true);
                        }
                    });
                }
            }
        },

        _getCombinationInfoVariantTable: function (ev) {
            var selected_product_id = parseInt(ev.currentTarget.value);
            var parent = $('div.js_product.js_main_product.mb-3');
            return ajax.jsonRpc(this._getUri('/sale/get_combination_info_website'), 'call', {
                'product_template_id': parseInt($('.product_template_id').val()),
                'product_id': selected_product_id,
                'combination': [],
                'add_qty': parseInt($('input[name="add_qty"]').val()),
                'pricelist_id': this.pricelistId || false,
                // ...this._getOptionalCombinationInfoParam($parent),
            }).then((combinationData) => {
                this._onChangeCombination(ev, parent, combinationData);
                this._setUrlHash(parent);
                // this._checkExclusions(parent, [], combinationData.parent_exclusions);
            });
        },


    });


});
