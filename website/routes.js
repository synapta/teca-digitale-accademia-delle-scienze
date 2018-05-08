var queries = require('./queries.js');
var utils = require('./utils.js');
var config = require('./config.js');

module.exports = function(app) {

  app.get('/', function(req, res) {
    res.sendFile(__dirname + '/public/views/index.html');
  });

  app.get('/searchAgent', function(request, response) {
    queries.launchESSearch(request.param('q'), request.param('start'), INDEX_ADDRESS, function(res) {
      response.send(res);
    });
  });

  app.get('/search', function(request, response) {
    response.send(utils.searchItem(request))
  });

  app.get('/top', function(request, response) {
    response.send(utils.topItem(request))
  });
}
