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

  $("#bid").click(function () {
    $("#bid").text("Bidding...");
  });

  $("#unbid").click(function () {
    $("#unbid").text("Unbidding...");
  });

  $("input").focus(function () {
    $("#upload").text("Upload");
  });

  $("#upload").click(function () {
    $("#upload").text("Uploading...");
  });
});

// ** JavaScript **
/*--------------------settings page---------------------------*/

function deleteForm() {
  var blur = document.getElementById("blur");
  blur.classList.toggle("active");

  var popup = document.getElementById("popup");
  popup.classList.toggle("active");
}

// get rating and present into stars config
const stars = document.getElementById("starScore");

const handleStarRating = (score) => {
  const starChildren = stars.children;

  for (let i = 0; i < starChildren.length; i++) {
    if (i <= score) {
      starChildren[i].classList.add("checked");
    } else {
      starChildren[i].classList.remove("checked");
    }
  }
};

const score = $("#avgScore").text();

if (score <= 1.5) {
  handleStarRating(1);
} else if (score <= 2.4) {
  handleStarRating(2);
} else if (score <= 3.4) {
  handleStarRating(3);
} else if (score <= 4.4) {
  handleStarRating(4);
} else if (score <= 5) {
  handleStarRating(5);
}
/*--------------------settings page---------------------------*/
// chart config
