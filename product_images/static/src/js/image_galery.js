var instance = openerp;
var QWeb = instance.web.qweb;
var _t = instance.web._t;
instance.web.form.FieldImageGalery = instance.web.form.FieldMany2One.extend({
	template:"FieldMany2One_ImageGalery",
	events:{
		"click a.fa-image":'show_galery'
		},
	show_galery: function(){
		
		var product_id = this.get('value');
		return new instance.web.Model('product.product').call('read',[product_id, ['altinkaya_image_ids']]).then(function(data){
			if(data.altinkaya_image_ids.length == 0){
				return;
			}
			return new instance.web.Model('ir.attachment').call('read',[data.image_ids,['name']]).then(function(images){
				var dialog = new instance.web.Dialog(this, 
						{ title: _t("Product Images")}, 
						QWeb.render("image_galery",{'image_ids':images})).open();
			})
			
				
        });
		
		
	}
});

instance.web.form.widgets.add('image_galery','instance.web.form.FieldImageGalery');


instance.web.ListView.List.include({
	init: function(){
		this._super.apply(this, arguments);
		this.$current.delegate('a.fa-image', 'click', function (e) {
			var product_id = $(e.currentTarget).data('product-id');
			new instance.web.Model('product.product').call('read',[product_id, ['altinkaya_image_ids']]).then(function(data){
				if(data.altinkaya_image_ids.length == 0){
					return;
				}
				return new instance.web.Model('ir.attachment').call('read',[data.altinkaya_image_ids,['name']]).then(function(images){
					var dialog = new instance.web.Dialog(this, 
							{ title: _t("Product Images")}, 
							QWeb.render("image_galery",{'image_ids':images})).open();
				})
				
					
	        });
            e.preventDefault();
        })
		
	}
});
