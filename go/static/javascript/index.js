let period;

$(window).scroll(function () {
    if ($(document).scrollTop() > 120) {
        $('.navbar').addClass('navbar-scroll');
    } else {
        $('.navbar').removeClass('navbar-scroll');
    }
});

$('#displayService').click(function (e) {
    $('#service').removeClass('hero-disabled');
});

$('#displayDateDaily').click(function (e) {
    $('#date').removeClass('hero-disabled');
    period = $(this).attr('value');
});

$('#displayDateMonthly').click(function (e) {
    $('#date').removeClass('hero-disabled')
    period = $(this).attr('value')
})

$('#displayLogin').click(function (e) {
    $('#login').removeClass('hero-disabled')
})
