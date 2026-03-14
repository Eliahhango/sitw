
function onAllNetworkRequestsCompleted() {

    const images = document.querySelectorAll('img[data-src]');
    const options = {
      rootMargin: '0px',
      threshold: 0.3
    };
  
    const observer = new IntersectionObserver(function(entries, observer) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    }, options);
  
    images.forEach(img => {
      observer.observe(img);
    });
}


document.addEventListener("DOMContentLoaded", function() {
// dom loaded complete run there function
if (document.readyState === 'complete') {
    onAllNetworkRequestsCompleted();
  }else {
    document.addEventListener('readystatechange', function() {
      if (document.readyState === 'complete') {
        onAllNetworkRequestsCompleted();
      }
    });
  }
});