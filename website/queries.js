var request = require('request');
var config


exports.launchSolrJson = function (query, pagina, solr_type, callback) {

    request(solr_type + "select?q=" + encodeURIComponent(query.replace("'", "\'" ))
            + "~0.9&wt=json&start=" + solrPage(pagina)
            + "&facet=true&facet.field=date_s&facet.field=language_s&facet.field=biblio_ss&facet.field=author_ss", function (error, response, body) {
        console.log('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the HTML for the Google homepage.
        callback(JSON.parse(body));
    });
}
