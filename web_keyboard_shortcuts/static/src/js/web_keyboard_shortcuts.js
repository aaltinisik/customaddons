
openerp.web_keyboard_shortcuts = function (openerp) {
		var QWeb = openerp.web.qweb,
		_t = openerp.web._t;
		openerp.web_shortcuts.Shortcuts.include({
			 init: function() {
		            this._super.apply(this, arguments);
		            var old=this;
		            var match=0;
		        	var str ="";
		        	var select=0;
		        	var menu_id=0;
		        	$(document).keyup(function(event){
		        			if(fullscreen_toggle.menu_dict)
		        				{
		        				var d = event.keyCode;
		        				var pa=$(".oe_searchview_input").html();
		        				for (key in Object.keys(fullscreen_toggle.menu_dict))
		        					{if (pa)
		        						{
		        						if(pa=='<br>')
		        							{
		        							$("div.oe_searchview_clear").click();
		        							break;
		        							}
		        						if (pa.length>0 )
		        						{		pa=pa.replace(/\\/g, "\\\\");
		        								pa=pa.replace(/\(/g, "\\(");
		        								pa=pa.replace(/\)/g, "\\)");
		        								var patt1=new RegExp("^"+pa);
		        								if(patt1.test(Object.keys(fullscreen_toggle.menu_dict)[key]))
		        									{
		        									str = Object.keys(fullscreen_toggle.menu_dict)[key]
		        									var sub = str.substring(pa.length);
		        									$("#search_hint").remove();
		        									$(".oe_searchview_input").append('<div id="search_hint" style="color:#898585">'+sub+"</div>");
		        									match=1;
		        									}
		        							}
		        						}
		        					
		        					}
		        		      }
		                  if(d==39 && match==1)
		                  {
		                	  $(".oe_searchview_input").trigger("paste");
		                	  match=0;
		                	  select=1;
		                	  menu_id=fullscreen_toggle.menu_dict[str];
		                  }
		                  if(d==37 || d==8)
		                  {   
		                	  event.preventDefault();
		                	  match=0;
		                	  select=0;
		                  }
		                  if (fullscreen_toggle.menu_dict){
		                  if(d==13 && select==1 && menu_id)
		                	  {
		                      var self = old,
		                      id = menu_id;
		                      menu_id=0;
			                  self.session.active_id = id;
			                  // TODO: Use do_action({menu_id: id, type: 'ir.actions.menu'})
			                  select=0;
			                  match=0;
			                  self.rpc('/web/menu/action', {'menu_id': id}).done(function(ir_menu_data) {
			                      if (ir_menu_data.action.length){
			                          openerp.webclient.on_menu_action({action_id: ir_menu_data.action[0][2].id});
			                      }
			                  });
		                	  }
		                  }
		                  
		                  
		        	});
			 },
			 
		});

};





$(document).ready(function(event) {
	 $(document).keyup(function(event) {
		 $("button u span").unwrap();
	 });
    $(document).keydown(function(event) {
	    	jQuery(".oe_menu").sortable({axis: "x",
			cursor: "move",
		});
    	
    	$("#search_hint").remove();
        var n = String.fromCharCode(event.charCode);
        var d = event.keyCode;
        var alt_dict={}
        if (event.altKey) {
        	$("header button:visible").attr("accesskey",function(index,currentvalue){ 
        																if(currentvalue){
        																	
        																	var button_text = $(this).text();
        																	 $(this).html(button_text.replace(currentvalue,'<u class="alt_base"><span class="under_line">'+currentvalue+'</sapn></u>'));
        																	 alt_dict[currentvalue]=$(this);
        																	 $('.alt_base').addClass("alt_after");
																			}
        															   });
//        	$("button").attr("accesskey",function(index,currentvalue){ 
//				if(currentvalue){
//					
//					var button_text = $(this).text();
//					 $(this).html(button_text.replace(currentvalue,'<u><span class="under_line">'+currentvalue+'</sapn></u>'));
//					 alt_dict[currentvalue]=$(this);
//					 $(this).removeAttr("accesskey");
//					 $(this).attr("acckey",currentvalue);
//					}
//			   });
        	
        }
        
        if (event.keyCode && event.keyCode != 18 && event.altKey) {
        	event.preventDefault();
        	var pressed = String.fromCharCode(event.keyCode);
        	if (alt_dict.hasOwnProperty(pressed)!=false)
        	{
//    		if(alt_dict[pressed].is(":visible"))
//    		{
//    	
//    			alt_dict[pressed].click();
//    		}

        	}
        }
        if (event.keyCode && event.keyCode != 17 && event.ctrlKey) {
            if (d == 83) {
                event.preventDefault();
                var x = document.getElementsByTagName('button');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_button oe_form_button_save oe_highlight" && $(y).is(':visible')) {
                        y.click();
                    }
                }
            }

            if (d == 75) {

                event.preventDefault();
                var x = document.getElementsByTagName('a');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_vm_switch_kanban") {
                        y.click();
                    }
                }

            }

            if (d == 222) {

                event.preventDefault();
                var x = document.getElementsByTagName('a');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_vm_switch_graph") {
                        y.click();
                    }
                }

            }

            if (d == 68) {
            	event.preventDefault();
            	
            	if(fullscreen_toggle.fullscreen_toggle)
            	{
            	$('div.oe_searchview').animate({
                    "top": "-32px"
                },"fast");
            	fullscreen_toggle.search=0;
            	}
            	else{
            		$('div.oe_searchview').animate({
                        "top": "0px"
                    },"fast");
            		fullscreen_toggle.search=0;	
            	}
            }
            
            if (d == 76) {

                event.preventDefault();
                var x = document.getElementsByTagName('a');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_vm_switch_list") {
                        y.click();
                    }
                }
            }

            if (d == 27) {

                event.preventDefault();
                var x = document.getElementsByTagName('a');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_bold oe_form_button_cancel" && $(y).is(':visible')) {
                        y.click();
                    }
                }

            }

            if (d == 186 | d == 59) {

                event.preventDefault();
                var x = document.getElementsByTagName('a');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_vm_switch_form") {
                        y.click();
                    }
                }

            }

            if (d == 32) {

                event.preventDefault();
                var x = document.getElementsByTagName('button');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if ((y.className == "oe_button oe_list_add oe_highlight" | y.className == "oe_kanban_button_new oe_highlight" | y.className == "oe_button oe_form_button_create") && $(y).is(':visible')) {
                        y.click();
                    }

                }

            }
           
            if (d == 187) {

                event.preventDefault();
                var x = document.getElementsByTagName('button');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    alert(d);
                    if (y.className == "oe_button oe_form_button_edit") {
                        //y.click();
                    }
                }
            }
            if (d == 69) {

                event.preventDefault();
                var x = document.getElementsByTagName('button');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_button oe_form_button_edit") {
                        y.click();
                    }
                }
            }

            if (d == 40) {

                event.preventDefault();
                var x = document.getElementsByTagName('span');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "ui-icon ui-icon-triangle-1-e") {
                        y.click();
                    }
                }
            }

            if (d == 38) {

                event.preventDefault();
                var x = document.getElementsByTagName('span');
                for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "ui-icon ui-icon-triangle-1-s") {
                        y.click();
                    }
                }
            }

            if (d == 8) {

                event.preventDefault();
                var x = document.getElementsByTagName('a');
                f_list = []
                    for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "oe_breadcrumb_item") {
                        f_list.push(y);
                    }

                }
                x = f_list.pop();
                if (x) {
                    x.click();
                }
            }
            if (d == 122) {

                event.preventDefault();
                var x = document.getElementsByTagName('div');
                f_list = []
                    for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "fullscreen") {
                        y.click();
                        if(fullscreen_toggle.search==0)
                        	{
                        	$('div.oe_searchview').delay(500).animate({
                                "top": "-32px"
                            },"fast");
                        	
                        	}
                    }

                }

            }

            if (!fullscreen_toggle.fullscreen_toggle) {
                if (d == 49 | d == 50 | d == 51 | d == 52 | d == 53 | d == 54 | d == 55 | d == 56 | d == 57) {

                    event.preventDefault();
                    n = d - 48;
                    var x = document.getElementsByTagName('a');
                    for (i = 0; i < x.length; i++) {
                        y = x[i];
                        if (y.className == "oe_menu_toggler") {
                            if (n == i + 1) {
                                y.click();
                            }
                        }

                    }
                }
            }

            if (d == 37) {
                event.preventDefault();
                $('.oe_i[data-pager-action="previous"]').each(function() {
                    if ($(this).parents('div:hidden').length == 0) {
                        $(this).trigger('click');
                    }
                });
            }
            if (d == 39) {
                event.preventDefault();
                $('.oe_i[data-pager-action="next"]').each(function() {
                    if ($(this).parents('div:hidden').length == 0) {
                        $(this).trigger('click');
                    }
                });
            }

        }

        if (d == 192) {
            if (event.ctrlKey == 1) {
                event.preventDefault();
                $("div ul li a.oe_menu_leaf:visible:first").focus();
            }

        }

        if (d == 40) {
            for (i = 0; i < $("div ul li a.oe_menu_leaf:visible").length; i++) {
                if ($("div ul li a.oe_menu_leaf:visible:eq(" + i + ")").is(":focus")) {
                    event.preventDefault();
                    var flg = i + 1;
                    $("div ul li a.oe_menu_leaf:visible:eq(" + flg + ")").focus();
                    break;
                }

            }
        }
        if (d == 38) {
            var flg = 0;
            for (i = 0; i < $("div ul li a.oe_menu_leaf:visible").length; i++) {
                if ($("div ul li a.oe_menu_leaf:visible:eq(" + i + ")").is(":focus")) {
                    event.preventDefault();
                    var flg = i - 1;
                    $("div ul li a.oe_menu_leaf:visible:eq(" + flg + ")").focus();
                    break;
                }

            }
        }

        if (event.ctrlKey != 1) {
            if (d == 27) {
                event.preventDefault();
                var x = document.getElementsByTagName('div');
                f_list = []
                    for (i = 0; i < x.length; i++) {
                    y = x[i];
                    if (y.className == "fullscreentrue") {
                        y.click();
                        if(fullscreen_toggle.search==0)
                    	{
                        	$('div.oe_searchview').delay(500).animate({
                                "top": "0px"
                            },"fast");
                    	
                    	}
                    }

                }

            }
        }

    });
});
