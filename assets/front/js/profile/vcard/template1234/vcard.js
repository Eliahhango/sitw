'use strict';
function showSnackbar(message) {
    var x = document.getElementById("snackbar");
    x.className = "show";
    x.innerHTML = message;
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}
(function($) {

    //===== Prealoder
    $(window).on('load', function(event) {
        $('.preloader').delay(500).fadeOut('500');
    })

    // MagnificPopup js
    $(".img-popup").magnificPopup({
        type: "image",
         gallery: { 
          enabled: true 
        }
    });

    // Slick Slider js
    var sliderArrows = $('.portfolio-arrows');
    $('.portfolio-slider-one').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-chevron-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-chevron-right"></i></div>',
        rtl: dir == 2 ? true : false
    });
    var sliderArrows = $('.testimonial-arrows');
    $('.testimonial-slider-one').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2000,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-chevron-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-chevron-right"></i></div>',
        rtl: dir == 2 ? true : false
    });

    // lazy load init
    var lazyLoadInstance = new LazyLoad();
})(window.jQuery);