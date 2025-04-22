const images = [
    {
      src: 'images/home_image.png',
      description: "Transforme suas finanças em algo simples e inteligente. Controle gastos, alcance metas e viva com mais tranquilidade!"
    },
    {
      src: "images/graphics_man.png",
      description: "Visualize seu progresso com gráficos intuitivos. Acompanhe cada centavo com sabedoria."
    },
    {
      src: 'images/infos_woman.png',
      description: "Veja informações e estatísticas personalizadas para turbinar sua saúde financeira!"
    }
  ];
  
  let currentSlide = 0;
  const image = document.getElementById("carousel-image");
  const description = document.getElementById("main-description");
  const dots = document.querySelectorAll(".dot");
  
  function showSlide(index) {
    image.style.opacity = 0;
    setTimeout(() => {
      image.src = images[index].src;  // Corrigido de slides para images
      description.textContent = images[index].description;  // Corrigido de slides para images
      image.style.opacity = 1;
  
      dots.forEach(dot => dot.classList.remove("active"));
      dots[index].classList.add("active");
  
      currentSlide = index;
    }, 300);
  }
  
  function nextSlide() {
    let next = (currentSlide + 1) % images.length;
    showSlide(next);
  }
  
  function changeSlide(index) {
    showSlide(index);
  }
  
  // Inicia
  showSlide(currentSlide);
  setInterval(nextSlide, 3500);
  window.changeSlide = changeSlide;
  