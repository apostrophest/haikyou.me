var http    = require("http"),
    restify = require("restify")
    fs      = require("fs"),
    url     = require("url"),
    path    = require("path");

var SERVE_DIR = "../app";
var MIME_MAP = {
  'html': 'text/html',
  'js': 'text/javascript',
  'css': 'text/css'
}

function abort404() {

}

function handleStatic(req, res, next) {
  console.log("Requesting " + req.url);
  
  var pathname = url.parse(req.url).pathname;
  var ext = path.extname(pathname);

  if (!ext) pathname = path.join(pathname, 'index.html');

  fs.readFile(SERVE_DIR + pathname, function(err, data) {
    if(err) {
      res.writeHead(404);
      res.write('fuck');
      res.end();

      return next();
    }

    res.writeHead(200, {"Content-Type": MIME_MAP[ext]});
    res.write(data);
    res.end();
  });
  
  return next();
}

// http.createServer(onRequest).listen(8888);

var server = restify.createServer();

server.get("/", handleStatic);
server.get("/index.html", handleStatic);
server.get(/^\/css\/.*/, handleStatic);
server.get(/^\/lib\/.*/, handleStatic);
server.get(/^\/partials\/.*/, handleStatic);
server.get(/^\/js\/.*/, handleStatic);
server.get(/^\/img\/.*/, handleStatic);

server.listen(8888);

console.log("Server has started.");