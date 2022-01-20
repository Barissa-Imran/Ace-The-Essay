// ****  JQuery  ***
$(document).ready(function () {
  // applicant dropdown button
  $(".dropdown-toggle").dropdown();

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

  /*---------------------project detail page-------------------------- */

  // prepopulate bid form fields with data.
  let project = $("h2").html();
  $("#id_project option").html(project);

  let user = $("#username").html();
  $("#id_made_by option").html(user);

  // alert(test);
});

// $(document).ready(function () {
//   $(".bid").click(function () {
//     $.ajax({
//       url: "",
//       type: "GET",
//       data: {
//         button_text: $(this).text(),
//       },
//       sucess: function (response) {
//         $(".bid").text(response.seconds);
//       },
//     });
//     alert("Bid sent seccessfully");
//   });
// });
