 odoo.define('badge_on_menu', function (require) {
    'use strict';
    var AppsMenu = require('web.AppsMenu');
    var Menu = require('web.Menu');
    var core = require('web.core');
    var QWeb = core.qweb;
    var session = require('web.session');

    Menu.include({
        start: function () {
              var self = this;

                this.$menu_apps = this.$('.o_menu_apps');
                this.$menu_brand_placeholder = this.$('.o_menu_brand');
                this.$section_placeholder = this.$('.o_menu_sections');

                // Navbar's menus event handlers
                var on_secondary_menu_click = function (ev) {
                    ev.preventDefault();
                    var menu_id = $(ev.currentTarget).data('menu');
                    var action_id = $(ev.currentTarget).data('action-id');
                    var menu_obj = $('.o_menu_sections').find('.o_menu_entry_lvl_2');
                    var on_load_badge = function (menu_id) {
                            var self = this;
                            var badge_count = $('[id=menu_counter]')
                            if (badge_count.length > 0){
                                $('[id=menu_counter]').remove();
                            }

                            var isEnterprise = odoo.session_info.server_version_info[5] === 'e';
                            if (isEnterprise){
                                var $menu_item = $('.o_apps').find('a[data-menu="' + item['id'] +'"]')
                            }else{
                                var $menu_item = $('.o_menu_sections').find('a[data-menu="' + menu_id +'"]').find('span')
                            }
                            var postData = new FormData();
                            postData.append("menu_id", menu_id);
                            if (core.csrf_token) {
                                postData.append('csrf_token', core.csrf_token);
                            }
                            var def = $.ajax({
                                type: "POST",
                                dataType: 'json',
                                url: '/get_badge_count',
                                cache: false,
                                contentType: false,
                                processData: false,
                                data: postData,
                            }).then(function (count) {
                                $menu_item.append(QWeb.render("badge_on_menu_counter", {widget: count}));
                            });
                        }
                    menu_obj.each(function(a) {
                        on_load_badge($( this ).attr("data-menu"));
                    })

                };
                var menu_ids = _.keys(this.$menu_sections);
                var primary_menu_id, $section;
                for (var i = 0; i < menu_ids.length; i++) {
                    primary_menu_id = menu_ids[i];
                    $section = this.$menu_sections[primary_menu_id];
                    $section.on('click', 'a[data-menu-xmlid]', self, on_secondary_menu_click.bind(this));
                }
                return this._super.apply(this, arguments);
        },
    });
    return {
        'Menu': Menu,
    };
});
