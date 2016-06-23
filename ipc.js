var ipc = require('node-ipc');

ipc.config.appspace = 'slapjack.';
ipc.config.rawBuffer = true;
ipc.config.maxRetries = 0;
ipc.config.silent = true;

var running = false;

function status(){
    return running;
}

function start(callback){
    ipc.connectTo(
            'pyserver',
            function(){
                // Set callback(s)
                ipc.of.pyserver.on('connect',
                        function(){
                            console.log("IPC: Connect to PyServer");
                            running = true;
                            ipc.of.pyserver.emit('hello');
                        });

                ipc.of.pyserver.on('disconnect',
                        function(){
                            console.log("IPC: Disconnect from PyServer");
                            running = false;
                        });
                ipc.of.pyserver.on('data',
                        function(data){
                            console.log("IPC: " +data);
                            if(callback) callback(data.toString());
                        });
            }
    );
}

exports.status = status;
exports.start = start;
exports.appspace = ipc.config.appspace;
exports.maxRetries = ipc.config.maxRetries;
