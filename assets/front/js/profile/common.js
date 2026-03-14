"use strict";

function initSiteMotion() {
    const body = document.body;

    if (!body) {
        return;
    }

    body.classList.add('motion-enhanced');

    const selector = [
        'section .container > .row > [class*="col-"]',
        '.blog-post-item',
        '.widget',
        '.post-item',
        '.portfolio-item',
        '.single-service',
        '.single-feature',
        '.single-pricing',
        '.single-testimonial',
        '.single-team',
        '.single-counter',
        '.single-box',
        '.single-page-wrapper',
        '.contact-form-wrapper',
        '.card',
        '.template-footer .col-lg-4',
        '.footer-area .col-lg-4',
        '.saas-footer .col-lg-4'
    ].join(',');

    const nodes = Array.from(document.querySelectorAll(selector)).filter(function(node) {
        return !node.closest('.slick-cloned');
    });
    const uniqueNodes = Array.from(new Set(nodes));

    uniqueNodes.forEach(function(node, index) {
        node.classList.add('reveal-on-scroll');
        node.style.setProperty('--reveal-delay', Math.min((index % 4) * 80, 240) + 'ms');
    });

    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion || !('IntersectionObserver' in window)) {
        uniqueNodes.forEach(function(node) {
            node.classList.add('site-reveal-visible');
        });
        return;
    }

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('site-reveal-visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.14,
        rootMargin: '0px 0px -12% 0px'
    });

    uniqueNodes.forEach(function(node) {
        observer.observe(node);
    });
}

$(function () {

    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });

    initSiteMotion();


    // Menu js
    $('.post-gallery-slider').slick({
        dots: false,
        arrows: true,
        infinite: true,
        autoplay: true,
        speed: 800,
        prevArrow: '<div class="prev"><i class="fas fa-angle-left"></i></div>',
        nextArrow: '<div class="next"><i class="fas fa-angle-right"></i></div>',
        slidesToShow: 1,
        slidesToScroll: 1,
        rtl: rtl == 1 ? true : false
    });

    //===== Magnific Popup

    $('.image-popup').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        }
    });

    // datepicker & timepicker
    /* ***************************************************
    ==========bootstrap datepicker and timepicker start==========
    ******************************************************/
    $('.datepicker').datepicker({
        autoclose: true
    });

    $('.timepicker').timepicker({
        autoclose: true
    });
    /* ***************************************************
  ==========bootstrap datepicker and timepicker  end==========
  ******************************************************/

    $(function () {
        let today = new Date();
        $('.calendar-container').pignoseCalendar('init', {
            disabledDates: jQuery.parseJSON($holidays),
            minDate: today.setDate(today.getDate() - 1),
            // date: '2023-02-23',
            disabledWeekdays: jQuery.parseJSON($weekends),
            // disabledWeekdays: [2, 4], // SUN (0), SAT (6)
            select: onClickHandler
        });
    });


    function onClickHandler(date, obj) {
        if (date[0] !== null) {
            var $date = date[0]._i;
            console.log($date);
            $("input[name='date']").val($date);
            $('.request-loader').show();
            $('.timeslot-box').hide();
            $.ajax({
                url: timeSlotUrl,
                type: 'get',
                data: {
                    date: $date
                },
                success: function (data) {
                    if (data.length !== 0) {
                        $('.timeslot-box').show();
                        let slots = '';
                        for (let i = 0; i < data.length; i++) {
                            slots += `<span dir="ltr" class="single-timeslot mr-2 mb-2  p-2 rounded" data-id="${data[i].id}" data-slot="${data[i].start} - ${data[i].end}"  >${data[i].start} - ${data[i].end}</span>`;
                        }
                        $(".timeslot-box").html(slots);
                    }
                    $('.request-loader').hide();
                }, error: function (data) {
                    console.log(data)
                }
            });
        }
    }

    $(document).on('click', '.single-timeslot', function (e) {
        let slotId = $(this).attr('data-id')
        let date = $("input[name='date']").val();
        $.ajax({
            url: checkThisSlot,
            type: 'get',
            data: {
                slotId: slotId,
                date: date,
            },
            success: function (data) {
                if (data == 'booked') {
                    toastr['error']("This time slot is booked! Please try another slot.")
                }
            }, error: function (err) {
                console.log(err)
            }
        });
        $('.single-timeslot').removeClass('active');
        $(this).addClass('active');
        $("input[name='slot']").val($(this).attr('data-slot'));
        $("input[name='slotId']").val($(this).attr('data-id'));
    })

});

