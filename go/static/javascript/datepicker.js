const placePopover = (title, start, end) => ({
  trigger: "hover",
  title: title,
  content: `${start.replace(/-/g, ".")} - ${end.replace(/-/g, ".")}`,
});

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
        .post("/api/free-places", { start: start, end: end })
        .then(function (response) {
          $(".chair-h").addClass("free");
          $(".chair-h2").addClass("free");
          $(".chair-v").addClass("free");
          for (let index = 1; index < 33; index++) {
            const el = $(`#${index}`);
            el.popover("dispose");
          }

          response.data.places.forEach((element) => {
            const el = $(`#${element.place}`);
            el.removeClass("free").addClass("occupied");
            el.popover(placePopover("Дата аренды", element.start, element.end));
          });

          response.data.paid_for.forEach((element) => {
            const el = $(`#${element.place}`);
            el.removeClass("free").addClass("marked");
            el.popover(
              placePopover(
                "Вы арендовали - оплачено",
                element.start,
                element.end
              )
            );
          });

          response.data.not_paid_for.forEach((element) => {
            const el = $(`#${element.place}`);
            el.removeClass("free").addClass("marked");
            el.popover(
              placePopover(
                "Вы арендовали - не оплачено",
                element.start,
                element.end
              )
            );
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
