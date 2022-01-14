// calculate approximate number of words according to spacing
$("#id_spacing").mouseup(function spacing(e) {
  return e.target.value;
});

// compute the price as the user types from number of pages
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
// $.each(
//   $("deadline_time").click(function () {
//     if ($(this).text() == "36 Hours") {
//       console.log("yes");
//     } else {
//       console.log("no");
//     }
//   })
// );

// calculate deadline date according to selected date
$(document).ready(function () {
  $("#deadline_count").html(Date);
});

$("#deadline_6").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 0.25 * 24 * 60 * 60 * 1000));
});

$("#deadline_12").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 0.5 * 24 * 60 * 60 * 1000));
});

$("#deadline_15").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 0.625 * 24 * 60 * 60 * 1000));
});

$("#deadline_24").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 1 * 24 * 60 * 60 * 1000));
});

$("#deadline_36").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 1.5 * 24 * 60 * 60 * 1000));
});

$("#deadline_48").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 2 * 24 * 60 * 60 * 1000));
});

$("#deadline_3").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 3 * 24 * 60 * 60 * 1000));
});

$("#deadline_5").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 5 * 24 * 60 * 60 * 1000));
});

$("#deadline_7").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000));
});

$("#deadline_10").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 10 * 24 * 60 * 60 * 1000));
});

$("#deadline_14").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 14 * 24 * 60 * 60 * 1000));
});

$("#deadline_40").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 40 * 24 * 60 * 60 * 1000));
});

$("#deadline_60").click(function (e) {
  $("#deadline_count").html(new Date(Date.now() + 60 * 24 * 60 * 60 * 1000));
});
// id_number_of_pages
// hint_id_number_of_pages
// hint_id_deadline
