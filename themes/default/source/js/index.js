import "@splidejs/splide/css";
import Splide from "@splidejs/splide";

import AOS from "aos";
import "aos/dist/aos.css";

document.addEventListener("DOMContentLoaded", function() {
  const testimonialContainer = document.getElementById("customerReviewsSlider");
  if (testimonialContainer !== null) {
    const testimonialSliders = new Splide("#customerReviewsSlider", {
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

  // Project sliders
  const projectsSlider = new Splide("#projectsSlider", {
    type: "loop",
    perPage: 2,
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

  projectsSlider.mount();

  AOS.init();
});
