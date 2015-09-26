openerp.web_action_request = function (instance) {
    instance.web.WebClient.include({ 
        show_application: function() {
            var self = this;
            this._super();
            instance.web.longpolling_socket.on('get request', function (action) {
                instance.client.action_manager.do_action(action);
            });
        },
    });
};
