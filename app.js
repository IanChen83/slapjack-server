var server = require('./server.js');
var spawn = require('child_process').spawn;

var ipc = require('./ipc.js');
//////////////// Configurations //////////////////
PORT = 8080
appspace = 'slapjack.';

////////////// Http server handler ///////////////
function serverHandler(req, res){
    res.end("Response");
};

////////////// IPC client handler ////////////////
function ipcHandler(data){
    console.log(data.startsWith("he"));
}

//////////////// SIGINT handler //////////////////
function exitHandler(){
    console.log("\r");
    if(server.status()){
        server.close(process.exit);
    }
    if(pyserver.connected){
        pyserver.kill();
    }
    setTimeout(() => {
        process.exit(2);
    }, 2000);
}
process.on('SIGINT', exitHandler);


///////////////// App workflow ///////////////////


///// Initial PyServer /////
var pyserver = spawn('python', ['-u','ipc.py']);

pyserver.stdout.on('data', function(data){
    console.log("PyServer: " + data);
});

pyserver.on('close', function(code){
    console.log("Pyserver closed (or crashed...)");
});

///// Start IPC /////
ipc.appspace = appspace;

setTimeout( () => {
    // setTimeout is needed to avoid pyserver not started
    ipc.start(ipcHandler);
}, 2000);


///// Start server /////
// server.start(serverHandler, PORT);

