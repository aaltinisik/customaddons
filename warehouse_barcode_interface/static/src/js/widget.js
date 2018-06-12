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
    	load: function(picking_id){
            var self = this;
            function load_picking_list(type_id){
                var pickings = new $.Deferred();
                new instance.web.Model('stock.picking')
                    .call('get_next_picking_for_ui',[{'default_picking_type_id':parseInt(type_id)}])
                    .then(function(picking_ids){
                        if(!picking_ids || picking_ids.length === 0){
                            (new instance.web.Dialog(self,{
                                title: _t('No Picking Available'),
                                buttons: [{
                                    text:_t('Ok'),
                                    click: function(){
                                        self.menu();
                                    }
                                }]
                            }, _t('<p>We could not find a picking to display.</p>'))).open();

                            pickings.reject();
                        }else{
                            self.pickings = picking_ids;
                            pickings.resolve(picking_ids);
                        }
                    });

                return pickings;
            }

            // if we have a specified picking id, we load that one, and we load the picking of the same type as the active list
            if( picking_id ){
                var loaded_picking = new instance.web.Model('stock.picking')
                    .call('read',[[parseInt(picking_id)], [], new instance.web.CompoundContext()])
                    .then(function(picking){
                        self.picking = picking[0];
                        self.picking_type_id = picking[0].picking_type_id[0];
                        return load_picking_list(self.picking.picking_type_id[0]);
                    });
            }else{
                // if we don't have a specified picking id, we load the pickings belong to the specified type, and then we take
                // the first one of that list as the active picking
                var loaded_picking = new $.Deferred();
                load_picking_list(self.picking_type_id)
                    .then(function(){
                        return new instance.web.Model('stock.picking').call('read',[self.pickings[0],[], new instance.web.CompoundContext()]);
                    })
                    .then(function(picking){
                        self.picking = picking;
                        self.picking_type_id = picking.picking_type_id[0];
                        loaded_picking.resolve();
                    });
            }

            return loaded_picking.then(function(){
                    if (!_.isEmpty(self.locations)){
                        return $.when();
                    }
                    return new instance.web.Model('stock.location').call('search',[[['usage','=','internal']]]).then(function(locations_ids){
                        return new instance.web.Model('stock.location').call('read',[locations_ids, []]).then(function(locations){
                            self.locations = locations;
                        });
                    });
                }).then(function(){
                    return new instance.web.Model('stock.picking').call('check_group_pack').then(function(result){
                        return self.show_pack = result;
                    });
                }).then(function(){
                    return new instance.web.Model('stock.picking').call('check_group_lot').then(function(result){
                        return self.show_lot = result;
                    });
                }).then(function(){
                	if(self.picking.state === 'confirmed' || self.picking.state === 'partially_available'){
                		return new instance.web.Model('stock.picking')
                        .call('force_assign', [self.picking.id])
                        .then(function(result){
                            if (self.picking.pack_operation_exist === false){
                                self.picking.recompute_pack_op = false;
                                return new instance.web.Model('stock.picking').call('do_prepare_partial',[[self.picking.id]]);
                            }
                        }); 
                	}
                    
                }).then(function(){
                        return new instance.web.Model('stock.pack.operation').call('search',[[['picking_id','=',self.picking.id]]])
                }).then(function(pack_op_ids){
                        return new instance.web.Model('stock.pack.operation').call('read',[pack_op_ids, [], new instance.web.CompoundContext()])
                }).then(function(operations){
                    self.packoplines = operations;
                    var package_ids = [];

                    for(var i = 0; i < operations.length; i++){
                        if(!_.contains(package_ids,operations[i].result_package_id[0])){
                            if (operations[i].result_package_id[0]){
                                package_ids.push(operations[i].result_package_id[0]);
                            }
                        }
                    }
                    return new instance.web.Model('stock.quant.package').call('read',[package_ids, [], new instance.web.CompoundContext()])
                }).then(function(packages){
                    self.packages = packages;
                }).then(function(){
                        return new instance.web.Model('product.ul').call('search',[[]])
                }).then(function(uls_ids){
                        return new instance.web.Model('product.ul').call('read',[uls_ids, []])
                }).then(function(uls){
                    self.uls = uls;
                });
        },
        print_picking_label: function(){
            var self = this;
            return new instance.web.Model('stock.picking.type').call('read', [[self.picking_type_id], ['code'], new instance.web.CompoundContext()])
                .then(function(pick_type){
                    return new instance.web.Model('stock.picking').call('do_print_picking_label',[[self.picking.id]])
                           .then(function(action){
                                return self.do_action(action);
                           });
                });
        },
        open_form_view: function(){
        	var self = this;
        	window.location = '/web#model=stock.picking&view_type=form&id=' + self.picking.id;
            
        },
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
        	
            this.$('.js_pick_print_label').click(function(){ self.getParent().print_picking_label(); });
            this.$('.js_pick_open_form').click(function(){ self.getParent().open_form_view(); });
            
            
            
            self.$('table#operations tr td:not(:last-child)').click(function(){
            	
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