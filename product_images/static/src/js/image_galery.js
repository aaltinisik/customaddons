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
		return new instance.web.Model('product.product').call('read',[product_id, ['image_ids']]).then(function(data){
			if(data.image_ids.length == 0){
				return;
			}
			var dialog = new instance.web.Dialog(this, 
					{ title: _t("Product Images")}, 
					QWeb.render("image_galery",{'image_ids':data.image_ids})).open();
				
        });
		
		
	}
});

instance.web.form.widgets.add('image_galery','instance.web.form.FieldImageGalery');