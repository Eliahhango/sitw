"use strict";
$(function () {

    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });


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

