var server = require('./server.js');
var spawn = require('child_process').spawn;
var ipc = require('./ipc.js');

var LINK = "LINK";
var SET_READY = "SET_READY";
var SET_SIMPLE_DEAL = "SIMPLE_DEAL";
var SET_DEAL = "DEAL";
var SET_HIT = "HIT";
var SET_FAKE_HIT = "FAKE_HIT";

var CONN_FAILED = "CONN_FAILED";
var RUN_SUCCESS = "RUN_SUCCESS";
var ARDUINO_FAILED = "ARDUINO_FAILED";
var SERVER_BUSY = "SERVER_BUSY";
var UNKNOWN_COMMAND = "UNKNOWN_COMMAND";

var resEnable = false;
var gRes = null;

//////////////// Configurations //////////////////
PORT = 8080
appspace = 'slapjack.';

var pyserver = null;

////////////// Http server handler ///////////////
function serverHandler(req, res){
    if(resEnable){
        console.log("HTTP server: " + SERVER_BUSY);
        res.end(SERVER_BUSY);
    }else{
        gRes = res;
        resEnable = true;

        var msg = req.url.substr(1);
        if(msg == "" || msg == LINK){
            ipc.write(LINK);
        }else if(msg == SET_READY){
            ipc.write(SET_READY);
        }else if(msg == SET_SIMPLE_DEAL){
            ipc.write(SET_SIMPLE_DEAL);
        }else if(msg == SET_DEAL){
            ipc.write(SET_DEAL);
        }else{
            console.write("HTTP server: Invaild request");
            res.end(UNKNOWN_COMMAND);
        }
    }
};
////////// PyServer Permanent Runner /////////////
function startPyServer(){
    ///// Initial PyServer /////
    pyserver = spawn('python', ['-u','app.py']);

    pyserver.stdout.on('data', function(data){
        process.stdout.write("PyServer: " + data);
    });

    pyserver.stderr.on('data', function(data){
        process.stdout.write("PyServer Error: " + data);
    });

    pyserver.on('close', function(code){
        console.log("Pyserver closed (or crashed...)");
        setTimeout(() => {
            console.log("Restart PyServer");
            startPyServer();
        }), 3000;
    });

}

////////////// IPC client handler ////////////////
function ipcHandler(data){
    if(resEnable){
        if(data == RUN_SUCCESS){
            gRes.end(RUN_SUCCESS);
        }else if(data == ARDUINO_FAILED){
            gRes.end(ARDUINO_FAILED);
        }else if(data == CONN_FAILED){
            gRes.end(CONN_FAILED);
        }else if(!isNaN(parseInt(data))){
            gRes.end(data);
        }else{
            gRes.end(UNKNOWN_COMMAND);
        }
        gRes = null;
        resEnable = false;
    }else{
        gRes = null;
    }
}

//////////////// SIGINT handler //////////////////
function exitHandler(){
    if(server){
        server.close();
    }
    if(pyserver){
        pyserver.kill();
    }
}
process.on('exit', exitHandler);

///////////////// App workflow ///////////////////
///// Start PyServer
//startPyServer();

///// Start IPC /////
ipc.appspace = appspace;

setTimeout( () => {
    // setTimeout is needed to avoid pyserver not started
    ipc.start(ipcHandler);
}, 2000);


///// Start server /////
server.start(serverHandler, PORT);

