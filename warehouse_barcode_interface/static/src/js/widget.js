function openerp_picking_order_widgets(instance){
    var module = instance.stock;
    var _t     = instance.web._t;
    var QWeb   = instance.web.qweb;
    
    module.PickingMenuWidget.include({
    	load: function(){
            var self = this;
            return new instance.web.Model('stock.picking.type').get_func('search_read')([],[])
                .then(function(types){
                    self.picking_types = types;
                    type_ids = [];
                    for(var i = 0; i < types.length; i++){
                        self.pickings_by_type[types[i].id] = [];
                        type_ids.push(types[i].id);
                    }
                    self.pickings_by_type[0] = [];

                    return new instance.web.Model('stock.picking').call('search_read',[ [['state','in', ['confirmed','assigned', 'partially_available']], ['picking_type_id', 'in', type_ids]], [] ], {context: new instance.web.CompoundContext()});

                }).then(function(pickings){
                    self.pickings = pickings;
                    for(var i = 0; i < pickings.length; i++){
                        var picking = pickings[i];
                        self.pickings_by_type[picking.picking_type_id[0]].push(picking);
                        self.pickings_by_id[picking.id] = picking;
                        self.picking_search_string += '' + picking.id + ':' + (picking.name ? picking.name.toUpperCase(): '') + '\n';
                    }

                });
        },
    });
    
  
    
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
     /*   get_rows: function(){
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
        },*/
        renderElement: function(){            
            var self = this;
            this._super();
            self.get_partner();
            
            self.render_active_operation();
        	
            
            self.$('table#operations tr td:first-child').click(function(){
            	
            	var id = $(this).parents("[data-id]:first").data('id');
            	self.set_active_operation(id);
           
            })
            
            self.$('#js_packconf_select').change(function(){
                var ul_id = self.$('#js_packconf_select option:selected').data('ul-id');
                var width = self.$('#js_packconf_select option:selected').attr('width');
                var height = self.$('#js_packconf_select option:selected').attr('height');
                var length = self.$('#js_packconf_select option:selected').attr('length');
                self.$('.o_pack_data #width').val(width);
                self.$('.o_pack_data #height').val(height);
                self.$('.o_pack_data #length').val(length);

            });
            self.$('.js_validate_pack').click(function(){
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
            self.$('.js_pack_configure').click(function(){
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
        	if(this.getParent().picking.partner_id){
        		return new instance.web.Model('res.partner').call('search_read',[ [['id', '=', this.getParent().picking.partner_id[0]]], ['name','street','street2','city','state_id','country_id', 'zip'] ], {context: new instance.web.CompoundContext()}).done(function(partners){
                    var partner = partners[0]
        			var street = partner.street
                    var street2 = partner.street2
                    var city = partner.city
                    var state = partner.state_id 
                    var zip = partner.zip
                    var partner_string = partner.name
                    $('.oe_pick_app_partner').append((partner.name ? $('<h5>', {
                        'class': 'o_partner_name'
                    }).text(partner.name + ',') : '')).append((partner.street ? $('<h5>', {
                        'class': 'o_partner_street'
                    }).text(partner.street + ',') : '')).append((partner.street2 ? $('<h5>', {
                        'class': 'o_partner_street2'
                    }).text(partner.street2 + ',') : '')).append((partner.city ? $('<h5>', {
                        'class': 'o_partner_city',
                    }).text(partner.city + ', ') : '')).append((partner.state_id[1] ? $('<h5>', {
                        'class': 'o_partner_state',
                    }).text(partner.state_id[1] + ', ') : '')).append((partner.zip ? $('<h5>', {
                        'class': 'o_partner_zip',
                    }).text(partner.zip + ',') : '')).append((partner.country_id[1] ? $('<h5>', {
                        'class': 'o_partner_country'
                    }).text(partner.country_id[1]) : ''));
        		});
        	}
            
        },
        set_active_operation: function(op_id){
        	var operation = this.rows.find(op => op.cols.id === op_id );
        	
        	this.active_operation_id = operation.cols.id;
        	this.render_active_operation();
        	
        },
        render_active_operation: function(){
        	var self = this;
        	if(this.active_operation_id){
        		var operation = this.rows.find(op => op.cols.id === this.active_operation_id );
            	if(operation){
            		var active_container = this.$('#selected_product_container');
                	active_container.html(
                            QWeb.render('SelectedOperation',{operation:operation.cols})
                        )
                    active_container.find('.js_plus').click(function(){
                        var op = $(this).parents("[data-id]:first");
                    	var id = op.data('product-id');
                        var op_id = op.data('id');
                        self.getParent().scan_product_id(id,true,op_id);
                    });
                	active_container.find('.js_minus').click(function(){
                		var op = $(this).parents("[data-id]:first");
                    	var id = op.data('product-id');
                        var op_id = op.data('id');
                        self.getParent().scan_product_id(id,false,op_id);
                    });
                	
                	active_container.find('.js_qty').focus(function(){
                        self.getParent().barcode_scanner.disconnect();
                        
                    });
                	active_container.find('.js_qty').blur(function(){
                        var op_id = $(this).parents("[data-id]:first").data('id');
                        var value = parseFloat($(this).val());
                        if (value>=0){
                            self.getParent().set_operation_quantity(value, op_id);
                        }
                        
                        self.getParent().barcode_scanner.connect(function(ean){
                            self.getParent().scan(ean);
                        });
                    });
            	}
        		
        	}
        	
        },
        blink: function(op_id){
            this.set_active_operation(op_id);
        	this._super();
            
        },
    });
}

openerp.warehouse_barcode_interface = function(openerp) {
    openerp.warehouse_barcode_interface = openerp.warehouse_barcode_interface || {};
    openerp_picking_order_widgets(openerp);
}