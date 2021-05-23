let period;

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

$("#displayAuth").click(function (e) {
  $("#auth").removeClass("hero-disabled");
});
