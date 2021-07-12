const placePopover = (title, start, end) => ({
  trigger: "hover",
  title: title,
  content: `${start.replace(/-/g, ".")} - ${end.replace(/-/g, ".")}`,
});

const locale = {
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
};

const daterangeDay = () => {
  let tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);

  $('input[name="daterange"]').daterangepicker(
    {
      autoApply: true,
      locale: locale,
      opens: "left",
      startDate: tomorrow,
      endDate: tomorrow,
      minDate: tomorrow,
      maxSpan: {
        days: 30,
      },
    },
    function (start, end, label) {
      start_g = `${start._d.getFullYear()}-${
        start._d.getMonth() + 1
      }-${start._d.getDate()}`;
      end_g = `${end._d.getFullYear()}-${
        end._d.getMonth() + 1
      }-${end._d.getDate()}`;
      getPlaces();
    }
  );
};

const daterangeMonth = () => {
  let tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  $("#month").removeAttr("style");
  $('input[name="daterange"]').daterangepicker({
    singleDatePicker: true,
    autoApply: true,
    locale: locale,
    opens: "left",
    startDate: tomorrow,
    endDate: tomorrow,
    minDate: tomorrow,
  });
};

$("body").on("click", ".free", function () {
  $(this).toggleClass("not-paid");
});

function getPlaces() {
  $(".paid").removeClass("paid");
  $(".not-paid").removeClass("not-paid");
  $(".occupied").removeClass("occupied");

  axios
    .post("/api/free-places", { start: start_g, end: end_g })
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

      response.data.user_places.forEach((element) => {
        const el = $(`#${element.place}`);
        if (element.paid_for == true) {
          el.removeClass("free").addClass("paid");
          el.popover(
            placePopover("Вы арендовали - оплачено", element.start, element.end)
          );
        } else {
          el.removeClass("free").addClass("not-paid");
          el.popover(
            placePopover(
              "Вы арендовали - не оплачено",
              element.start,
              element.end
            )
          );
        }
      });

      $("#tables").removeClass("hero-disabled");
      window.location.href = "#tables";
    })
    .catch(function (error) {});
}
