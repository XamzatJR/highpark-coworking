$("#displayService").click((e) => $("#service").removeClass("hero-disabled"));

$("#displayDateDaily").click((e) => {
  $("#date").removeClass("hero-disabled");
  period = "day";
  daterangeDay();
});

$("#displayDateMonthly").click((e) => {
  $("#date").removeClass("hero-disabled");
  period = "month";
  daterangeMonth();
});

$("#displayTables").click((e) => {
  e.preventDefault();
  $(".alert").remove();
  if ($("#month").val() == "") {
    $("#dateForm").append(danger("Выберите количество месяцев"));
  } else {
    $("#tables").removeClass("hero-disabled");
    let date = $('input[name="daterange"]').val().split(".");
    date = new Date(date[2], date[1] - 1, date[0]);
    start_g = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    date.setDate(date.getDate() + (30 * $("#month").val()));
    end_g = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    getPlaces()
    window.location.href = "#tables";
  }
});

$("#displayLogin").click((e) => $("#loginHero").removeClass("hero-disabled"));
