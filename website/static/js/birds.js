// Generated by CoffeeScript 1.9.0
(function() {
  var createExpandButtons, expandNoSubfamilies;

  $(document).ready(function() {
    expandNoSubfamilies();
    return createExpandButtons();
  });

  expandNoSubfamilies = function() {
    return $(".no-subfamily").next("ul").toggleClass("collapsed");
  };

  createExpandButtons = function() {
    var links;
    links = $(".plus-sign").closest("a");
    links.css("cursor", "pointer");
    return links.click(function(e) {
      e.preventDefault();
      $(this).toggleClass("active");
      $(this).find(".plus-sign").toggleClass("minus");
      return $(this).closest("li").next("ul").toggleClass("collapsed");
    });
  };

}).call(this);
