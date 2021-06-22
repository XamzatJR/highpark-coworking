const phoneMask = IMask(document.getElementById("phone-number"), {
  mask: "+{7}(000)000-00-00",
});

let period;

$(window).scroll(function () {
  if ($(document).scrollTop() > 120) {
    $(".navbar").addClass("navbar-scroll");
  } else {
    $(".navbar").removeClass("navbar-scroll");
  }
});

$("#displayService").click(function (e) {
  $("#service").removeClass("hero-disabled");
});

$("#displayDateDaily").click(function (e) {
  $("#date").removeClass("hero-disabled");
  period = $(this).attr("value");
});

$("#displayDateMonthly").click(function (e) {
  $("#date").removeClass("hero-disabled");
  period = $(this).attr("value");
});

$("#displayLogin").click(function (e) {
  $("#login").removeClass("hero-disabled");
});

$("#register").submit(function (e) {
  e.preventDefault();
  const username = $("#username").val();
  const email = $("#email").val();
  const phoneNumber = $("#phone-number").val();
  const password = $("#password").val();
  let places = [];

  $(".marked").each(function () {
    places.push({ place: this.id });
  });

  axios
    .post("http://127.0.0.1:8000/auth/register", {
      fullname: username,
      email: email,
      phone: phoneNumber,
      password: password,
      date: { start: start_g, end: end_g },
      places: places,
    }) // TODO: Change address
    .then(function (response) {})
    .catch(function (error) {});
});
