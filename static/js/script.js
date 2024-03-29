if (document.getElementsByClassName("myPages").length != 0) {
  function displaySlides() {
    let i;
    let pages = document.getElementsByClassName("myPages");
    for (i = 0; i < pages.length; i++) {
      pages[i].style.display = "none";
    }
    pageIndex++;
    if (pageIndex > pages.length) { pageIndex = 1 }
    pages[pageIndex - 1].style.display = "block";
    setTimeout(displaySlides, 10000);
  }
  displaySlides()
}


// THIS IS FOR THE HOME.HTML 
// IT CONTROLS SWITCHING BETWEEN FARM AND INDUSTRY
if (document.getElementById("farm")) {
  const farm = document.getElementById("farm");
  const industry = document.getElementById("industry");

  const farmItems = document.getElementById("farm-items");
  const industryItems = document.getElementById("industry-items");

  farm.addEventListener('click', () => {
    farmItems.style.display = "block";
    industryItems.style.display = "none";
  })

  industry.addEventListener('click', () => {
    farmItems.style.display = "none";
    industryItems.style.display = "block";
  })
}

// THIS CONTROLS THE CAROUSEL ON ALL UNITS
if (document.getElementsByClassName("mySlides")) {
  let slideIndex = 0;
  animateSlide();
  showSlides(slideIndex);

  function plusSlides(n) {
    showSlides(slideIndex += n);
  }

  function currentSlide(n) {
    showSlides(slideIndex = n);
  }

  function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    // THIS CHECKS IF THE SLIDES CONTAINS ELEMENT
    if (slides[0]?.innerHTML) {
      if (n > slides.length) { slideIndex = 1 }
      if (n < 1) { slideIndex = slides.length }
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[slideIndex - 1].style.display = "block";
      dots[slideIndex - 1].className += " active";
    }
  }


  function animateSlide() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    // THIS CHECKS IF THE SLIDES CONTAINS ELEMENT
    if (slides[0]?.innerHTML) {
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      slideIndex++;
      if (slideIndex > slides.length) { slideIndex = 1 }
      for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
      }
      slides[slideIndex - 1].style.display = "block";
      dots[slideIndex - 1].className += " active";
      setTimeout(animateSlide, 3500); // Change image every 2 seconds
    }
  }
}

// THIS IS FOR THE HAMBURGER MENU TOGGLING
if (document.querySelector("#menu-toggle-icon")) {
  const toggleMenu = document.querySelector("#menu-toggle-icon");
  const openAside = document.querySelector('#aside');
  const bodyColor = document.querySelector('#body');

  function toggleFunction() {
    toggleMenu.classList.toggle("activated");
    openAside.classList.toggle("hidden");
    // bodyColor.classList.toggle("bg-blur");
    // bodyColor.classList.toggle("bg-transparent");
  }

  toggleMenu.addEventListener('click', toggleFunction);
}

// THIS IS FOR READ MESSAGE THAT CHANGES THE READ FROM FALSE TO TRUE
function readMessage(val) {
  const id = val.getAttribute('data-pk');
  $.get(url, { 'pk': id }, () => {
    location.reload()
  })
}

// THIS IS FOR POP UP MESSAGE DISAPPEAR
if (document.getElementById("pop-up")) {
  window.onload = () => {
    popUp = document.getElementById("pop-up");
    setTimeout(() => {
      popUp.style.display = "none"
    }, 1500)
  }
}


// THIS IS THE TOGGLER FOR THE ADD DESCRIPTION TEXTAREA
if (document.getElementById("id_add_description")) {
  const adddescription = document.getElementById("id_add_description");
  const descriptionTextarea = document.getElementById("id_description");

  //  THIS WILL HIDE THE TEXTAREA UNTIL THE BE IS CHECKED
  window.addEventListener('load', () => {
    if (!adddescription.checked) {
      descriptionTextarea.parentNode.parentNode.parentNode.style.display = 'none';
    }
  })

  adddescription.addEventListener('click', () => {
    if (adddescription.checked) {
      descriptionTextarea.parentNode.parentNode.parentNode.style.display = 'table-row';
    } else {
      descriptionTextarea.parentNode.parentNode.parentNode.style.display = 'none';
    }
  })
}

if (document.getElementById("dropdown")) {
  // const dropDown = document.getElementsByClassName("dropdown");
  const dropDowns = document.querySelectorAll(".dropdown");
  dropDowns.forEach((dropDown) => {
    dropDown.addEventListener("click", () => {
      dropDown.nextElementSibling.classList.toggle("scale-dropdown");
      console.log(dropDown.nextElementSibling)
    })
  })
}


if (document.getElementById("select-date")) {
  const selectDate = document.getElementById("select-date");
  const dateDropdown = document.getElementById("date-dropdown");
  selectDate.addEventListener("click", () => {
    dateDropdown.classList.toggle("hidden")
  })
}