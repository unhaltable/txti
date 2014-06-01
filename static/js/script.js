var scrollTo = function(el, off){
  $("html, body").animate({
    scrollTop: $(el).offset().top - off
  }, 650);
}

$("#more-button").click(function(){ scrollTo("#learn-more", 0); });

$(".recipe").click(function() {
  var image = "static/img/phone/" + $(this).attr("data-key") + ".jpg";
  $("#example").css('background-image', 'url(/' + image + ')');
});

