(function ($) {
    'use strict';

    /*---------------------
    === Document Ready  ===
    ----------------------*/
    $(document).ready(function () {
        // Easy Pie Chart
        $('.skill-section').on('inview', function (event, isInView) {
            if (isInView) {
                $(this).find('.chart').each(function () {
                    $(this).easyPieChart({
                        size: 200,
                        lineWidth: 8,
                        scaleLength: 0,
                        trackColor: '#7936ff91',
                    });
                });
                $(this).unbind('inview');
            }
        });

        // Project Section
        $('.project-section').imagesLoaded(function () {
            const items = $('.project-loop');

            items.isotope('layout');
            // items on button click
            $('.project-filter').on('click', 'li', function (e) {
                const filterValue = $(this).attr('data-filter');
                items.isotope({
                    filter: filterValue
                });
            });
            // menu active class
            $('.project-filter li').on('click', function (event) {
                $('.project-filter .active').removeClass('active');
                $(this).addClass('active');

                event.preventDefault();
            });
        });

        //  Counter Up
        $('.counter-item').on('inview', function (event, isInView) {
            if (isInView) {
                $(this).find('.counter').each(function () {
                    $(this).prop('Counter', 0).animate({
                        Counter: $(this).text()
                    }, {
                        duration: 3000,
                        easing: 'swing',
                        step: function (now) {
                            $(this).text(Math.ceil(now));
                        }
                    });
                });
                $(this).unbind('inview');
            }
        });

        $('.testimonial-slider').slick({
            dots: false,
            arrows: false,
            infinite: true,
            speed: 300,
            slidesToShow: 3,
            slidesToScroll: 1,
            rtl: rtl == 1 ? true : false,
            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        slidesToShow: 2,
                    }
                },
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                    }
                }
            ]
        });

        // Language Dropdown
        $('.selected-flag').on('click', function (e) {
            e.preventDefault();

            $('.language-list').toggleClass('show-list');
        });
    });

    /*---------------------
    === Window Scroll  ===
    ----------------------*/
    $(window).on('scroll', function () {
        var header = $(".template-header");

        var scroll = $(window).scrollTop();

        if (scroll >= 10) {
            header.addClass("scroll-on");
        } else {
            header.removeClass("scroll-on");
        }
    });

    /*------------------
    === Window Load  ===
    --------------------*/
    $(window).on('load', function () {
    });
    // lazy load init
    var lazyLoadInstance = new LazyLoad();
})(jQuery);

$(".language-dropdown").on("click", ".dropdown-toggle", function(e) { 
    e.preventDefault();
    $(this).parent().addClass("show");
    $(this).attr("aria-expanded", "true");
    $(this).next().addClass("show"); 
});