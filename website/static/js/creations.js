// Generated by CoffeeScript 1.9.0
(function() {
  var initializeProgramInfoButtons, initializeRadioYearButtons;

  $(document).ready(function() {
    initializeRadioYearButtons();
    return initializeProgramInfoButtons();
  });

  initializeRadioYearButtons = function() {
    var yearButtons, yearPrograms;
    yearButtons = $(".year-button");
    yearPrograms = $(".year-programs");
    yearButtons.click(function(e) {
      var year;
      e.preventDefault();
      yearButtons.removeClass("active");
      yearPrograms.hide();
      $(".program-info").hide();
      year = $(this).attr("id");
      $(this).addClass("active");
      return $("#" + year + ".year-programs").show();
    });
    return $(".year-button:first").click();
  };

  initializeProgramInfoButtons = function() {
    var programInfoBoxes, programInfoButtons;
    programInfoButtons = $(".program-info-button");
    programInfoBoxes = $(".program-info");
    return programInfoButtons.click(function(e) {
      var program, programInfo;
      e.preventDefault();
      program = $(this).closest(".program");
      programInfo = program.find(".program-info");
      if (programInfo.is(":visible")) {
        return programInfo.hide();
      } else {
        return programInfo.show();
      }
    });
  };

}).call(this);
