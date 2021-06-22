$(window).scroll(function () {
  if ($(document).scrollTop() > 120) {
    $(".navbar").addClass("navbar-scroll");
  } else {
    $(".navbar").removeClass("navbar-scroll");
  }
});

$("#register").submit(function (e) {
  e.preventDefault();

  $(".alert").remove();

  const username = $("#username").val();
  const email = $("#email").val();
  const phoneNumber = $("#phone-number").val();
  const password = $("#password").val();
  let places = [];

  $(".marked").each(function () {
    places.push({ place: this.id });
  });

  axios
    .post("/api/auth/register", {
      fullname: username,
      email: email,
      phone: phoneNumber,
      password: password,
      date: { start: start_g | null, end: end_g | null },
      places: places ?? [],
      period: period ?? null,
    })
    .then(function (response) {
      $("#register").append(
        info(
          `Письмо с подтверждением отправлено на почту ${response.data.email}`
        )
      );
    })
    .catch(function (error) {
      const msg = {
        email: "электронную почту",
        phone: "номер телефона",
        password: "пароль",
      };

      error.response.data.detail.forEach((element) => {
        if (element.loc.length == 2) {
          $("#register").append(
            danger("Необходимо указать " + msg[element.loc[1]])
          );
        }
      });
    });
});
