$("#displayLoginForm").click((e) => {
  e.preventDefault()
  $(this).parent(".registration-form").hide()
  $("#displayRegisterForm").parent(".registration-form").show()
})


$("#displayRegisterForm").click((e) => {
  e.preventDefault()
  $(this).parent(".registration-form").hide()
  $("#displayLoginForm").parent(".registration-form").show()
})

$("#displayService").click((e) => $("#service").removeClass("hero-disabled"))

$("#displayDateDaily").click((e)  => {
  $("#date").removeClass("hero-disabled");
  period = "day";
});

$("#displayDateMonthly").click((e) => {
  $("#date").removeClass("hero-disabled");
  period = "month";
});

$("#displayLogin").click((e) => $("#loginHero").removeClass("hero-disabled"));
