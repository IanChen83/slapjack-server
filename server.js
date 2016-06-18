var http = require('http');

const PORT = 8080;

function reqHandler(req, res){
    res.end('Response');
}

var server = http.createServer(reqHandler);

exports = server;
