function openerp_picking_order_widgets(instance){
    var module = instance.stock;
    var _t     = instance.web._t;
    var QWeb   = instance.web.qweb;
    module.PickingMainWidget.include({
        set_package_pack: function(package_id, pack,width,height,length,net_weight,gross_weight){
            var self = this;
                return new instance.web.Model('stock.quant.package')
                    .call('write',[[package_id],{'ul_id': pack ,'width':width,'height':height,'length':length,'net_weight':net_weight,'gross_weight':gross_weight}]);
        },
    });
    module.PickingEditorWidget.include({
        get_pack_data: function(pack_id){              
            return new instance.web.Model('stock.quant.package').call('search_read',[ [['id', '=', pack_id]], ['pack','width','height','length','net_weight','gross_weight'] ], {context: new instance.web.CompoundContext()}).done(function(pack_datas){
                    $('#width').attr('value',pack_datas[0].width);
                    $('#height').attr('value',pack_datas[0].height);
                    $('#length').attr('value',pack_datas[0].length);
                    $('#net_weight').attr('value',pack_datas[0].net_weight);
                    $('#gross_weight').attr('value',pack_datas[0].gross_weight);
            });
        },
        get_logisticunit: function(){
            var model = this.getParent();
            var ul = [];
            var self = this;
            _.each(model.uls, function(ulog){
                ul.push({name: ulog.name, id: ulog.id, width: ulog.width, height: ulog.height, length: ulog.length,});
            });
            return ul;
        },
        get_rows: function(){
            var model = this.getParent();
            this.rows = [];
            var self = this;
            var pack_created = [];
            _.each( model.packoplines, function(packopline){
                    var pack = undefined;
                    var color = "";
                    if (packopline.product_id[1] !== undefined){ pack = packopline.package_id[1];}
                    if (packopline.product_qty == packopline.qty_done){ color = "success "; }
                    if (packopline.product_qty < packopline.qty_done){ color = "danger "; }
                    //also check that we don't have a line already existing for that package
                    if (packopline.result_package_id[1] !== undefined && $.inArray(packopline.result_package_id[0], pack_created) === -1){
                        var myPackage = $.grep(model.packages, function(e){ return e.id == packopline.result_package_id[0]; })[0];
                        self.rows.push({
                            cols: { product: packopline.result_package_id[1],
                                    qty: '',
                                    rem: '',
                                    uom: undefined,
                                    lot: undefined,
                                    pack: undefined,
                                    container: packopline.result_package_id[1],
                                    container_id: undefined,
                                    loc: packopline.location_id[1],
                                    dest: packopline.location_dest_id[1],
                                    id: packopline.result_package_id[0],
                                    product_id: undefined,
                                    can_scan: false,
                                    head_container: true,
                                    processed: packopline.processed,
                                    package_id: myPackage.id,
                                    ul_id: myPackage.ul_id[0],
                            },
                            classes: ('success container_head ') + (packopline.processed === "true" ? 'processed hidden ':''),
                        });
                        pack_created.push(packopline.result_package_id[0]);
                    }
                    self.rows.push({
                        cols: { product: packopline.product_id[1] || packopline.package_id[1],
                                qty: packopline.product_qty,
                                rem: packopline.qty_done,
                                uom: packopline.product_uom_id[1],
                                lot: packopline.lot_id[1],
                                pack: pack,
                                container: packopline.result_package_id[1],
                                container_id: packopline.result_package_id[0],
                                loc: packopline.location_id[1],
                                dest: packopline.location_dest_id[1],
                                id: packopline.id,
                                product_id: packopline.product_id[0],
                                can_scan: packopline.result_package_id[1] === undefined ? true : false,
                                head_container: false,
                                processed: packopline.processed,
                                package_id: undefined,
                                ul_id: -1,
                        },
                        classes: color + (packopline.processed === "true" ? 'processed hidden ':''),
                    });
            });
            //sort element by things to do, then things done, then grouped by packages
            group_by_container = _.groupBy(self.rows, function(row){
                return row.cols.container;
            });
            var sorted_row = [];
            if (group_by_container.undefined !== undefined){
                group_by_container.undefined.sort(function(a,b){return (b.classes === '') - (a.classes === '');});
                $.each(group_by_container.undefined, function(key, value){
                    sorted_row.push(value);
                });
            }

            $.each(group_by_container, function(key, value){
                if (key !== 'undefined'){
                    $.each(value, function(k,v){
                        sorted_row.push(v);
                    });
                }
            });

            return sorted_row;
        },
        renderElement: function(){            
            var self = this;
            this._super();
            self.get_partner();
            self.$('#js_packconf_select').change(function(){
                var ul_id = self.$('#js_packconf_select option:selected').data('ul-id');
                var width = self.$('#js_packconf_select option:selected').attr('width');
                var height = self.$('#js_packconf_select option:selected').attr('height');
                var length = self.$('#js_packconf_select option:selected').attr('length');
                self.$('.o_pack_data #width').val(width);
                self.$('.o_pack_data #height').val(height);
                self.$('.o_pack_data #length').val(length);

            });
            this.$('.js_validate_pack').click(function(){
                //get current selection
                var select_dom_element = self.$('#js_packconf_select');
                var ul_id = self.$('#js_packconf_select option:selected').data('ul-id');
                var width = self.$('#width').val();
                var length = self.$('#length').val();
                var net_weight = self.$('#net_weight').val();
                var gross_weight = self.$('#gross_weight').val();
                var height = self.$('#height').val();    
                var current_url = $('#current_url').val();
                var pack_id = select_dom_element.data('pack-id');
                self.$el.siblings('#js_PackConfModal').modal('hide');
                if (pack_id){
                    self.getParent().set_package_pack(pack_id, ul_id,width,height,length,net_weight,gross_weight).then(function(){
                        $('.container_head[data-package-id="'+pack_id+'"]').data('ulid', ul_id);    
                        self.getParent().refresh_ui(self.getParent().picking.id);
                    });
                }
            });
            this.$('.js_pack_configure').click(function(){
                var pack_id = $(this).parents(".js_pack_op_line:first").data('package-id');
                var ul_id = $(this).parents(".js_pack_op_line:first").data('ulid');
                self.$('#current_url').attr('value',window.location.href);
                self.get_pack_data(pack_id);
                self.$('#js_packconf_select').val(ul_id);
                self.$('#js_packconf_select').data('pack-id',pack_id);
                self.$el.siblings('#js_PackConfModal').modal();
            });
        },
        get_partner: function(){              
            return new instance.web.Model('res.partner').call('search_read',[ [['id', '=', this.getParent().picking.partner_id[0]]], ['name','street','street2','city','state_id','country_id', 'zip'] ], {context: new instance.web.CompoundContext()}).done(function(pickings){
                    var street = pickings[0].street
                    var street2 = pickings[0].street2
                    var city = pickings[0].city
                    var state = pickings[0].state_id 
                    var zip = pickings[0].zip
                    var partner_string = pickings[0].name
                    $('.oe_pick_app_partner').append((pickings[0].name ? $('<h5>', {
                        'class': 'o_partner_name'
                    }).text(pickings[0].name + ',') : '')).append((pickings[0].street ? $('<h5>', {
                        'class': 'o_partner_street'
                    }).text(pickings[0].street + ',') : '')).append((pickings[0].street2 ? $('<h5>', {
                        'class': 'o_partner_street2'
                    }).text(pickings[0].street2 + ',') : '')).append((pickings[0].city ? $('<h5>', {
                        'class': 'o_partner_city',
                    }).text(pickings[0].city + ', ') : '')).append((pickings[0].state_id[1] ? $('<h5>', {
                        'class': 'o_partner_state',
                    }).text(pickings[0].state_id[1] + ', ') : '')).append((pickings[0].zip ? $('<h5>', {
                        'class': 'o_partner_zip',
                    }).text(pickings[0].zip + ',') : '')).append((pickings[0].country_id[1] ? $('<h5>', {
                        'class': 'o_partner_country'
                    }).text(pickings[0].country_id[1]) : ''));
            });
        },
    });
}

openerp.warehouse_barcode_interface = function(openerp) {
    openerp.warehouse_barcode_interface = openerp.warehouse_barcode_interface || {};
    openerp_picking_order_widgets(openerp);
}