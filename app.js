var connect = require('connect');
var http = require('http');
var net = require('net');
var fs = require('fs').promises
var app = connect();
var requestIp = require('request-ip');
const express = require('express')
const appl = express()
// you can override which attirbute the ip will be set on by
// passing in an options object with an attributeName
app.use(requestIp.mw({ secondTry : 'clientIp' }))

const exec = require('child_process').exec;

app.use(function(req, res) {
    var ip = req.clientIp;
    fs.writeFile('data.txt',ip,{flags:'a'},(err,data)=>{
    	console.log(ip);//writing data to data.txt
    })
    var ipType = net.isIP(ip);
    fs.readFile('./project.html')
    .then(contents=>{
        res.setHeader("Content-Type","text/html");
        res.writeHead(200);
        res.end(contents);
    })
    .catch(err => {
        res.writeHead(500);
        res.end(err);
        return;})
    // }) // returns 0 for invalid, 4 for IPv4, and 6 for IPv6
    //res.end('Hello, your ip address is ' + ip + ' and is of type IPv' + ipType + '\n');

});

// http.createServer((req,res)=>{
//      fs.readFile('project.html',(err,data)=>{
//         res.writeHead(200,{'Content-Type':'text/html'})
//         res.write(data)
//         return res.end()
//     })
// })
// appl.get('/',(req,res)=>{
//     res.render('project.ejs')

// })
const myShellScript = exec('sh bash.sh /project_2');

const server =http.createServer(app).listen(3000);
// server.on('request',(req,res)=>{
//     fs.readFile(`./project.html`)
//     .then(contents=>{
//         res.setHeader("Content-Type","text/html");
//         res.writeHead(200);
//         res.end(contents);
//     })
    
//     });
// })
