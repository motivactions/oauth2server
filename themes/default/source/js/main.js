import bootstrap from "bootstrap/dist/js/bootstrap.bundle.js";
import OverlayScrollbars from "overlayscrollbars";

import "@splidejs/splide/css";
import Splide from "@splidejs/splide";

import "./images";
import "../scss/main.scss";

document.addEventListener("DOMContentLoaded", function () {
  // BOOTSTRAP TOOLTIP
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // BOOTSTRAP POPOVER
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  
  popoverTriggerList.map(function (popoverTriggerEl) {
    let opts = {
      animation: true,
    };
    if (popoverTriggerEl.hasAttribute("data-bs-content-id")) {
      var content_id = popoverTriggerEl.getAttribute("data-bs-content-id");
      var content_el = document.getElementById(content_id);
      if (content_el != null) {
        opts.content = content_el.innerHTML;
      } else {
        opts.content = `content element with #${content_id} not found!`;
      }
      opts.html = true;
    }
    return new bootstrap.Popover(popoverTriggerEl, opts);
  });

  // Scrollbar overlay
  var OverlayScrollbarsList = [].slice.call(
    document.querySelectorAll(".scrollbars")
  );
  
  //Testimonial Slider
  var testimonialSliders = document.getElementById("customerReviewsSlider");
  if (testimonialSliders != null) {
    var testimonialSliders = new Splide("#customerReviewsSlider", {
      type: "loop",
      perPage: 3,
      perMove: 1,
      gap: "0.25rem",
      interval: 2000,
      autoplay: true,
      pauseOnFocus: true,
      pauseOnHover: false,
      arrows: false,
      pagination: false,
      breakpoints: {
        640: {
          perPage: 1,
        },
        960: {
          perPage: 2,
        },
      },
    });
    testimonialSliders.mount();
  }
  
  OverlayScrollbarsList.map(function (scrollbarsEl) {
    return new OverlayScrollbars(scrollbarsEl, {});
  });
});

window.bootstrap = bootstrap;
window.OverlayScrollbars = OverlayScrollbars;
