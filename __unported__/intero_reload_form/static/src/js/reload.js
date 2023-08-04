odoo.define('intero_reload_form.reload', function (require) {
	var Pager = require('web.Pager');
	
	var Reload = Pager.include({
		first_render: true,
		 
		_updateArrows: function () {
	        var disabled = this.disabled || this._singlePage();
	        this.$('button').prop('disabled', disabled);
	        this.$(".o_pager_reload").prop("disabled", false);
	    },

		_render: function() {
			this._super();
			if (this.first_render) {
				this.first_render = false;
				var self = this;
				var $reload = $('<button class="fa fa-refresh btn btn-icon o_pager_reload" type="button" accesskey="R">')
				.click(function() {
					self._changeSelection(0);
				});
				$reload.appendTo(this.$el.find(".btn-group"));
			}
		}
	});
	return Reload;
});