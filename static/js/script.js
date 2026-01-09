// ============================
// HERO IMAGE SLIDER SCRIPT
// ============================

document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");
  let index = 0;

  function showSlide(i) {
    slides.forEach(slide => slide.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active"));

    slides[i].classList.add("active");
    dots[i].classList.add("active");
    index = i;
  }

  function setLanguage(lang) {
    const interval = setInterval(() => {
      const select = document.querySelector(".goog-te-combo");
      if (select) {
        select.value = lang;
        select.dispatchEvent(new Event("change"));
        clearInterval(interval);
      }
    }, 500);
  }


  // Auto slide
  setInterval(() => {
    let nextIndex = (index + 1) % slides.length;
    showSlide(nextIndex);
  }, 3500);

  // Dot click
  dots.forEach(dot => {
    dot.addEventListener("click", () => {
      const slideIndex = dot.getAttribute("data-slide");
      showSlide(slideIndex);
    });
  });
});
