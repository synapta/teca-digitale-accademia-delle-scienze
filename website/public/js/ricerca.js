var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = decodeURIComponent(window.location.search.substring(1)),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');

    if (sParameterName[0] === sParam) {
      return sParameterName[1] === undefined ? true : sParameterName[1];
    }
  }
};


function beautyFilter(value) {
  return value.replace("creator=", "Autore: ")
    .replace("date=", "Data: ")
    .replace("language=", "Lingua: ")
    .replace("type=", "Tipologia: ")
}

var type = getUrlParameter("type");
var params = decodeURIComponent(window.location.search).split('&');
var query = getUrlParameter("q");

var buttonFilter = function(url, title) {
  return '<a class="rect-btn nodeca rdf" style="cursor:pointer; margin-right:10px; font-size:16px; height:30px; line-height:30px; border-bottom:solid 1px;" href="' + url + '">' + title + ' ✖</a>';
}

for (var p = 1; p < params.length; p++) {
  query += "&" + params[p];
}

if (params[0] === "") {
  document.location.href = "/?q=&start=1"
}

$.getJSON("/search?q=" + query, function(resData) {
  var obj = {
    instances: resData.data.items,
    facetsAuthArray: resData.data.aggregations.creator.buckets,
    facetsDataArray: resData.data.aggregations.date.buckets,
    facetsTypeArray: resData.data.aggregations.type.buckets,
    facetsLinguaArray: resData.data.aggregations.language.buckets,
  }

  if (decodeURIComponent(window.location.search.substring(1)).split('&').indexOf('q=') > -1) {
    obj.hasSearch = false;
  } else {
    obj.hasSearch = true;
  }

  obj.currentQuery = decodeURIComponent(window.location.search).replace("?q=", "");
  obj.currentFacetQuery = decodeURIComponent(window.location.search).replace("?q=", "").replace(/&start=[0-9]{1,3}/, "&start=1");
  for (var i = 0; i < obj.instances.length; i++) {
    obj.instances[i].title = obj.instances[i].title;
    obj.instances[i].author = obj.instances[i].creator;
    obj.instances[i].date = obj.instances[i].date;
    obj.instances[i].type = obj.instances[i].type;
    obj.instances[i].identifier = obj.instances[i].identifier;
  }

  obj.facetsType = [];
  for (var i = 0; i < obj.facetsTypeArray.length; i++) {
    var fa = {};
    fa.type = obj.facetsTypeArray[i].key;
    fa.count = obj.facetsTypeArray[i].doc_count;
    if (fa.count == 0) {
      break;
    }
    obj.facetsType.push(fa);
  }

  obj.facetsAuth = [];

  for (var i = 0; i < obj.facetsAuthArray.length; i++) {
    var fa = {};
    fa.title = obj.facetsAuthArray[i].key;
    fa.count = obj.facetsAuthArray[i].doc_count;
    if (fa.count == 0) {
      break;
    }
    obj.facetsAuth.push(fa);
  }

  obj.facetsData = [];
  for (var i = 0; i < obj.facetsDataArray.length; i++) {
    if (obj.facetsDataArray[i].key !== '9999' && obj.facetsDataArray[i].key !== "    ") {
      var fa = {};
      fa.title = obj.facetsDataArray[i].key;
      fa.count = obj.facetsDataArray[i].doc_count;
      if (fa.count == 0) {
        break;
      }
      obj.facetsData.push(fa);
    }
  }

  obj.facetsLingua = [];
  for (var i = 0; i < obj.facetsLinguaArray.length; i++) {
    var fa = {};
    fa.title = obj.facetsLinguaArray[i].key;
    fa.count = obj.facetsLinguaArray[i].doc_count;
    if (fa.count == 0) {
      break;
    }
    obj.facetsLingua.push(fa);
  }


  $("#result").load("/views/template/ricerca-full-optional.html", function(res, status, xhr) {
    var template = document.getElementById('wok-main-panel-content').innerHTML;
    var output = Mustache.render(template, obj);
    $("#result").html(output);
    $('#search').val(getUrlParameter("q"))

    for (var p = 1; p < params.length; p++) {
      if (!params[p].includes('start=')) {
        $("#active-filters").append(buttonFilter("/?q=" + obj.currentQuery.replace("&" + params[p], "") + " ", beautyFilter(params[p])))
      }
    }

    var num = resData.pagination.total;
    var pages = Math.ceil(parseInt(num) / 10);
    var currentPage = parseInt(getUrlParameter("start")) || 1;

    $('#results-number').append((num || 0) + " risultati");

    var paginationObj = {
      totalPages: pages,
      visiblePages: 5,
      startPage: currentPage,
      initiateStartPageClick: false,
      first: 'Inizio',
      prev: '',
      next: '',
      last: 'Fine',
      onPageClick: function(event, page) {
        if (obj.currentQuery.includes('&start=')) {
          document.location.href = "/?q=" + obj.currentQuery.replace(/&start=[^&]+/, "&start=" + page)
        } else {
          document.location.href = "/?q=" + (obj.currentQuery || "") + "&start=" + page;
        }
      }
    }

    $('#pagination-demo').twbsPagination(paginationObj);

    $('#sync-pagination-demo').twbsPagination(paginationObj);

  });
});

$(document).on("keypress", "#search", function(e) {
  if (e.which == 13) {
    e.preventDefault()
    var searchField = $('#search').val();
    var params = "";
    var facets = ['creator', 'date', 'language']
    for (var i = 0; i < facets.length; i++) {
      params += (getUrlParameter(facets[i]) !== undefined) ? "&" + facets[i] + "=" + getUrlParameter(facets[i]) : "";
      document.location.href = "/?q=" + searchField + params;
    }
  }
});

$(document).on("click", "#clearsearch", function(e) {
    document.location.href = "/?q=&start=1";
});

console.log(getUrlParameter('q'))
if (decodeURIComponent(window.location.search.substring(1)).split('&').indexOf('q=') > -1 ) {
    console.log('remove')
    $('#autoreFacet').remove();
    $('#dataFacet').remove();
}
