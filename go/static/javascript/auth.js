let start_g = null;
let end_g = null;
let period;

const info = (message) =>
  `<div class="alert alert-primary mt-3" role="alert">${message}</div>`;

const danger = (message) =>
  `<div class="alert alert-danger mt-3" role="alert">${message}</div>`;

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
      date: { start: start_g, end: end_g | null },
      places: places,
      period: period,
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

$("#login").submit(function (e) {
  $(".alert").remove();

  e.preventDefault();
  axios
    .post("/api/auth/login", {
      email: $("#email").val(),
      password: $("#password").val(),
    })
    .then(function (response) {
      window.location = "/profile";
    })
    .catch(function (e) {
      $("#login").append(danger("Не удалось войти"));
    });
});
