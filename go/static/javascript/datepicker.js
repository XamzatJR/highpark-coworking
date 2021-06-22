let start_g;
let end_g;

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
      $(".marked").removeClass("marked");
      $(".occupied").removeClass("occupied");
      start = `${start._d.getFullYear()}-${
        start._d.getMonth() + 1
      }-${start._d.getDate()}`;
      end = `${end._d.getFullYear()}-${
        end._d.getMonth() + 1
      }-${end._d.getDate()}`;
      start_g = start;
      end_g = end;
      axios
        .post("http://127.0.0.1:8000/free-places", { start: start, end: end }) // TODO: Change address
        .then(function (response) {
          $(".chair-h").addClass("free");
          $(".chair-h2").addClass("free");
          $(".chair-v").addClass("free");
          response.data.places.forEach((element) => {
            const el = $(`#${element.place}`);
            el.removeClass("free").addClass("occupied");
            el.popover({
              trigger: "hover",
              title: "Дата аренды",
              content: `${element.start.replace(
                /-/g,
                "."
              )} - ${element.end.replace(/-/g, ".")}`,
            });
          });
          $("#tables").removeClass("hero-disabled");
          window.location.href = "#tables";
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  );
});

$("body").on("click", ".free", function () {
  $(this).toggleClass("marked");
});
