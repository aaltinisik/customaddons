openerp.web_longpolling = function (instance) {
    instance.web.longpolling_socket = null;
    instance.web.WebClient.include({
        show_application: function() {
            instance.web.longpolling_socket = new instance.web.SocketIO('/longpolling');
            this._super();
        },
        on_logout: function () {
            instance.web.longpolling_socket.disconnect();
            this._super();
        },
    });

}
