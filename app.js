var server = require('./server.js');
var spawn = require('child_process').spawn;
var ipc = require('./ipc.js');

var stdout = process.stdout.write;

//////////////// Configurations //////////////////
PORT = 8080
appspace = 'slapjack.';

////////////// Http server handler ///////////////
function serverHandler(req, res){
    ipc.write("simple_deal");
};

////////////// IPC client handler ////////////////
function ipcHandler(data){
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
    stdout("PyServer: " + data);
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
server.start(serverHandler, PORT);

