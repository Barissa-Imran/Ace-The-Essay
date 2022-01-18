// sidebar panel show/hide on screen size

$(document).ready(function () {
  // variable assignment outside event handler
  var $window = $(window);
  var $panel = $("#navcol-1");

  function checkWidth() {
    var windowsize = $window.width();
    if (windowsize <= 1024) {
      // if window is equal to tablet ir smaller then hide sidebar panel
      $panel.toggleClass("collapse");
    }
  }
  //   Execute on load
  checkWidth();
  //   Bind event listener
  $(window).resize(checkWidth);
});

// calculate approximate number of words according to spacing
$("#id_spacing").mouseup(function spacing(e) {
  return e.target.value;
});

/* compute the price as the user types from number of pages*/
$("#id_number_of_pages").keyup(function (e) {
  $("#number_of_pages").html(e.target.value + " pages x (price)");
  $("#total").html("$" + e.target.value * 4.0);

  // calculate the approximate number of words
  if (e.target.value == "1") {
    var count = 275;
    $("#hint_id_number_of_pages").html(count * 2 + " words approx");
  } else {
    var count = 275 * e.target.value;
    $("#hint_id_number_of_pages").html(count + " words approx");
  }
});

// number of pages compute on click arrows
$("#id_number_of_pages").click(function (e) {
  $("#number_of_pages").html("Number of pages x (price)");
  $("#total").html("$" + e.target.value * 4.0);

  // calculate the approximate number of words
  if (e.target.value == "1") {
    var count = 275;
    $("#hint_id_number_of_pages").html(count + " words approx");
  } else {
    var count = 275 * e.target.value;
    $("#hint_id_number_of_pages").html(count + " words approx");
  }
});

// get the academic level selected by the user and display it on price panel
$("#id_academic_level").mouseup(function (e) {
  $("#academic_level").html(e.target.value);
});

// get the type of paper to displaying on price panel
$("#id_type_of_paper").mouseup(function (e) {
  $("#type_of_paper").html(e.target.value);
});

// calculate deadline date according to selected date
$(document).ready(function () {
  $("#deadline_count").html(Date);
});

$(
  "#deadline_6, #deadline_12, #deadline_15, #deadline_24, #deadline_36, #deadline_48, #deadline_3, #deadline_5, #deadline_7, #deadline_10, #deadline_14, #deadline_30, #deadline_60"
).click(function () {
  if (this.id == "deadline_6") {
    $("#deadline_count").html(
      new Date(Date.now() + 0.25 * 24 * 60 * 60 * 1000)
    );
  } else if (this.id == "deadline_12") {
    $("#deadline_count").html(new Date(Date.now() + 0.5 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_15") {
    $("#deadline_count").html(
      new Date(Date.now() + 0.625 * 24 * 60 * 60 * 1000)
    );
  } else if (this.id == "deadline_24") {
    $("#deadline_count").html(new Date(Date.now() + 1 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_36") {
    $("#deadline_count").html(new Date(Date.now() + 1.5 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_48") {
    $("#deadline_count").html(new Date(Date.now() + 2 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_3") {
    $("#deadline_count").html(new Date(Date.now() + 3 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_5") {
    $("#deadline_count").html(new Date(Date.now() + 5 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_7") {
    $("#deadline_count").html(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_10") {
    $("#deadline_count").html(new Date(Date.now() + 10 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_14") {
    $("#deadline_count").html(new Date(Date.now() + 14 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_30") {
    $("#deadline_count").html(new Date(Date.now() + 30 * 24 * 60 * 60 * 1000));
  } else if (this.id == "deadline_60") {
    $("#deadline_count").html(new Date(Date.now() + 60 * 24 * 60 * 60 * 1000));
  }
});
