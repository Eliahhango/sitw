'use strict';
function showSnackbar(message) {
    var x = document.getElementById("snackbar");
    x.className = "show";
    x.innerHTML = message;
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}
(function($) {
    // MagnificPopup js
    $(".img-popup").magnificPopup({
        type: "image",
         gallery: { 
          enabled: true 
        }
    });
    //===== Magnific-popup js
    $('.video-popup').magnificPopup({
        type: 'iframe',
        removalDelay: 300,
        mainClass: 'mfp-fade'
    });
    // Slick Slider js
    var sliderArrows = $('.service-arrows');

    
    $('.service-slider-one').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
        variableWidth: true,
		slidesToShow: 2,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });


    $('.service-slider-two').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 2,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });

    $('.service-slider-three').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });


    var sliderArrows = $('.project-arrows');
    $('.project-slider-one').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
        variableWidth: true,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });
    $('.project-slider-two').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });
    $('.project-slider-three').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 2,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });
    $('.project-slider-four').slick({
		dots: false,
		arrows: true,
        infinite: true,
		autoplaySpeed: 2500,
        autoplay: false,
        appendArrows: sliderArrows,
        variableWidth: true,
        centerMode: true,
		slidesToShow: 2,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
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
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });
    $('.testimonial-slider-two').slick({
		dots: true,
		arrows: false,
        infinite: true,
		autoplaySpeed: 2000,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });
    $('.testimonial-slider-three').slick({
		dots: false,
		arrows: false,
        infinite: true,
		speed: 700,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });

    $('.video-slider-one').slick({
		dots: false,
		arrows: false,
        infinite: true,
		speed: 700,
        autoplay: false,
        appendArrows: sliderArrows,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });

    $('.video-slider-two').slick({
		dots: true,
		arrows: false,
        infinite: true,
		autoplaySpeed: 2000,
        autoplay: false,
        appendArrows: sliderArrows,
        variableWidth: true,
        centerMode: true,
		slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
		nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        rtl: dir == 2 ? true : false
    });

    // lazy load init
    var lazyLoadInstance = new LazyLoad();

})(window.jQuery);


//===== Prealoder
$(window).on('load', function(event) {
    $('.preloader').delay(500).fadeOut('500');
})