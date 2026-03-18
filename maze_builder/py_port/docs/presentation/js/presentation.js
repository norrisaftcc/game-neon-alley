document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    
    // Initialize buttons
    const prevBtn = document.getElementById('prev-slide');
    const nextBtn = document.getElementById('next-slide');
    
    // Create slide indicators
    const slideIndicators = document.querySelector('.slide-indicators');
    for (let i = 0; i < totalSlides; i++) {
        const indicator = document.createElement('div');
        indicator.classList.add('indicator');
        if (i === 0) indicator.classList.add('active');
        indicator.setAttribute('data-slide', i);
        indicator.addEventListener('click', () => goToSlide(i));
        slideIndicators.appendChild(indicator);
    }
    
    // Update button states
    function updateButtons() {
        prevBtn.disabled = currentSlide === 0;
        nextBtn.disabled = currentSlide === totalSlides - 1;
    }
    
    // Show a specific slide
    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        slides[index].classList.add('active');
        
        // Update indicators
        document.querySelectorAll('.indicator').forEach((ind, i) => {
            if (i === index) {
                ind.classList.add('active');
            } else {
                ind.classList.remove('active');
            }
        });
        
        // Update buttons
        updateButtons();
    }
    
    // Go to a specific slide
    function goToSlide(index) {
        currentSlide = index;
        showSlide(currentSlide);
    }
    
    // Next slide
    function nextSlide() {
        if (currentSlide < totalSlides - 1) {
            currentSlide++;
            showSlide(currentSlide);
        }
    }
    
    // Previous slide
    function prevSlide() {
        if (currentSlide > 0) {
            currentSlide--;
            showSlide(currentSlide);
        }
    }
    
    // Theme switching
    const themeBtns = document.querySelectorAll('.theme-btn');
    themeBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const theme = this.getAttribute('data-theme');
            
            // Remove all theme classes
            document.body.classList.remove('theme-retro', 'theme-light');
            
            // Add the selected theme class if not default
            if (theme !== 'default') {
                document.body.classList.add(`theme-${theme}`);
            }
            
            // Update active button
            themeBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight' || e.key === ' ') {
            nextSlide();
        } else if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key >= '1' && e.key <= totalSlides.toString()) {
            // Go to slide number (1-based)
            goToSlide(parseInt(e.key) - 1);
        }
    });
    
    // Event listeners for buttons
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // Initialize
    showSlide(currentSlide);
    
    // Add animation class to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
    });
});