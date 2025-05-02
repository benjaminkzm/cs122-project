// static/trailer_carousel.js
document.addEventListener('DOMContentLoaded', () => {
    const vc = document.getElementById('videoCarousel');
    if (!vc) return;
    let items;
    try {
      items = JSON.parse(vc.dataset.items);
    } catch {
      return;
    }
  
    let idx = 0;
    const vidEl   = document.getElementById('carouselVideo');
    const prevBtn = document.getElementById('prevVideo');
    const nextBtn = document.getElementById('nextVideo');
  
    function preloadVideo(src) {
      const link = document.createElement('link');
      link.rel = 'preload';
      link.as  = 'video';
      link.href = src;
      document.head.appendChild(link);
    }
  
    function updateVideo() {
      vidEl.querySelector('source').src = items[idx];
      vidEl.load();
  
      // preload the *following* video
      const nextIndex = (idx + 1) % items.length;
      preloadVideo(items[nextIndex]);
    }
  
    prevBtn.addEventListener('click', () => {
      idx = (idx - 1 + items.length) % items.length;
      updateVideo();
    });
  
    nextBtn.addEventListener('click', () => {
      idx = (idx + 1) % items.length;
      updateVideo();
    });
  
    // initial preload of the very next clip
    preloadVideo(items[1]);
  });
  