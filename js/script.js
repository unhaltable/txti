var scrollTo = function(el, off){
  $("html, body").animate({
    scrollTop: $(el).offset().top - off
  }, 650);
}

$("#more-button").click(function(){ scrollTo("#learn-more", 0); });

for (var i = 1; i < 3; i++) {
  $("#messages").prepend("<li><img src='http://unhaltable.github.io/txti/img/to" + i + ".jpg' width='258px'></li>");
  $("#messages").prepend("<li><img src='http://unhaltable.github.io/txti/img/from" + i + ".jpg' width='258px'></li>");
}