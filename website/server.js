var express  = require('express');
var app      = express();
var port     = process.env.PORT || 5432;
var morgan   = require('morgan');

app.use(morgan('common'));

app.use(express.static('public'));
require('./routes.js')(app);
require('./routesNegotiation.js')(app);

//The 404 Route (ALWAYS Keep this as the last route)
app.use(function(req, res) {
    res.status(404).sendFile(__dirname + '/public/views/404.html');
});

app.listen(port);
console.log('You can find your website on port ' + port);
