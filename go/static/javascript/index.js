const info = (message) =>
  `<div class="alert alert-primary mt-3" role="alert">${message}</div>`;

const danger = (message) =>
  `<div class="alert alert-danger mt-3" role="alert">${message}</div>`;

const phoneMask = IMask(document.getElementById("phone-number"), {
  mask: "+{7}(000)000-00-00",
});

let period;

$("#displayService").click(function (e) {
  $("#service").removeClass("hero-disabled");
});

$("#displayDateDaily").click(function (e) {
  $("#date").removeClass("hero-disabled");
  period = "day";
});

$("#displayDateMonthly").click(function (e) {
  $("#date").removeClass("hero-disabled");
  period = "month";
});

$("#displayLogin").click(function (e) {
  $("#login").removeClass("hero-disabled");
});