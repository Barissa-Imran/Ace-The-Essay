// ****  JQuery  ***
$(document).ready(function () {
  /*---------------------Dashboards mobile view page-------------------------- */

  /* sidebar panel show/hide on screen size
  variable assignment outside event handler*/
  var $window = $(window);
  var $panel = $("#navcol-1");

  function checkWidth() {
    var windowsize = $window.width();
    if (windowsize <= 1024) {
      // if window is equal to tablet or smaller then hide sidebar panel
      $panel.addClass("collapse");
    } else {
      $panel.removeClass("collapse");
    }
  }
  //   Execute on load
  checkWidth();
  //   Bind event listener
  $(window).resize(checkWidth);

  /*---------------------------Place order page-------------------------------- */
  function words_1() {
    $("#id_number_of_pages").keyup(function (e) {
      $("#number_of_pages").html(e.target.value + " pages x (price)");
      $("#total").html("$" + e.target.value * 4.0);

      // calculate the approximate number of words
      if (e.target.value == "1") {
        var count = 275;
        $("#hint_id_number_of_pages").html(count + " words approx");
        return count;
      } else {
        var count = 275 * e.target.value;
        $("#hint_id_number_of_pages").html(count + " words approx");
        return count;
      }
    });
  }

  // number of pages compute on click arrows
  function words_2() {
    $("#id_number_of_pages").click(function (e) {
      $("#number_of_pages").html("Number of pages x (price)");
      $("#total").html("$" + e.target.value * 4.0);

      // calculate the approximate number of words
      if (e.target.value == "1") {
        const count = 275;
        $("#hint_id_number_of_pages").html(count + " words approx");
        return count;
      } else {
        var count = 275 * e.target.value;
        $("#hint_id_number_of_pages").html(count + " words approx");
        return count;
      }
    });
  }
  // execute on load
  words_1();
  words_2();

  // calculate approximate number of words according to spacing
  $("#id_spacing").mouseup(function spacing(e) {
    // get number of pages entered above.
    function count() {
      let count = $("#id_number_of_pages").val() * 275;
      return count;
    }

    var count = count();
    if (e.target.value == "single") {
      $("#hint_id_number_of_pages").html(count * 2 + " words approx");
    } else if (e.target.value == "double") {
      $("#hint_id_number_of_pages").html(count + " words approx");
    }
  });

  /* compute the price as the user types from number of pages*/

  // get the academic level selected by the user and display it on price panel
  $("#id_academic_level").mouseup(function (e) {
    $("#academic_level").html(e.target.value);
  });

  $("#id_subject_area").mouseup(function (e) {
    $("#subject_area").html(e.target.value);
  });

  // get the type of paper to displaying on price panel
  $("#id_type_of_paper").mouseup(function (e) {
    $("#type_of_paper").html(e.target.value);
  });

  // calculate deadline date according to clicked button

  // show the current date on load
  $("#deadline_count").html(Date);

  $(
    "#deadline_6, #deadline_12, #deadline_15, #deadline_24, #deadline_36, #deadline_48, #deadline_3, #deadline_5, #deadline_7, #deadline_10, #deadline_14, #deadline_30, #deadline_60"
  ).click(function () {
    // change deadline date according to specific deadline on button
    if (this.id == "deadline_6") {
      $("#deadline_count").html(
        new Date(Date.now() + 0.25 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_12") {
      $("#deadline_count").html(
        new Date(Date.now() + 0.5 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_15") {
      $("#deadline_count").html(
        new Date(Date.now() + 0.625 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_24") {
      $("#deadline_count").html(new Date(Date.now() + 1 * 24 * 60 * 60 * 1000));
    } else if (this.id == "deadline_36") {
      $("#deadline_count").html(
        new Date(Date.now() + 1.5 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_48") {
      $("#deadline_count").html(new Date(Date.now() + 2 * 24 * 60 * 60 * 1000));
    } else if (this.id == "deadline_3") {
      $("#deadline_count").html(new Date(Date.now() + 3 * 24 * 60 * 60 * 1000));
    } else if (this.id == "deadline_5") {
      $("#deadline_count").html(new Date(Date.now() + 5 * 24 * 60 * 60 * 1000));
    } else if (this.id == "deadline_7") {
      $("#deadline_count").html(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000));
    } else if (this.id == "deadline_10") {
      $("#deadline_count").html(
        new Date(Date.now() + 10 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_14") {
      $("#deadline_count").html(
        new Date(Date.now() + 14 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_30") {
      $("#deadline_count").html(
        new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
      );
    } else if (this.id == "deadline_60") {
      $("#deadline_count").html(
        new Date(Date.now() + 60 * 24 * 60 * 60 * 1000)
      );
    }
  });

  // ### more jquery goes here following the above pattern ###
});

// *** JavaScript ***
