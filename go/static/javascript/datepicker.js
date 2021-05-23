$(function () {
  let tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  $('input[name="daterange"]').daterangepicker(
    {
      autoApply: true,
      locale: {
        format: "DD.MM.YYYY",
        separator: " - ",
        applyLabel: "Сохранить",
        cancelLabel: "Назад",
        daysOfWeek: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
        monthNames: [
          "Январь",
          "Февраль",
          "Март",
          "Апрель",
          "Май",
          "Июнь",
          "Июль",
          "Август",
          "Сентябрь",
          "Октябрь",
          "Ноябрь",
          "Декабрь",
        ],
        firstDay: 1,
      },
      opens: "left",
      startDate: tomorrow,
      endDate: tomorrow,
      minDate: tomorrow,
      maxSpan: {
        days: 30,
      },
    },
    function (start, end, label) {
      $("#places").removeClass("hero-disabled");
      location.href = "#places"
    }
  );
});
