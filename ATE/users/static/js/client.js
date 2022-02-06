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
  /*DATA*/
  // Technical subjects
  var $technicalSubjects = [
    ("Aeronautics", "Aeronautics"),
    ("Architecture", "Architecture"),
    ("Astronomy", "Astronomy"),
    ("Aviation", "Aviation"),
    ("Bio-Medical Sciences", "Bio-Medical Sciences"),
    ("Biochemistry", "Biochemistry"),
    ("Biology", "Biology"),
    ("Building & Construction", "Building & Construction"),
    ("Chemistry", "Chemistry"),
    ("Computers", "Computers"),
    ("Economics", "Economics"),
    ("Engineering", "Engineering"),
    ("English", "English"),
    ("Food-Nutrition", "Food-Nutrition"),
    ("Healthcare", "Healthcare"),
    ("History", "History"),
    ("Investment", "Investment"),
    ("Law", "Law"),
    ("Legal Issues", "Legal Issues"),
    ("Linguistics", "Linguistics"),
    ("Literature", "Literature"),
    ("Logistics", "Logistics"),
    ("Management", "Management"),
    ("Marketing", "Marketing"),
    ("Mathematics", "Mathematics"),
    ("Medicine", "Medicine"),
    ("Military Studies", "Military Studies"),
    ("Music", "Music"),
    ("Nursing", "Nursing"),
    ("Nutrition", "Nutrition"),
    ("Other(Not Listed)", "Other(Not Listed)"),
    ("Pedagogy", "Pedagogy"),
    ("Pharmacology", "Pharmacology"),
    ("Physical-Education", "Physical-Education"),
    ("Physics", "Physics"),
    ("Psychology", "Psychology"),
    ("Quantity Survey", "Quantity Survey"),
    ("Statistics", "Statistics"),
  ];
  //theoretical subjects
  var $theoreticalSubjects = [
    "Accounting",
    ("Anthropology", "Anthropology"),
    ("Arts", "Arts"),
    ("Auditing", "Auditing"),
    ("Business", "Business"),
    ("Childcare", "Childcare"),
    ("Communication and Media", "Communication and Media"),
    ("Company Anlysis", "Company Analysis"),
    ("Counseling", "Counseling"),
    ("Criminology", "Criminology"),
    ("Education", "Education"),
    ("English", "English"),
    ("Environmental-Studies", "Environmental-Studies"),
    ("Ethics", "Ethics"),
    ("Ethnic-Studies", "Ethnic-Studies"),
    ("finance", "finance"),
    ("Food-Nutrition", "Food-Nutrition"),
    ("History", "History"),
    ("Investment", "Investment"),
    ("Law", "Law"),
    ("Legal Issues", "Legal Issues"),
    ("Linguistics", "Linguistics"),
    ("Literature", "Literature"),
    ("Logistics", "Logistics"),
    ("Management", "Management"),
    ("Marketing", "Marketing"),
    ("Military Studies", "Military Studies"),
    ("Nutrition", "Nutrition"),
    ("Other(Not Listed)", "Other(Not Listed)"),
    ("Philosophy", "Philosophy"),
    ("Physical Problems", "Physical Problems"),
    ("Political Science", "Political Science"),
    ("Politics", "Politics"),
    ("Procurement", "Procurement"),
    ("Religion", "Religion"),
    ("Sociology", "Sociology"),
    ("Sport", "Sport"),
    ("Taxation Theory, Practice & Law", "Taxation Theory, Practice & Law"),
    ("Teacher's Career", "Teacher's Career"),
    ("Tourism", "Tourism"),
    ("Trade", "Trade"),
  ];
  /*DATA*/

  // load values on load in project update page
  $("#academic_level").html($("#id_academic_level").val());
  $("#type_of_paper").html($("#id_type_of_paper").val());
  $("#subject_area").html($("#id_subject_area").val());
  $("#number_of_pages").html($("#id_number_of_pages").val() + " page(s)");
  $("#total").html("$" + $("#id_price").val());

  // get entered data and display on price panel (computed)
  $("#id_academic_level").mouseup(function (e) {
    $("#academic_level").html(e.target.value);
  });
  $("#id_type_of_paper").mouseup(function (e) {
    $("#type_of_paper").html(e.target.value);
  });

  // main function
  function subRate() {
    // mouseup event to get subject area value
    $("#id_subject_area").mouseup(function (e) {
      $("#subject_area").html(e.target.value);

      // compute price according to subject selected
      function sub(value) {
        $technicalSubjects.forEach((subject) => {
          if (value === subject) {
            var $rate = 40;
            $("#total").text("$40");
            return $rate;
          } else {
            $theoreticalSubjects.forEach((subject) => {
              if (value === subject) {
                var $rate = 20;
                $("#total").text("$20");
                return $rate;
              }
            });
          }
        });
      }
      sub(e.target.value);
    });

    var value = $("#id_subject_area").val();
  }

  subRate();

  // compute price according to subject selected
  function sub(value) {
    let $rate = 0;
    $technicalSubjects.forEach((subject) => {
      if (value === subject) {
        $rate = 40;
      } else {
        $theoreticalSubjects.forEach((subject) => {
          if (value === subject) {
            $rate = 20;
          }
        });
      }
    });
    return $rate;
  }

  // number of pages config------------
  $("#id_number_of_pages").keyup(function (e) {
    $("#number_of_pages").html(e.target.value + " pages(s)");

    // run function to get subject rate on click
    var $subjectVal = $("#id_subject_area").val();
    var $subjectRate = sub($subjectVal);

    // calculate the approximate number of words and price
    if (e.target.value === "1") {
      var count = 275;
      // multiply by price
      var $price = $subjectRate * e.target.value;
      $("#total").html("$" + $price);
      $("#hint_id_number_of_pages").html(count + " words approx");
      return count;
    } else {
      var count = 275 * e.target.value;
      // multiply by price
      var $price = $subjectRate * e.target.value;
      $("#total").html("$" + $price);
      $("#hint_id_number_of_pages").html(count + " words approx");
      return count;
    }
  });

  $("#id_number_of_pages").mouseup(function (e) {
    $("#number_of_pages").html(e.target.value + " pages(s)");
    // run function to get subject rate on click
    var $subjectVal = $("#id_subject_area").val();
    var $subjectRate = sub($subjectVal);

    // calculate the approximate number of words
    if (e.target.value === "1") {
      var count = 275;
      // multiply by price
      var $price = $subjectRate * e.target.value;
      $("#total").html("$" + $price);
      $("#hint_id_number_of_pages").html(count + " words approx");
      return count;
    } else {
      var count = 275 * e.target.value;
      // multiply by price
      var $price = $subjectRate * e.target.value;
      $("#total").html("$" + $price);
      $("#hint_id_number_of_pages").html(count + " words approx");
      return count;
    }
  });

  // calculate approximate number of words according to spacing
  $("#id_spacing").mouseup(function spacing(e) {
    // run function to get subject rate on click
    var $subjectVal = $("#id_subject_area").val();
    var $subjectRate = sub($subjectVal);
    var $pages = $("#id_number_of_pages").val();

    // get number of pages entered above.
    function count() {
      let count = $("#id_number_of_pages").val() * 275;
      return count;
    }

    var count = count();
    if (e.target.value === "single") {
      $("#hint_id_number_of_pages").html(count * 2 + " words approx");
      // multiply price by 2, #pages
      $("#total").html("$" + 2 * $subjectRate * $pages);
    } else if (e.target.value === "double") {
      $("#hint_id_number_of_pages").html(count + " words approx");
      // price back to default
      $("#total").html("$" + $subjectRate * $pages);
    }
  });

  $("#id_spacing").click(function spacing(e) {
    // run function to get subject rate on click
    var $subjectVal = $("#id_subject_area").val();
    var $subjectRate = sub($subjectVal);
    var $pages = $("#id_number_of_pages").val();

    // get number of pages entered above.
    function count() {
      let count = $("#id_number_of_pages").val() * 275;
      return count;
    }

    var count = count();
    if (e.target.value === "single") {
      $("#hint_id_number_of_pages").html(count * 2 + " words approx");
      // multiply price by 2
      // multiply price by 2, #pages
      $("#total").html("$" + 2 * $subjectRate * $pages);
    } else if (e.target.value === "double") {
      $("#hint_id_number_of_pages").html(count + " words approx");
      // price back to default
      $("#total").html("$" + $subjectRate * $pages);
    }
  });

  // calculate deadline date according to clicked button

  // show the current date on load
  $("#deadline_count").html(Date);

  $(
    "#deadline_6, #deadline_12, #deadline_15, #deadline_24, #deadline_36, #deadline_48, #deadline_3, #deadline_5, #deadline_7, #deadline_10, #deadline_14, #deadline_30, #deadline_60"
  ).click(function () {
    // run function to get subject rate on click
    var $subjectVal = $("#id_subject_area").val();
    var $subjectRate = sub($subjectVal);
    var $pages = $("#id_number_of_pages").val();
    var $spacing = $("#id_spacing").val();

    // get multiplier from spacing
    function product() {
      if ($spacing === "single") {
        return 2;
      } else if ($spacing === "double") {
        return 1;
      }
    }

    let $multi = product();
    var $fprice = $subjectRate * $pages * $multi;

    // change deadline date according to specific deadline on button
    if (this.id === "deadline_6") {
      $("#deadline_count").html(
        new Date(Date.now() + 0.25 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (27.5 / 100) * $fprice));
    } else if (this.id === "deadline_12") {
      $("#deadline_count").html(
        new Date(Date.now() + 0.5 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (25 / 100) * $fprice));
    } else if (this.id === "deadline_15") {
      $("#deadline_count").html(
        new Date(Date.now() + 0.625 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (22.5 / 100) * $fprice));
    } else if (this.id === "deadline_24") {
      $("#deadline_count").html(new Date(Date.now() + 1 * 24 * 60 * 60 * 1000));
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (20 / 100) * $fprice));
    } else if (this.id === "deadline_36") {
      $("#deadline_count").html(
        new Date(Date.now() + 1.5 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (17.5 / 100) * $fprice));
    } else if (this.id === "deadline_48") {
      $("#deadline_count").html(new Date(Date.now() + 2 * 24 * 60 * 60 * 1000));
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (15 / 100) * $fprice));
    } else if (this.id === "deadline_3") {
      $("#deadline_count").html(new Date(Date.now() + 3 * 24 * 60 * 60 * 1000));
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (12.5 / 100) * $fprice));
    } else if (this.id === "deadline_5") {
      $("#deadline_count").html(new Date(Date.now() + 5 * 24 * 60 * 60 * 1000));
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (10 / 100) * $fprice));
    } else if (this.id === "deadline_7") {
      $("#deadline_count").html(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000));
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (7.5 / 100) * $fprice));
    } else if (this.id === "deadline_10") {
      $("#deadline_count").html(
        new Date(Date.now() + 10 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (5 / 100) * $fprice));
    } else if (this.id === "deadline_14") {
      $("#deadline_count").html(
        new Date(Date.now() + 14 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (2.5 / 100) * $fprice));
    } else if (this.id === "deadline_30") {
      $("#deadline_count").html(
        new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (2.5 / 100) * $fprice));
    } else if (this.id === "deadline_60") {
      $("#deadline_count").html(
        new Date(Date.now() + 60 * 24 * 60 * 60 * 1000)
      );
      //add the price by 2.5% from <14 days
      $("#total").html("$" + ($fprice + (2.5 / 100) * $fprice));
    }
  });

  // price computation

  // Place order method-----------------------------

  $("select").focus(function () {
    $("#order").text("Order");
  });

  // get csrf token for post request
  var csrf = $("input[name=csrfmiddlewaretoken]").val();

  // hide price and deadline fields from user
  $("#div_id_price").addClass("d-none");
  $("#div_id_deadline").addClass("d-none");

  // Form submission config for place order page
  $("#projectorder-create-form").submit(function (e) {
    e.preventDefault();
    $("#order").text("Ordering...");
    // get deadline string
    var $deadline = $("#deadline_count").text();

    // get the date from js format to django appropriate fmt
    function converter(deadline) {
      var $dateArray = deadline.split(" ");

      // convert month initials to integer
      function month(month) {
        if (month === "Jan") {
          return "01";
        } else if (month === "Feb") {
          return "02";
        } else if (month === "Mar") {
          return "03";
        } else if (month === "Apr") {
          return "04";
        } else if (month === "May") {
          return "05";
        } else if (month === "Jun") {
          return "06";
        } else if (month === "Jul") {
          return "07";
        } else if (month === "Aug") {
          return "08";
        } else if (month === "Sep") {
          return "09";
        } else if (month === "Oct") {
          return "10";
        } else if (month === "Nov") {
          return "11";
        } else if (month === "Dec") {
          return "12";
        }
      }

      var $converted =
        $dateArray[3] +
        "-" +
        month($dateArray[1]) +
        "-" +
        $dateArray[2] +
        " " +
        $dateArray[4];

      return $converted;
    }

    var $fdeadline = converter($deadline);

    // get final price
    var $price = $("#total").text();
    var $finalPrice = $price.replace("$", "");

    // parse the data from above into the form
    $.ajax({
      url: "",
      type: "POST",
      data: {
        csrfmiddlewaretoken: csrf,
        academic_level: $("#id_academic_level").val(),
        type_of_paper: $("#id_type_of_paper").val(),
        subject_area: $("#id_subject_area").val(),
        title: $("#id_title").val(),
        paper_instructions: $("#id_paper_instructions").val(),
        additional_materials: $("#id_additional materials").val(),
        paper_format: $("#id_paper_format").val(),
        number_of_pages: $("#id_number_of_pages").val(),
        spacing: $("#id_spacing").val(),
        currency: $("#id_currency").val(),
        deadline: $fdeadline,
        price: $finalPrice,
      },
      success: function (response) {
        window.location.href= "http://acetheessayapp.herokuapp.com/auth/client/projects";
      },
    });
  });

  /*--------------------client detail page---------------------------*/

  // mark a project as complete
  var csrf = $("input[name=csrfmiddlewaretoken]").val();

  $("#markcomplete").click(function () {
    $.ajax({
      url: "",
      type: "post",
      data: {
        csrfmiddlewaretoken: csrf,
      },
    });
  });

  // ### more jquery goes here following the above pattern ###
});

/*** JavaScript ***/

/*--------------------settings page---------------------------*/

function deleteForm() {
  var blur = document.getElementById("blur");
  blur.classList.toggle("active");

  var popup = document.getElementById("popup");
  popup.classList.toggle("active");
}
