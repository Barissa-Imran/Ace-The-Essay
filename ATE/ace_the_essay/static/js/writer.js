// applicant dropdown button

$(document).ready(function () {
  $(".dropdown-toggle").dropdown();
});

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
