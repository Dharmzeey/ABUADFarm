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
    bodyColor.classList.toggle("bg-neutral-700");
    bodyColor.classList.toggle("bg-transparent");
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
if (document.getElementById("pop-up")){
  window.onload = ()=>{
    popUp = document.getElementById("pop-up");
    setTimeout(()=>{
      popUp.style.display = "none"
    }, 2000)
  }
}


// THIS IS THE TOGGLER FOR THE ADD NOTE TEXTAREA
if (document.getElementById("id_add_note")){
  const addNote = document.getElementById("id_add_note");
  const noteTextarea = document.getElementById("id_note");

//  THIS WILL HIDE THE TEXTAREA UNTIL THE BE IS CHECKED
  window.addEventListener('load', ()=> {
    if (!addNote.checked) {
      noteTextarea.parentNode.parentNode.style.display = 'none';
    }
  })

  addNote.addEventListener('click', ()=> {
    if(addNote.checked){
      noteTextarea.parentNode.parentNode.style.display = 'table-row';
    }else {
      noteTextarea.parentNode.parentNode.style.display = 'none';
    }
  })
}

