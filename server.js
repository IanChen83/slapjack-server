/******** server.js ********
 * server   : http.server ojbect
 *
 * start    : function(handler, port)
 *              Start a new server. Previous server will be closed.
 *
 * close    : function()
 *              Close server if it existing
 *
 * get_port : function()
 *              return port number if server is running.
 *              return -1 if server is not running.
 **************************/
var http = require('http');

var server = null;
var PORT = -1;

function start(handler, port){
    if(server != null){
        // server has been started, do something?
        close(function(){
            console.log("Close previous server for restarting.");
        });
    }
    server = http.createServer(handler);
    server.listen(port, function(){
        console.log("Start server at port " + port);
        PORT = port;
    });
}

function close(callback){
    server.close(function(){
        console.log("Closing server");
        PORT = -1;
        callback();
    });
}

exports.server = server;
exports.start = start;
exports.close = close;
exports.get_port = () => PORT;

