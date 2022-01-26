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

  $('#bid').click(function (){
    $("#bid").text("Bidding...")
  });

  $("input").focus(function () {
    $("#upload").text("Upload");
  });

  $('#upload').click(function (){
    $("#upload").text("Uploading...")
  });

});

// ** JavaScript **
/*--------------------settings page---------------------------*/ 

function deleteForm() {
  var blur = document.getElementById("blur");
  blur.classList.toggle("active");

  var popup = document.getElementById("popup");
  popup.classList.toggle("active");
};

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
