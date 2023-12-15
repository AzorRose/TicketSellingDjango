window.addEventListener("scroll", function() {
    var middleLine = document.querySelector(".middle-line");
    var scrollPosition = window.scrollY;

    if (scrollPosition > 0) {
      middleLine.style.position = "fixed";
      middleLine.style.top = "0";
    } else {
      middleLine.style.position = "static";
    }
});