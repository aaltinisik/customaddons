openerp.web_socketio = function (instance) {

    socket_to_disconnect_on_before_unload = {};
    window_on_before_unload = window.onbeforeunload;

    window.onbeforeunload = function(event) {
        _(_(socket_to_disconnect_on_before_unload).keys()).each(function (ns) {
            socket_to_disconnect_on_before_unload[ns]();
        });
        if (window_on_before_unload != undefined) window_on_before_unload(event);
    }

    instance.web_socketio.MixinSocket = instance.web.Class.extend({
        init: function(namespace) {
            var session_id = instance.session.session_id;
            socket_to_disconnect_on_before_unload[namespace] = this.disconnect;
            this.namespace = namespace;
            this.disconnected_method = [];
            this.reconnected_method = [];
            //for reconnection of server
            this.on('get session id', function () {
                this.emit('session id', session_id);
            });
            // for connection and reconnection of client
            this.emit('session id', session_id);
        },
        on: function (event, callback) {
            undefinedfunction();
        },
        emit: function (event) {
            undefinedfunction();
        },
        disconnect: function () {
            delete socket_to_disconnect_on_before_unload[this.namespace];
        },
        add_reconnect_method: function (callback) {
            this.reconnected_method.push(callback);
        },
        add_disconnect_method: function (callback) {
            this.disconnected_method.push(callback);
        },
        reconnected: function () {
            _(this.reconnected_method).each( function (method) {
                method();
            });
        },
        disconnected: function() {
            _(this.disconnected_method).each( function (method) {
                method();
            });
        },
    });


    instance.web.SocketIO = instance.web_socketio.MixinSocket.extend({
        init: function (namespace) {
            var self = this;
            this.socket = io.connect(namespace);
            this.connected = true;
            this.flag_disconnected = false;
            this.on('disconnect', function () {
                var socket = this;
                var reconnect = function() {
                    if (!self.connected) return;
                    if (socket.socket.connected) {
                        self.reconnected();
                        self.flag_disconnected = false;
                        return;
                    }
                    if (!self.flag_disconnected) {
                        self.disconnected();
                        self.flag_disconnected = true;
                    }
                    socket.socket.connect();
                    setTimeout(reconnect, 10000);
                };
                reconnect();
            });
            this._super(namespace);
        },
        on: function (event, callback) {
            this.socket.on(event, callback);
        },
        emit: function (event) {
            this.socket.emit.apply(this.socket, arguments);
        },
        disconnect: function (){
            this._super();
            this.connected = false;
            this.socket.disconnect();
        },
    });
}
