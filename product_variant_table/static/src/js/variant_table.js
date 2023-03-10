// Copyright 2022 Yiğit Budak (https://github.com/yibudak)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

odoo.define('product_variant_table.variant_handle', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var VariantMixin = require('sale.VariantMixin');
    var WebsiteSale = require('website_sale.website_sale');

    publicWidget.registry.WebsiteSale.include({
        /**
         * We need to override this method to prevent the default behavior of
         * the website_sale module.
         * @override
         */
        triggerVariantChange: function () {
            return true;
        },

    });

    publicWidget.registry.VariantTableMixin = publicWidget.Widget.extend(VariantMixin, WebsiteSale, {
        selector: '.oe_website_sale',
        events: {
            'change input[name="product-variant-table-select"]': '_getCombinationInfoVariantTable',
            'change form .js_product:first input[name="add_qty"]': '_getCombinationInfoVariantTable',
            'change select#special-attr-selector': '_getCombinationInfoVariantTable',
        },

        /**
         * @constructor
         */
        init: function ($parent) {
            this._super.apply(this, arguments);
        },

        start() {
            const def = this._super(...arguments);
            let $parent = this.$el;
            if ($parent.find("#product_variants_table").length > 0) {
                this._applyHash();
                this.$el.find('input[name="product-variant-table-select"]:checked').trigger('change');

            } else {
                $parent.find('form .js_product:first input[name="add_qty"]').trigger('change');
            }
            return def;
        },
        /**
         * @see onChangeVariant
         *
         * @private
         * @param {Event} ev
         * @returns {Deferred}
         */

        _setUrlHash: function ($parent) {
            var $attributes = $parent.find('input[name="product-variant-table-select"]:checked');
            var $attribute_container = $parent.find('div.attribute_container');
            var $specialAttrSelector = $parent.find('#special-attr-selector');
            $attribute_container.empty();
            var vals = $attributes.attr('vals');
            $.each(vals.split(","), function (index, value) {
                $("<input/>").attr({
                    'value_id': value,
                    'type': 'checkbox',
                    'class': 'js_variant_change d-none',
                    'checked': 'checked',
                }).val(value).appendTo($attribute_container);
            });
            if ($specialAttrSelector.length > 0) {
                $("<input/>").attr({
                    'value_id': $specialAttrSelector.val(),
                    'type': 'checkbox',
                    'class': 'js_variant_change d-none',
                    'checked': 'checked',
                }).val($specialAttrSelector.val()).appendTo($attribute_container);
                if (vals) {
                    vals += ',' + $specialAttrSelector.val();
                }
            }

            window.location.hash = 'attr=' + vals;
        },

        _applyHash: function () {
            var hash = window.location.hash.substring(1);
            if (hash) {
                var params = $.deparam(hash);
                if (params['attr']) {
                    var attributeIds = params['attr'];
                    var selectedInput = this.$('input[name="product-variant-table-select"][vals="' + attributeIds + '"]')
                    if (selectedInput) {
                        selectedInput.prop('checked', true);
                    }
                    var specialAttrSelector = this.$('#special-attr-selector');
                    if (specialAttrSelector.length > 0) {
                        var specialAttrId = attributeIds.split(',').pop();
                        specialAttrSelector.val(specialAttrId);
                    }

                }
            }
        },

        _renderPricelistTable: function ($parent, combinationData) {

            return ajax.jsonRpc(this._getUri('/sale/get_combination_pricelist_info'), 'call', {
                'product_id': combinationData.product_id,
            }).then((pricelistTable) => {
                if (pricelistTable.table_html) {
                    $parent.find('.js_pricelist_table').html(pricelistTable.table_html);
                }

            });
        },


        _updateProductImage: function ($productContainer, displayImage, productId, productTemplateId) {
            /**
             * Since we don't use specific product images for each combination,
             * no need to update the product image.
             * @override
             */
            return true;
        },

        _getCombinationInfoVariantTable: function (ev) {
            var $parent = $('div.js_product.js_main_product.mb-3');
            let $combination_el;
            var combinationArray = [];
            var productId = false;
            var $specialAttrSelector = this.$el.find('#special-attr-selector');

            if ($parent.find("#product_variants_table").length > 0) {
                // If product has combinations
                // We need this if-else because we're overriding the default
                // behavior of the website_sale module.
                $combination_el = this.$el.find('input[name="product-variant-table-select"]:checked');
                combinationArray = $combination_el.attr('vals').split(',').map((str) => Number(str));
                if ($specialAttrSelector.length > 0) {
                    combinationArray.push(Number($specialAttrSelector.val()));
                }
            } else {
                productId = parseInt($parent.find('input[name="product_id"]').val());
            }

            return ajax.jsonRpc(this._getUri('/sale/get_combination_info_website'), 'call', {
                'product_template_id': parseInt($('.product_template_id').val()),
                'product_id': productId,
                'parent_combination': [],
                'combination': combinationArray,
                'add_qty': parseInt($('input[name="add_qty"]').val()),
                'pricelist_id': this.pricelistId || false,
            }).then((combinationData) => {
                this._onChangeCombination(ev, $parent, combinationData);
                if (combinationArray.length > 0) {
                    this._setUrlHash($parent);
                }
                if (combinationData.is_combination_possible) {
                    this._renderPricelistTable($parent, combinationData);
                } else {
                    $parent.find('.js_pricelist_table').html('');
                }
            });
        },
    });
});
