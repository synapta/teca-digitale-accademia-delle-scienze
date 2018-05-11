var fs = require('fs');
var data = JSON.parse(fs.readFileSync('./public/data/book.json', 'utf8'))
console.log(data)
var itemsjs = require('itemsjs')(data, {
  sortings: {
    name_asc: {
      field: 'title',
      order: 'asc'
    }
  },
  aggregations: {
    publisher: {
      title: 'publisher',
      size: 10
    },
    language: {
      title: 'language',
      size: 10
    },
    date: {
      title: 'date',
      size: 10
    },
    creator: {
      title: 'creator',
      size: 10
    }
  },
  searchableFields: ['title', 'description', 'date', 'creator', 'identifier']
});

exports.searchItem = function(request) {
  console.log(request.query)
  var filters = {};

  ['creator', 'date', 'publisher', 'language' ].forEach(function(v) {
    filters[v] = request.query[v];
  })

  console.log(filters)

  return itemsjs.search({
    per_page: 10,
    page: request.query.s,
    sort: 'name_asc',
    // full text search
    query: request.query.q,
    filters: filters
  })
}

exports.topItem = function(request) {
  return itemsjs.aggregation({
    per_page: 1,
    sort: 'name_asc',
    // full text search
    query: request.query.q,
  })
}
