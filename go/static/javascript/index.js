const phoneMask = IMask(document.getElementById("phone-number"), {
  mask: "+{7}(000)000-00-00",
});

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
  $("#loginHero").removeClass("hero-disabled");
});
