(function ($) {
  "use strict";

  /*--------------------------------------------------------
  // Sticky header
  /--------------------------------------------------------*/

  $(window).on("scroll", function () {
    var navbar = $(".navbar");
    if ($(window).scrollTop() >= 200) {
      navbar.addClass("sticky-navbar");
    } else {
      navbar.removeClass("sticky-navbar");
    }
  });


  /*-------- MainMenu To mobileMenu --------*/
  const mainMenu = document.querySelector('#mainMenu');
  const mobileMenu = document.querySelector('#mobileMenu');

  // Clone এবং append
  if (mainMenu && mobileMenu) {
    const cloneMenu = mainMenu.cloneNode(true);
    mobileMenu.appendChild(cloneMenu);
  }


  /*------------------------------------
  /  01. Mobile menu toggle Dropdown
  /------------------------------------*/
  $(document).ready(function () {
    $("#mobileMenu .dropdown-toggle, #mobileMenu .submenu-toggle").click(function (e) {
      e.preventDefault();
      $(this).next(".dropdown-menu").slideToggle("slow");
    });
  });

  /*============================================
    Navlink active class in location
  ============================================*/
  $(document).ready(function () {
    var currentPage = window.location.pathname.split("/").pop(); // Get current page name

    $('#mainMenu a, #mobileMenu a').each(function () {
      var linkPage = $(this).attr('href');

      if (linkPage === currentPage) {
        $(this).addClass('active');

        // Optional: Add 'active' to parent <li> if needed
        $(this).closest('.nav-item').addClass('active');
      }
    });
  });


  // menu - toggler
  var menuToggler = $(".menu-toggler");
  var offcanvas = $("#mobilemenu-offcanvas");

  offcanvas.on("show.bs.offcanvas", function () {
    menuToggler.addClass("active");
  });

  offcanvas.on("hidden.bs.offcanvas", function () {
    menuToggler.removeClass("active");
  });

  // menu-action use mobile menu
  $(".menu-action-item a").on('click', function () {
    var target = $(this).parent().children(".setting-dropdown");
    $(target).slideToggle();
    $(this).find(".plus-icon i").toggleClass("fa-plus fa-minus");
  });


})(jQuery);
// Hover Menu
document.addEventListener("DOMContentLoaded", function () {
  if (window.innerWidth > 1199) {
    document.querySelectorAll('.hover-menu .dropdown').forEach(function (everyitem) {
      everyitem.addEventListener('mouseover', function (e) {
        let el_link = this.querySelector('a[data-bs-toggle]');
        if (el_link !== null) {
          let nextEl = el_link.nextElementSibling;
          el_link.classList.add('show');
          if (nextEl !== null && this.contains(nextEl)) {
            nextEl.classList.add('show');
          }
        }
      }.bind(everyitem));
      everyitem.addEventListener('mouseleave', function (e) {
        let el_link = this.querySelector('a[data-bs-toggle]');
        if (el_link !== null) {
          let nextEl = el_link.nextElementSibling;
          if (nextEl !== null && this.contains(nextEl)) {
            el_link.classList.remove('show');
            nextEl.classList.remove('show');
          }
        }
      }.bind(everyitem));
    });
  }
  // end if innerWidth
});
