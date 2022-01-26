// show login popup
function login() {
  var blur = document.getElementById("blur");
  blur.classList.toggle("active");

  var popup = document.getElementById("popup");
  popup.classList.toggle("active");
}

$(document).ready(function () {
  // change login button text
  $("input").focus(function () {
    $("#login-btn").text("Login");
    $("#send-btn").text("Send");
  });

  $("#login-btn").click(function () {
    $(this).text("Logging in...");
  });

  $("#send-btn").click( function (){
    $(this).text("Sending...");
  });
});

//   var csrf = $("input[name=csrfmiddlewaretoken]").val();

// $.ajax({
//   url: "auth/admin-landing",
//   type: "post",
//   data: {
//     username: $("#username").val(),
//     password: $("#password").val(),
//     csrfmiddlewaretoken: csrf,
//   },
// });

// change login button text on click
