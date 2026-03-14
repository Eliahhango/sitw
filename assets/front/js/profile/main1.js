(function ($) {
    'use strict';

    // ===== Main Menu
    function mainMenu() {
        const navbarToggler = $('.navbar-toggler'),
            navMenu = $('.nav-menu'),
            mobilePanel = $('.mobile-slide-panel'),
            mobilePanelMenu = $('.mobile-menu'),
            mobileOverly = $('.panel-overlay'),
            navClose = $('.panel-close');

        // Show Mobile Slide Panel
        navbarToggler.on('click', function (e) {
            e.preventDefault();
            mobilePanel.toggleClass('panel-on');
        });

        // Close Mobile Slide Panel
        navClose.add(mobileOverly).on('click', function (e) {
            e.preventDefault();
            mobilePanel.removeClass('panel-on');
        });

        // Adds toggle button to li items that have children
        navMenu.find('li a').each(function () {
            if ($(this).next().length > 0) {
                $(this).append('<span class="dd-trigger"><i class="fas fa-angle-down"></i></span>');
            }
        });

        mobilePanelMenu.find('li a').each(function () {
            if ($(this).next().length > 0) {
                $(this).append('<span class="dd-trigger"><i class="fas fa-angle-down"></i></span>');
            }
        });

        // Expands the dropdown menu on each click
        mobilePanelMenu.find('.dd-trigger').on('click', function (e) {
            e.preventDefault();
            $(this).parent().parent('li').children('ul.sub-menu').stop(true, true).slideToggle(350);
            $(this).toggleClass('sub-menu-opened');
        });

        // One Page Nav animation
        $('a[href*="#"]').not('[href="#"]').not('[href="#0"]').click(function (event) {
            if (
                location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') &&
                location.hostname == this.hostname
            ) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');

                if (target.length) {

                    event.preventDefault();
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 1000, function () {

                        var $target = $(target);
                        $target.focus();

                        if ($target.is(":focus")) {
                            return false;
                        } else {
                            $target.attr('tabindex', '-1');
                            $target.focus();
                        };
                    });
                }
            }
        });
    }

    // ===== Testimonials Slider One
    function testimonialActive() {
        const slider = $('.testimonial-slider');

        slider.slick({
            infinite: true,
            dots: false,
            arrows: false,
            speed: 500,
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay: false,
            autoplaySpeed: 5000,
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
    }

    // ===== Counter Up
    function counterUp() {
        $('.counter-box, .single-progress-bar').on('inview', function (event, isInView) {
            if (isInView) {
                $(this).find('.count').each(function () {
                    var $this = $(this);
                    $({
                        Counter: 0
                    }).animate({
                        Counter: $this.text()
                    }, {
                        duration: 3000,
                        easing: 'swing',
                        step: function () {
                            $this.text(Math.ceil(this.Counter));
                        },
                    });
                });
                $(this).unbind('inview');
            }
        });
    }

    // ===== Progress bar
    function progressBar() {
        $('.progress-bars').on('inview', function (event, isInView) {
            if (isInView) {
                $(this).find('.single-progress-bar').each(function () {
                    const percentage = $(this).data('percentage'),
                        lineInner = $(this).find('.line'),
                        widthCss = percentage + '%';

                    lineInner.width(widthCss);
                });
                $(this).unbind('inview');
            }
        });
    }

    // ===== Active Isotope
    function activeIsotope() {
        var items = $('.filter-items').isotope();

        // items on button click
        $('.portfolio-filter li').on('click', 'a', function (e) {
            var filterValue = $(this).attr('data-filter');
            items.isotope({
                filter: filterValue,
                isOriginLeft: rtl == 1 ? false : true,
            });
        });
        // menu active class
        $('.portfolio-filter li a').on('click', function (event) {
            $('.portfolio-filter .filter-active').removeClass('filter-active');
            $(this).addClass('filter-active');

            event.preventDefault();
        });
    }

    // ==== Nice Select
    function activeNiceSelect() {
        $('select').niceSelect();
    }

    // ==== Active Pie Chart
    function activePiechart() {
        $('.pie-charts').on('inview', function (event, isInView) {
            if (isInView) {
                $('.chart').easyPieChart({
                    scaleLength: 0,
                    lineWidth: 15,
                    trackWidth: 15,
                    size: 160,
                    lineCap: 'square',
                    rotate: 360,
                    trackColor: '#dbd8f3',
                    barColor: '#4c3ec7',
                    lineCap: 'round'
                });
                $(this).unbind('inview');
            }
        });
    }

    /*---------------------
    === Document Ready  ===
    ----------------------*/
    $(document).ready(function () {
        mainMenu();
        activeNiceSelect();
        activePiechart();
        testimonialActive();
        counterUp();
        progressBar();
        activeIsotope();
    });

    // Typed js
    if($("#typed").length > 0) {
        var typed = new Typed('#typed', {
          stringsElement: '.type-string',
          typeSpeed: 80,
          loop: true
        });
    }

    // lazy load init
    var lazyLoadInstance = new LazyLoad();
})(jQuery);

/*---------------------
=== Window Scroll  ===
----------------------*/
$(window).on('scroll', function () {
    const scroll_top = $(window).scrollTop(),
    siteHeader = $('.template-header');

    if (siteHeader.hasClass('sticky-header')) {
        if (scroll_top < 110) {
            siteHeader.removeClass('sticky-on');
        } else {
            siteHeader.addClass('sticky-on');
        }
    }
});

/*------------------
=== Window Load  ===
--------------------*/
$(window).on('load', function () {
    $('#preloader').fadeOut(500);
});