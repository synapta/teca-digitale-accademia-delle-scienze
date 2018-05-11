var utils = require('./utils.js');
var config = require('./config.js');

module.exports = function(app) {

  app.get('/', function(req, res) {
    res.sendFile(__dirname + '/public/views/index.html');
  });

  app.get('/search', function(request, response) {
    response.send(utils.searchItem(request))
  });

  app.get('/book/:id', function(req, res) {
      res.redirect("https://archive.org/stream/" + req.params.id);
  });
}
