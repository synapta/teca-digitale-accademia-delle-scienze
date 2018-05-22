var id = window.location.pathname.replace("/book/", "");

var getHeight = function(){
  return $(document).height() - 5;
}
var getWidth = function() {
  return $(window).width() - 5;
}

var getIAFrame = function(book, height, width) {
    if (height/width > 1.)
      var page = '1'
    else
      var page = '2'
    return "<iframe src='https://archive.org/stream/" + book + "#page/1/mode/" + page + "up' " +
           "width='" + width + "px' height='" + height + "px' frameborder='1' id='frame' ></iframe>"
}

$("#iframe-container").html(getIAFrame(id, getHeight(), getWidth()))

$(window).resize(function() {
  $("#iframe-container").html("");
  $("#iframe-container").html(getIAFrame(id, getHeight(), getWidth()));
});
