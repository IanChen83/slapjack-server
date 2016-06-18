var SerialPort = require('serialport').SerialPort;

var serialPath = '/dev/ttyACM0';
var serial = null;

exports.set_serial_path = function(np){
    serialPath = np;
};

exports.get_serial_path = function(){
    return serialPath;
};

exports.serial = serial;

exports.open = function(onHandler){
    serial = new SerialPort(serialPath, function(err){
        if(err){
            console.log("Error opening serial port:", err.message);
            serial = null;
            return;
        }
        console.log("Serial start at " + serialPath);
        if(onHandler){
            serial.on('data', function(data){
                console.log("Serial receive:" + data);
                onHandler(data);
            });
        }
    });
};

exports.isOpen = function(){
    return !(serial == null || !serial.isOpen());
};

exports.write = function(data, writeHandler){
    if(!exports.isOpen()){
        console.log("Serial not opened.");
        return false;
    }
    serial.write(data, function(err){
        if(err){
            console.log("Serial write data failed.");
            return false;
        }
        if(writeHandler){
            writeHandler(data);
        }
    });
    return true;
};

exports.close = function(){
    if(!exports.isOpen()){
        console.log("Serial not opened.");
        return false;
    }
    serial.close(function(err){
        if(err){
            console.log("Serial closing error.");
        }else{
            console.log("Serial closed.");
        }
        serial = null;
    });
};
