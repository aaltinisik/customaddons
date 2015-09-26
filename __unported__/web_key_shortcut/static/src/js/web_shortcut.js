openerp.web_key_shortcut = function(instance, m) {
var _t = instance.web._t,
    QWeb = instance.web.qweb;
    instance.web_key_shortcut.KeyShortcutsIcon = instance.web.Widget.extend({
        template: 'web_shortcut_create_icon',
        init: function (parent) {
            this._super(parent);
        },
        start: function() {
            this.$el.find('.oe_key_shortcuts_toggle').click(function(){
                self.shortcuts = new instance.web_key_shortcut.KeyShortcuts(self);
                self.shortcuts.prependTo(instance.webclient.$el.find('.oe_systray'));
            });
            this._super();
        },
    });
    
    instance.web_key_shortcut.KeyShortcuts = instance.web.Widget.extend({
        template: 'web_shortcut_create',
        init: function() {
            this._super();
            var self = this
            this.start()
        },
        start: function() {
            var self = this;
            console.log(this.$el)
            this.$el.dialog(
                {
                buttons: {
                            'Create': function () { 
                                var menu_id = this.session
                                active_menu = document.getElementsByClassName('oe_active')
                                if (active_menu !== undefined){
	                                active_menu_array = Array.prototype.slice.call(active_menu)
	                                for (var i = 0; i < active_menu_array.length; i++) {
	                                   parent_node = active_menu_array[i].parentNode
	                                   console.log(parent_node.classList)
	                                   if (parent_node.classList.contains('oe_secondary_submenu')){
	                                       active_menu = active_menu_array[i]
	                                   }
	                                }
	                                console.log(active_menu)
	                                anchor_tab_data = active_menu.getElementsByTagName('a')
	                                if (anchor_tab_data !== undefined){
	                                    href = anchor_tab_data[0].href
	                                    console.log(href)
	                                    menu_data = href.substring(href.lastIndexOf("#")+1,href.lastIndexOf("&"));
	                                    menu_id = menu_data.split("=")[1]
	                                    if (menu_id !== undefined){
	                                       var selected_element = document.getElementById('modifier_key')
	                                       var selected_value = selected_element.options[selected_element.selectedIndex].value;
	                                       var other_key_element = document.getElementById('other_key')
	                                       var other_key_value = other_key_element.value
	                                       if (other_key_value.length === 0){
	                                           other_key_element.classList.add("dialog_box");
	                                       }
	                                       else{
		                                       var login_user_id = instance.session.uid
		                                       var vals = {
		                                           'menu_id': menu_id,
		                                           'modifier_key': selected_value,
		                                           'other_keys': other_key_value,
		                                           'user_id': login_user_id
		                                       }
		                                       $(this).dialog("close");
		                                       return new instance.web.Model("web.shortcut").get_func("create")(vals)
	                                       }
	                                    }
	                                }
                                }
                            },
                            'Cancel': function() {
                                $(this).dialog("close");
                            }
                            
                    },
                }
            );
            this._super();
        },
    });
    
    instance.web.WebClient.include({
        bind_hashchange: function() {
            var self = this;
            if (this.session.session_is_valid()){
	            new instance.web.Model("web.shortcut").get_func("search_read")([['user_id', '=', self.session.uid]]).pipe(function(res) {
	                //var self = this
	                key_data = {}
	                for (var i = 0; i < res.length; i++) {
	                    data = res[i]
	                    var menu_id = data['menu_id'][0]
	                    var action_id = data['action']
	                    var mod_key = data['modifier_key']
	                    var other_key = data['other_keys']
	                    key_comb = false
	                    if (other_key.substring(0, 1) == "+") {
	                        key_comb = mod_key+other_key
	                    }
	                    else{
	                        key_comb = mod_key+"+"+other_key
	                    }
	                    href = "#menu_id="+menu_id+"&action="+action_id
	                    key_data[key_comb] = href
	                }
	                var key_map = []
	                $(document.body).keydown(function (evt) {
	                    if (evt.keyCode === 16){
	                        key_map.push("shift")
	                    }
	                    else if(evt.keyCode === 17){
	                        key_map.push("ctrl")
	                    }
	                    else if(evt.keyCode === 18){
	                        key_map.push("alt")
	                    }
	                    else{
	                        key_map.push(String.fromCharCode( evt.keyCode ).toLowerCase())
	                    }
	                    console.log(JSON.stringify(key_map))
	                    if (key_map){
	                        key_map = self.remove_duplicate(key_map)
	                        key_combination = key_map.join("+")
	                        redir_href = key_data[key_combination]
	                        if (redir_href != undefined){
	                            evt.preventDefault();
	                            key_map = []
	                            document.location.href = redir_href;
	                        }
	                    }
	                });
	                $(document.body).keyup(function (evt) {
	                    if (evt.keyCode === 16){
	                        key_map = self.remove_element("shift", key_map)
	                    }
	                    else if(evt.keyCode === 17){
	                        key_map = self.remove_element("ctrl", key_map)
	                    }
	                    else if(evt.keyCode === 18){
	                        key_map = self.remove_element("alt", key_map)
	                    }
	                    else{
	                        key_code = String.fromCharCode( evt.keyCode ).toLowerCase()
	                        key_map = self.remove_element(key_code, key_map)
	                    }
	                });
	            });
            }
            this._super.apply(this, arguments);
        },
        remove_element: function(element, array){
            for (var i = 0; i < array.length; i++) {
                if (array[i] === element) {
                    array.splice(i, 1);
                    i--;
                }
            }
            return array
        },
        remove_duplicate: function(array){
            var uniqueNames = []
            $.each(array, function(i, el){
                if($.inArray(el, uniqueNames) === -1) uniqueNames.push(el);
            });
            return uniqueNames
        }
    });
    
    instance.web.UserMenu.include({
        do_update: function() {
            //alert("test")
            var self = this
            if (instance.session.session_is_valid()){
                self.key_shortcut_icon = new instance.web_key_shortcut.KeyShortcutsIcon(self);
                self.key_shortcut_icon.prependTo(instance.webclient.$el.find('.oe_systray'));
            }
            this._super();
        },
    });
};