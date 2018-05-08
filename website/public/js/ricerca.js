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

//Clean import without decimals
var cleanImporto = function cleanImporto(x) {
  x = parseInt(x);
  return x.toLocaleString('it', {
    minimumFractionDigits: 0
  });
};

function formatter(value) {
  return cleanImporto(value).replace(/\B(?=(?:\d{3})+(?!\d))/g, '.');
}

function getTextQuery(value) {
  return value.replaceAll(" AND ", " ");
}

function beautyFilter(value) {
  return value.replace("author_ss=", "Autore: ")
    .replace("date_s=", "Data: ")
    .replace("language_s=", "Lingua: ")
    .replace("biblio_ss=*", "Biblioteca: ");
}

function agentName(str) {
  return str.split('###');

}

var type = getUrlParameter("type");
var params = decodeURIComponent(window.location.search).replace(/&type[^&]+/, "").split('&');
var luceneQuery = getUrlParameter("q");

var buttonFilter = function(url, title) {
  return '<a class="rect-btn nodeca rdf" style="cursor:pointer; margin-right:10px; font-size:12px; height:30px; line-height:30px;" href="' + url + '">' + title + ' ✖</a>';
}

for (var p = 2; p < params.length; p++) {
  luceneQuery += " AND " + params[p].replace("=", ":");
}

$.getJSON("/search?q=" + luceneQuery, function(resData) {
  console.log(resData);
  var obj = {
    instances: resData.data.items,
    facetsAuthArray: resData.data.aggregations.creator.buckets,
    facetsDataArray: resData.data.aggregations.date.buckets,
    facetsLinguaArray: resData.data.aggregations.language.buckets,
  }

  obj.currentQuery = decodeURIComponent(window.location.search).replace("?q=", "");
  obj.currentFacetQuery = decodeURIComponent(window.location.search).replace("?q=", "").replace(/&start=[0-9]{1,3}/, "&start=1");
  for (var i = 0; i < obj.instances.length; i++) {
    obj.instances[i].title = obj.instances[i].title;
    obj.instances[i].author = obj.instances[i].creator;
    obj.instances[i].date = obj.instances[i].date;
    obj.instances[i].identifier = obj.instances[i].identifier;
  }
  console.log(obj)
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
    var fa = {};
    fa.title = obj.facetsDataArray[i].key;
    fa.count = obj.facetsDataArray[i].doc_count;
    if (fa.count == 0) {
      break;
    }
    obj.facetsData.push(fa);
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
    var template = document.getElementById('resultTemplate').innerHTML;
    var output = Mustache.render(template, obj);
    $("#result").html(output);
    $('#search').val(getTextQuery(getUrlParameter("q")))

    for (var p = 2; p < params.length; p++) {
      $("#active-filters").append(buttonFilter("/ricerca?q=" + obj.currentQuery.replace("&" + params[p], "") + " ", beautyFilter(params[p])))
    }

    var num = 10;
    var pages = Math.ceil(parseInt(num) / 10);
    var currentPage = parseInt(getUrlParameter("start"));
/*
    if (currentPage > 1) {
      $("#results-number").append("Pagina " + currentPage + " di ").append(formatter(num) + " risultati");
    } else {
      $("#results-number").append(formatter(num) + " risultati");
    }

    //Draw pagination
    $('.pagination-buttons').bootpag({
      total: pages,
      page: currentPage,
      maxVisible: 5,
      leaps: true,
      firstLastUse: false,
      wrapClass: 'pagination',
      activeClass: 'active',
      disabledClass: 'disabled-pag',
      nextClass: 'next',
      prevClass: 'prev',
      lastClass: 'last',
      firstClass: 'first'
    });
*/
    //N.B. do NOT use bootpag on event because is bugged with double ajax call!!
    $('.disabled-pag').hide();
    $('ul.pagination.bootpag li').click(function(e) {
      var num = $(this).attr('data-lp');
      if (e.target.innerText === "»") {
        num = 1 + currentPage;
      }
      if (e.target.innerText === "«") {
        num = -1 + currentPage;
      }

      document.location.href = "/ricerca?q=" + obj.currentQuery.replace(/&start=[^&]+/, "&start=" + num)

      return false;
    });
  });
});
