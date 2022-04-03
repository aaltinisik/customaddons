odoo.define('ks_chat_edit_and_delete.ks_qweb_load', function (require) {
'use strict';

    var core = require('web.core');
    var ajax = require('web.ajax');
    var ks_thread = require('mail.widget.Thread');
    var ks_abstract_message = require('mail.model.AbstractMessage');
    var ks_rpc = require('web.rpc');
    var ks_model_message = require('mail.model.Message');
    var ks_session = require('web.session');
    var ks_emojis = require('mail.emojis');
    var ks_mailUtils = require('mail.utils');
    var ks_ajax = require('web.ajax');
    var ks_config = require('web.config');
    var ks_qweb = core.qweb;
    var ks_global_id = 0;
    var ks_message_div;
    var ks_message;
    var ks_thread_messages

    if(ks_session.ks_chat_enable)
        ks_ajax.loadXML('/ks_chat_edit_and_delete/static/src/xml/ks_inherited_mail_config.xml', ks_qweb);

    ks_thread.include({

         events: _.extend({}, ks_thread.prototype.events, {
            'click .o_thread_edit': '_onEditClick',
            'click .o_thread_message_delete': '_onDeleteClick',
            'click .o_mail_emoji_container .o_mail_emoji': '_onEmojiImageClick',
            'mouseover .o_thread_message': 'onMessageThreadHover',
            'mouseout .o_thread_message': 'onMessageThreadUnHover',
        }),

          /*
          * Render function is used to clone all the messages and start a thread to disabled the edit/delete icons after 15 minutes.
          */
         render: function (thread, options) {
           var ks_self = this;
            ks_thread_messages = _.clone(thread.getMessages({ domain: options.domain || [] }));


            if (!this._updateTimestampsInterval) {
                this.ks_updateTimestampsInterval = setInterval(function () {
                    var ks_res = ks_self.ks_updateTimestamps();
                }, 1000*60);
            }

            var $html = this._super(thread, options);

            _.each(ks_thread_messages, function (ks_message) {
                try{
                if($(ks_message).find(".ks_check_edited").length){
                  $(ks_message).find(".ks_check_edited").css("display","none");
                }
                var $ks_message = this.$('.o_thread_message[data-message-id="'+ ks_message.getID() +'"]');
                var ks_check = this.$('.o_thread_message[data-message-id="'+ ks_message.getID() +'"]');
                $ks_message.find('.o_thread_message_side_date').data('date', ks_message.getDate());
                this._insertReadMore($ks_message);
                }
                catch(err){
                    console.log(err);
                }
            }.bind(ks_self));

            this.$el.find('.ks_edit_icon').addClass('ks_hide')
            this.$el.find('.ks_delete_icon').addClass('ks_hide')
            this.$el.find('.fa-star-o').parent().addClass('ks_hide')

            return $html;
        },

         //    Hover discussion thread onchange
         onMessageThreadHover : function(e){
                 $(e.currentTarget).find('.ks_edit_icon').removeClass('ks_hide');
                 $(e.currentTarget).find('.ks_delete_icon').removeClass('ks_hide');
                 $(e.currentTarget).find('.fa-star-o').parent().removeClass('ks_hide');
                 $(e.currentTarget).find('.ks_check_edited').addClass('ks_hide');
            },

         //    UnHover discussion thread onchange
         onMessageThreadUnHover : function(e){
                $(e.currentTarget).find('.ks_edit_icon').addClass('ks_hide');
                $(e.currentTarget).find('.ks_delete_icon').addClass('ks_hide');
                $(e.currentTarget).find('.fa-star-o').parent().addClass('ks_hide');
                $(e.currentTarget).find('.ks_check_edited').removeClass('ks_hide');
            },

          /*
           * _onEditClick function is used to handle the click event of the edit icon.
           */
         _onEditClick: function (ev){
            var ks_self = this;
            var ks_messageID = $(ev.currentTarget).data('message-id');
            var ks_icons = $('[data-message-id = '+ks_messageID+']');
            var ks_msg_date = ks_icons[0].children[4].children[0].children[1];
            var ks_sidebar_msg_date = ks_icons[0].children[0].children[0];
            $(ks_icons[1]).hide();
            $(ks_icons[3]).hide();
            $(ev.currentTarget).hide();


            var ks_time = $(ks_msg_date).data('date');
            var ks_sidebar_time = $(ks_sidebar_msg_date).data('date');
            /*
             * Condition to check the Illegal updation of the message.
             */

            if((moment().diff(ks_time, 'minutes') > 15) || (moment().diff(ks_sidebar_time, 'minutes') > 15)){
                $(ks_icons[1]).show();
                return;
            }

            if(ev.target.className === "fa o_thread_icon o_thread_edit fa-pencil fa-lg"){
                try{
                        if($("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].children[0].className === "o_attachments_previews" || $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].children[0] === undefined){
                            var ks_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1];
                            var ks_msg = $(ks_div).contents().get(0).nodeValue;
                            $(ks_div).contents().get(0).nodeValue = "";
                            $(ks_div).prepend("<p>"+ks_msg.trim()+"</p>");
                        }
                    }
                catch(err){
                         if($("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].children[0] === undefined){
                            var ks_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1];
                            var ks_msg = $(ks_div).contents().get(0).nodeValue;
                            $(ks_div).contents().get(0).nodeValue = "";
                            $(ks_div).prepend("<p>"+ks_msg.trim()+"</p>");
                        }
                    }
                ks_message_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].children[0];
                ks_message = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].children[0].innerText;

            }
            else{
                try{
                    if($("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[0].className === "o_attachments_previews"){
                        var ks_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0];
                        var ks_msg = $(ks_div).contents().get(0).nodeValue;
                        $(ks_div).contents().get(0).nodeValue = "";
                        $(ks_div).prepend("<p>"+ks_msg.trim()+"</p>");
                    }
                }
                catch(err){
                    if($("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[0] === undefined){
                        var ks_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0];
                        var ks_msg = $(ks_div).contents().get(0).nodeValue;
                        $(ks_div).contents().get(0).nodeValue = "";
                        $(ks_div).prepend("<p>"+ks_msg.trim()+"</p>");
                    }
                }
                ks_message_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[0];
                ks_message = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[0].innerText;
            }

            var ks_input = document.createElement("div");
            ks_input.id = "div_input_"+ks_messageID;
            $(ks_input).addClass("div_input");
            ks_input.innerHTML = "<div><textarea type='text' class='o_input_chat' id='input_"+ks_messageID+"'> </textarea>  <button class=' btn btn-secondary fa o_thread_smile fa-smile-o' type='button' data-toggle='popover' title='Emojis' id='emoji_"+ks_messageID+"' ></button><i class='fa o_thread_update fa-check fa-lg' title='Update' id='update_"+ks_messageID+"' ></i> <i class='fa o_thread_cancel fa-times fa-lg' title='Cancel' id='cancel_"+ks_messageID+"' ></i></div>";
            ks_message_div.replaceWith(ks_input);
            $('#input_'+ks_messageID).val(ks_message);

            var ks_textarea = document.getElementById("input_"+ks_messageID);
            ks_textarea.style.cssText = 'height:auto; padding:0';
            ks_textarea.style.cssText = 'height:' + ks_textarea.scrollHeight + 'px';
            $(ks_textarea).scrollTop(ks_textarea.scrollHeight);

            document.getElementById("update_"+ks_messageID).onclick = function() {ks_update_click(ks_message,false,ks_self)};
            document.getElementById("cancel_"+ks_messageID).onclick = function() {ks_update_click(ks_message,true,ks_self)};
            document.getElementById("emoji_"+ks_messageID).onclick = function() {ks_emoji_btn_click(ks_self,ks_messageID)};

            $('#input_'+ks_messageID).on("keyup", function(e) {
                if (e.keyCode == 13 && !e.shiftKey) {
                    ks_update_click(ks_message,false,ks_self);
                }
            });

            $('#input_'+ks_messageID).on("keydown", function(e) {
                var ks_el = this;
                setTimeout(function(){
                    ks_el.style.cssText = 'height:auto; padding:0';
                    ks_el.style.cssText = 'height:' + ks_el.scrollHeight + 'px';
                    $(ks_el).scrollTop(ks_el.scrollHeight);
                  },0);
            });

            /*
             * Function to handle the emoji button.
             */

            function ks_emoji_btn_click(ks_self,ks_messageID)
            {
                ks_global_id = ks_messageID;
                if (!ks_self._$emojisContainer) {
                ks_self._$emojisContainer = $(ks_qweb.render('mail.Composer.emojis', {
                    emojis: ks_emojis,
                }));
                }
                if (ks_self._$emojisContainer.parent().length) {
                    ks_self._$emojisContainer.remove();
                } else {
                    ks_self._$emojisContainer.appendTo($('#div_input_'+ks_messageID));
                    ks_self.$el.scrollTop(ks_self.el.scrollHeight);
                }
            }

            /*
             * Function to Handle the update click button to update the message.
             */

            function ks_update_click(ks_message,ks_undo,ks_self) {
                var ks_input_val = document.getElementById("input_"+ks_messageID).value;

                if(ks_self._$emojisContainer != undefined){
                    ks_self._$emojisContainer.remove();
                }

                if(ks_input_val === "" || ks_undo === true){
                   ks_input_val = ks_message;
                }

                if(ev.target.className === "fa o_thread_icon o_thread_edit fa-pencil fa-lg"){
                    ks_message_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].children[0];
                    var ks_msg_span = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[5];
                }
                else{
                    ks_message_div = $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[0];
                    var ks_msg_span = $("[data-message-id = "+ks_messageID+"]")[0].children[3];
                }

                if(ks_input_val != ks_message){
                    var ks_data = ks_rpc.query({
                                model: 'mail.message',
                                method: 'ks_edit_message',
                                args: [ks_messageID, true],
                            });
                    ks_msg_span.innerHTML = "<span>(Edited)</span>";

                    _.map(ks_thread_messages, function(ks_thread_message, ks_message_div){
                       if(ks_thread_message._id === ks_messageID){
                            ks_thread_message.ks_msg_edit = true;
                            ks_thread_message._body = $("#input_"+ks_messageID)[0].value;
                       }
                   });
                }

                var ks_para = document.createElement("P");
                var ks_text = document.createTextNode(ks_input_val);
                ks_para.appendChild(ks_text);
                $(ks_message_div.replaceWith(ks_para));

                ks_input_val = "<p>"+ks_input_val+"</p>";
                var messages = ks_rpc.query({
                model: 'mail.message',
                method: 'write',
                args:  [[ks_messageID],{'id': ks_messageID,
                                        'body': ks_input_val, }],
                });
                $(ks_icons[1]).show();
                $(ks_icons[2]).show();
                $(ks_icons[3]).show();
            }
         },

            /*
             * Function to handle the delete button for deleting the message.
             */
         _onDeleteClick: function(ev){

             var ks_result = confirm("Are you sure, you want to delete this message permanently ?");
             if (ks_result) {
               var ks_self = this;
               var ks_messageID = $(ev.currentTarget).data('message-id');
               var ks_data = ks_rpc.query({
                                model: 'mail.message',
                                method: 'ks_delete_message',
                                args: [ks_messageID],
                            }).then (function(value){
                                    return value;
                       });

               var ks_msg_edited = ks_rpc.query({
                                model: 'mail.message',
                                method: 'ks_edit_message',
                                args: [ks_messageID, false],
                            });
               var ks_messageID = $(ev.currentTarget).data('message-id');

               if(ev.target.className === "fa fa-lg fa-trash-o o_thread_icon o_thread_message_delete"){
                    $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[1].innerHTML = "<p><i>This message was deleted.</i></p>";
                    $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].children[5].innerHTML = "";
                }
               else{
                    $("[data-message-id = "+ks_messageID+"]")[0].children[4].children[0].innerHTML = "<p><i>This message was deleted.</i></p>";
                    $("[data-message-id = "+ks_messageID+"]")[0].children[3].innerText = "";
                }

               _.map(ks_thread_messages, function(ks_thread_message){
                       if(ks_thread_message._id === ks_messageID){
                            ks_thread_message._body = "<p><i>This message was deleted.</i></p>";
                            ks_thread_message.ks_msg_edit = false;
                            ks_thread_message._type = "notification";
                            ks_thread_message._attachmentIDs = [];
                       }
                });

               var ks_notif_div = document.createElement("div");
               ks_notif_div.id = "snackbar";
               var ks_textnode = document.createTextNode("Message deleted successfully");
               ks_notif_div.appendChild(ks_textnode);

               var ks_body = document.getElementsByTagName("body");
               $(ks_body[0]).append(ks_notif_div);

               var ks_snackbar = document.getElementById("snackbar");
               ks_snackbar.className = "show";
               setTimeout(function(){ ks_snackbar.className = ks_snackbar.className.replace("show", ""); }, 3000);

               var ks_icons = $('[data-message-id = '+ks_messageID+']');
               $(ks_icons[1]).hide();
               $(ks_icons[2]).hide();
               $(ks_icons[3]).hide();

             }
         },

         _onEmojiImageClick: function (ev) {

           var ks_emotes = $(ev.currentTarget).data('emoji');
           _.each(ks_emojis, function (emoji) {
                _.each(emoji.sources, function (source) {
                    var escapedSource = String(source).replace(/([.*+?=^!:${}()|[\]/\\])/g, '\\$1');
                    var regexp = new RegExp("(\\s|^)(" + escapedSource + ")(?=\\s|$)", 'g');
                    ks_emotes = ks_emotes.replace(regexp, '$1' + emoji.unicode);
                });
            });

           $('#input_'+ks_global_id).val( $('#input_'+ks_global_id).val() + " " + ks_emotes + " " );
           this._$emojisContainer.remove();
        },

        /*
         *  Function to disable edit and delete icons after 15 minutes of the message send.
         */

        ks_updateTimestamps: function () {
            var time;
            if(ks_session.is_admin){
                time = (48*60);
            }else{
                time = 15;
            }
            this.$('.text-muted').each(function () {
                var ks_timestamp = this.children[1];
                var ks_date = $(ks_timestamp).data('date');
                try{
                    if(this.children[3].innerText != ""){
                         if(!(moment().diff(ks_date, 'minutes') < time)){
                            this.children[3].innerHTML = "";
                            this.children[4].innerHTML = "";
                        }
                }}
                catch(err){
                    console.log(err);
                }
            });

            this.$('.o_mail_discussion').each(function () {
                    try{
                        if(this.children[0].children[0].className === "o_thread_message_side_date"){
                            var ks_timestamp = this.children[0].children[0];
                            var ks_date = $(ks_timestamp).data('date');
                                if(this.children[1].children[0] !== "undefined"){
                                    if(!(moment().diff(ks_date, 'minutes') < time)){
                                        this.children[1].innerHTML = "";
                                        this.children[2].innerHTML = "";
                                    }
                                }
                        }
                    }
                    catch(err){
                    }
            });
        },

    });

    ks_abstract_message.include({

        /*
         * init function to add attribute ks_msg_edit is true or false to check the message is edited or not.
         */

        init: function (parent, data) {
            this.ks_msg_edit = data.ks_msg_edit;
            this._super(parent, data);
        },

        /*
         * ks_hasBody checks that the message is contained only document and not message.
         */

        ks_shouldRedirectToAuthor:function(){
            if(ks_session.is_admin && ks_session.ks_admin_delete_access){
                return false;
            }
            else{
                return this.shouldRedirectToAuthor();
            }
        },
        ks_hasBody: function(){
            if(this._type === "comment"){
                if(this._body.length != 0){
                    return true;
                }
                return false;
            }
            return false;
        },

        /*
         * Function to return the that message is edited or not.
         */

        ks_getEditMessage: function(){
            return this.ks_msg_edit;
        },

        ks_edit_time_elapsed: function(){
            if(moment().diff(this.getDate(), 'minutes') < 15)
            {
                return true;
            }
            return false;
        },

        ks_edit_time_elapsed_delete : function(){
            var time;
            if(ks_session.is_admin && ks_session.ks_admin_delete_access){
                time = (48*60);
            }else{
                time = 15;
            }

            if(moment().diff(this.getDate(), 'minutes') < time)
            {
                return true;
            }
            return false;
        }
    });

    ks_model_message.include({

        init: function (parent, data, emojis){
            this._super(parent, data, emojis);
        },

        _processBody: function () {
            var ks_self = this;
            _.each(ks_emojis, function (emoji) {
                var unicode = emoji.unicode;
                var regexp = new RegExp("(?:^|\\s|<[a-z]*>)(" + unicode + ")(?=\\s|$|</[a-z]*>)", 'g');
                var originalBody = ks_self.body;
                ks_self._body = ks_self._body.replace(regexp,
                    ' <span class="o_mail_emoji">' + unicode + '</span> ');
                // Idiot-proof limit. If the user had the amazing idea of
                // copy-pasting thousands of emojis, the image rendering can lead
                // to memory overflow errors on some browsers (e.g. Chrome). Set an
                // arbitrary limit to 200 from which we simply don't replace them
                // (anyway, they are already replaced by the unicode counterpart).
                if (_.str.count(ks_self._body, 'o_mail_emoji') > 200) {
                    ks_self._body = originalBody;
                }
            });
            var ks_body_check = ks_self._body;
            if(ks_body_check.includes("</p>")){
                if(!ks_body_check.includes("<p>")){
                    ks_self._body = "<p>"+ks_self._body;
                }
            }
            // add anchor tags to urls
            ks_self._body = ks_mailUtils.parseAndTransform(ks_self._body, ks_mailUtils.addLink);
        },

    });
});