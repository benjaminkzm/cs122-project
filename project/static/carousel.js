// static/carousel.js
// Wait until DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('carousel');
    if (!container) return;
  
    // Parse the screenshots array from the data attribute
    let screenshots;
    try {
      screenshots = JSON.parse(container.dataset.screenshots);
    } catch (e) {
      console.error('Invalid screenshots data', e);
      return;
    }
  
    // Grab elements
    const imgEl = document.getElementById('carouselImage');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    let index = 0;
  
    // Update the image source based on current index
    function updateImage() {
      imgEl.src = screenshots[index];
    }
  
    // Previous button handler
    prevBtn.addEventListener('click', () => {
      index = (index - 1 + screenshots.length) % screenshots.length;
      updateImage();
    });
  
    // Next button handler
    nextBtn.addEventListener('click', () => {
      index = (index + 1) % screenshots.length;
      updateImage();
    });
  
    // Initialize
    updateImage();
  });
  