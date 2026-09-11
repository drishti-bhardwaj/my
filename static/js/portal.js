/* ==========================================================================
   NATIONAL CPSE PORTAL - INTERACTIVE JAVASCRIPT CONTROLLER
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  initLanguageToggle();
  initAccessibility();
  initCPSEModals();
  initCPSEFilter();
  initMediaLightbox();
  initCountUpObserver();
  initSearchModal();
});

/* --------------------------------------------------------------------------
   1. HERO BANNER SLIDER WITH AUTOPLAY & KEN BURNS EFFECT
   -------------------------------------------------------------------------- */
let currentSlideIndex = 0;
let slideInterval = null;
let isPlaying = true;

function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dotsContainer = document.getElementById('heroDots');
  const prevBtn = document.getElementById('heroPrev');
  const nextBtn = document.getElementById('heroNext');
  const playPauseBtn = document.getElementById('heroPlayPause');

  if (!slides.length) return;

  // Create dot indicators
  if (dotsContainer) {
    dotsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('div');
      dot.className = `hero-dot ${idx === 0 ? 'active' : ''}`;
      dot.addEventListener('click', () => goToSlide(idx));
      dotsContainer.appendChild(dot);
    });
  }

  function showSlide(index) {
    slides.forEach((slide, idx) => {
      if (idx === index) {
        slide.classList.add('active');
      } else {
        slide.classList.remove('active');
      }
    });

    const dots = document.querySelectorAll('.hero-dot');
    dots.forEach((dot, idx) => {
      if (idx === index) dot.classList.add('active');
      else dot.classList.remove('active');
    });

    currentSlideIndex = index;
  }

  function nextSlide() {
    const newIndex = (currentSlideIndex + 1) % slides.length;
    showSlide(newIndex);
  }

  function prevSlide() {
    const newIndex = (currentSlideIndex - 1 + slides.length) % slides.length;
    showSlide(newIndex);
  }

  function goToSlide(index) {
    showSlide(index);
    resetTimer();
  }

  function startTimer() {
    if (slideInterval) clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 6000);
    isPlaying = true;
    if (playPauseBtn) playPauseBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
  }

  function pauseTimer() {
    if (slideInterval) clearInterval(slideInterval);
    isPlaying = false;
    if (playPauseBtn) playPauseBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
  }

  function resetTimer() {
    if (isPlaying) {
      pauseTimer();
      startTimer();
    }
  }

  if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); resetTimer(); });
  if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); resetTimer(); });
  if (playPauseBtn) {
    playPauseBtn.addEventListener('click', () => {
      if (isPlaying) pauseTimer();
      else startTimer();
    });
  }

  startTimer();
}

/* --------------------------------------------------------------------------
   2. LANGUAGE SWITCHER (ENGLISH <-> HINDI)
   -------------------------------------------------------------------------- */
const translations = {
  en: {
    navHome: "Home",
    navAbout: "About",
    navCpses: "Featured CPSEs",
    navSectors: "Sectors",
    navProjects: "Projects",
    navNews: "News & Updates",
    navGallery: "Media Gallery",
    navContact: "Contact",
    portalSubtitle: "Department of Public Enterprises | Ministry of Finance",
    heroCta1: "Explore CPSEs",
    heroCta2: "Discover Sectors",
    sectionCpseTitle: "India's Leading CPSEs",
    sectionCpseSubtitle: "Explore Maharatna, Navratna and Miniratna enterprises driving national industrial growth.",
    exploreBtn: "Explore CPSE",
    officialWebBtn: "Visit Official Website"
  },
  hi: {
    navHome: "मुख्य पृष्ठ",
    navAbout: "परिचय",
    navCpses: "प्रमुख सीपीएसई",
    navSectors: "औद्योगिक क्षेत्र",
    navProjects: "प्रमुख परियोजनाएं",
    navNews: "समाचार एवं अपडेट",
    navGallery: "मीडिया गैलरी",
    navContact: "संपर्क करें",
    portalSubtitle: "लोक उद्यम विभाग | वित्त मंत्रालय, भारत सरकार",
    heroCta1: "सीपीएसई देखें",
    heroCta2: "क्षेत्र खोजें",
    sectionCpseTitle: "भारत के प्रमुख केंद्रीय सार्वजनिक क्षेत्र उद्यम (CPSEs)",
    sectionCpseSubtitle: "राष्ट्र के औद्योगिक विकास को गति देने वाले महारत्न एवं नवरत्न उद्यमों का अन्वेषण करें।",
    exploreBtn: "विवरण देखें",
    officialWebBtn: "आधिकारिक वेबसाइट पर जाएं"
  }
};

let currentLang = 'en';

function initLanguageToggle() {
  const langEnBtn = document.getElementById('langEn');
  const langHiBtn = document.getElementById('langHi');

  if (!langEnBtn || !langHiBtn) return;

  langEnBtn.addEventListener('click', () => setLanguage('en'));
  langHiBtn.addEventListener('click', () => setLanguage('hi'));
}

function setLanguage(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;

  document.getElementById('langEn').classList.toggle('active', lang === 'en');
  document.getElementById('langHi').classList.toggle('active', lang === 'hi');

  const dict = translations[lang];

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });
}

/* --------------------------------------------------------------------------
   3. ACCESSIBILITY CONTROLS (FONT SIZE & HIGH CONTRAST)
   -------------------------------------------------------------------------- */
function initAccessibility() {
  const fontSmBtn = document.getElementById('fontSm');
  const fontMdBtn = document.getElementById('fontMd');
  const fontLgBtn = document.getElementById('fontLg');
  const contrastToggle = document.getElementById('contrastToggle');

  if (fontSmBtn) fontSmBtn.addEventListener('click', () => setFontSize('font-sm'));
  if (fontMdBtn) fontMdBtn.addEventListener('click', () => setFontSize('font-md'));
  if (fontLgBtn) fontLgBtn.addEventListener('click', () => setFontSize('font-lg'));

  if (contrastToggle) {
    contrastToggle.addEventListener('click', () => {
      document.body.classList.toggle('high-contrast');
    });
  }
}

function setFontSize(sizeClass) {
  document.documentElement.classList.remove('font-sm', 'font-md', 'font-lg');
  document.documentElement.classList.add(sizeClass);
}

/* --------------------------------------------------------------------------
   4. CPSE DETAIL MODAL SYSTEM
   -------------------------------------------------------------------------- */
function initCPSEModals() {
  const modalOverlay = document.getElementById('cpseModalOverlay');
  const closeBtn = document.getElementById('cpseModalClose');

  if (!modalOverlay) return;

  document.querySelectorAll('.cpse-explore-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const cpseId = btn.getAttribute('data-cpse-id');
      openCPSEModal(cpseId);
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });
  }

  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) {
      modalOverlay.classList.remove('active');
    }
  });
}

function openCPSEModal(cpseId) {
  const cpse = window.CPSE_DATA_GLOBAL ? window.CPSE_DATA_GLOBAL.find(c => c.id === cpseId) : null;
  if (!cpse) return;

  const modalOverlay = document.getElementById('cpseModalOverlay');

  document.getElementById('modalCpseName').textContent = cpse.fullName + ` (${cpse.name})`;
  document.getElementById('modalCpseTag').textContent = cpse.category;
  document.getElementById('modalCpseSector').textContent = cpse.sector;
  document.getElementById('modalCpseOverview').textContent = cpse.overview;
  document.getElementById('modalCpseImg').src = cpse.image;
  document.getElementById('modalCpseWeb').href = cpse.officialWebsite;

  // Key Areas
  const areasList = document.getElementById('modalCpseKeyAreas');
  if (areasList) {
    areasList.innerHTML = cpse.keyAreas.map(area => `<li><i class="fa-solid fa-check-circle text-success me-2"></i> ${area}</li>`).join('');
  }

  // Contributions
  const contribList = document.getElementById('modalCpseContributions');
  if (contribList) {
    contribList.innerHTML = cpse.contributions.map(c => `<li class="mb-2"><i class="fa-solid fa-arrow-right text-warning me-2"></i> ${c}</li>`).join('');
  }

  // Stats Grid
  const statsContainer = document.getElementById('modalCpseStats');
  if (statsContainer) {
    statsContainer.innerHTML = Object.entries(cpse.stats).map(([k, v]) => `
      <div class="p-3 bg-light rounded text-center border">
        <div class="h5 font-weight-bold text-primary mb-1">${v}</div>
        <div class="small text-muted text-capitalize">${k.replace(/([A-Z])/g, ' $1')}</div>
      </div>
    `).join('');
  }

  modalOverlay.classList.add('active');
}

/* --------------------------------------------------------------------------
   5. FILTER & SEARCH CPSE CARDS
   -------------------------------------------------------------------------- */
function initCPSEFilter() {
  const filterBtns = document.querySelectorAll('.cpse-filter-btn');
  const searchInput = document.getElementById('cpseSearchInput');
  const cards = document.querySelectorAll('.cpse-card-col');

  let activeSector = 'all';

  function filterCards() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    cards.forEach(card => {
      const sector = card.getAttribute('data-sector') || '';
      const text = card.textContent.toLowerCase();

      const matchesSector = (activeSector === 'all' || sector === activeSector);
      const matchesSearch = (!query || text.includes(query));

      if (matchesSector && matchesSearch) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active', 'btn-primary'));
      filterBtns.forEach(b => b.classList.add('btn-outline'));
      
      btn.classList.add('active', 'btn-primary');
      btn.classList.remove('btn-outline');

      activeSector = btn.getAttribute('data-filter');
      filterCards();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', filterCards);
  }
}

/* --------------------------------------------------------------------------
   6. MEDIA GALLERY LIGHTBOX
   -------------------------------------------------------------------------- */
let currentMediaIndex = 0;
let mediaList = [];

function initMediaLightbox() {
  const mediaCards = document.querySelectorAll('.media-gallery-card');
  const lightbox = document.getElementById('mediaLightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxTitle = document.getElementById('lightboxTitle');
  const closeBtn = document.getElementById('lightboxClose');
  const prevBtn = document.getElementById('lightboxPrev');
  const nextBtn = document.getElementById('lightboxNext');

  if (!lightbox) return;

  mediaCards.forEach((card, idx) => {
    const imgUrl = card.getAttribute('data-img');
    const title = card.getAttribute('data-title');
    mediaList.push({ imgUrl, title });

    card.addEventListener('click', () => {
      showMedia(idx);
      lightbox.classList.add('active');
    });
  });

  function showMedia(index) {
    if (!mediaList[index]) return;
    currentMediaIndex = index;
    lightboxImg.src = mediaList[index].imgUrl;
    lightboxTitle.textContent = mediaList[index].title;
  }

  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      const newIdx = (currentMediaIndex - 1 + mediaList.length) % mediaList.length;
      showMedia(newIdx);
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      const newIdx = (currentMediaIndex + 1) % mediaList.length;
      showMedia(newIdx);
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      lightbox.classList.remove('active');
    });
  }

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) lightbox.classList.remove('active');
  });

  document.addEventListener('keydown', (e) => {
    if (!lightbox.classList.contains('active')) return;
    if (e.key === 'Escape') lightbox.classList.remove('active');
    if (e.key === 'ArrowLeft') prevBtn && prevBtn.click();
    if (e.key === 'ArrowRight') nextBtn && nextBtn.click();
  });
}

/* --------------------------------------------------------------------------
   7. COUNT-UP ANIMATION ON SCROLL
   -------------------------------------------------------------------------- */
function initCountUpObserver() {
  const statNumbers = document.querySelectorAll('.stat-number');
  if (!statNumbers.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(num => observer.observe(num));
}

function animateCounter(el) {
  const targetText = el.getAttribute('data-target') || el.textContent;
  const targetNum = parseInt(targetText.replace(/\D/g, '')) || 100;
  const suffix = targetText.replace(/[0-9]/g, '');

  let current = 0;
  const step = Math.ceil(targetNum / 40);
  const timer = setInterval(() => {
    current += step;
    if (current >= targetNum) {
      el.textContent = targetNum + suffix;
      clearInterval(timer);
    } else {
      el.textContent = current + suffix;
    }
  }, 40);
}

/* --------------------------------------------------------------------------
   8. FULLSCREEN SEARCH MODAL (CTRL+K)
   -------------------------------------------------------------------------- */
function initSearchModal() {
  const searchTrigger = document.getElementById('searchModalTrigger');
  const searchModal = document.getElementById('searchModal');
  const searchClose = document.getElementById('searchModalClose');
  const globalInput = document.getElementById('globalSearchInput');
  const searchResults = document.getElementById('searchResultsContainer');

  if (!searchModal) return;

  if (searchTrigger) {
    searchTrigger.addEventListener('click', () => {
      searchModal.classList.add('active');
      if (globalInput) globalInput.focus();
    });
  }

  if (searchClose) {
    searchClose.addEventListener('click', () => {
      searchModal.classList.remove('active');
    });
  }

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchModal.classList.add('active');
      if (globalInput) globalInput.focus();
    }
  });

  if (globalInput && searchResults) {
    globalInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        searchResults.innerHTML = '<p class="text-muted text-center py-4">Type to search CPSEs, Sectors, Projects, or News...</p>';
        return;
      }

      const matches = window.CPSE_DATA_GLOBAL ? window.CPSE_DATA_GLOBAL.filter(c => 
        c.name.toLowerCase().includes(q) || 
        c.fullName.toLowerCase().includes(q) || 
        c.sector.toLowerCase().includes(q) ||
        c.overview.toLowerCase().includes(q)
      ) : [];

      if (!matches.length) {
        searchResults.innerHTML = `<p class="text-muted text-center py-4">No results found for "${q}"</p>`;
        return;
      }

      searchResults.innerHTML = matches.map(m => `
        <div class="p-3 bg-white border rounded mb-2 d-flex justify-content-between align-items-center">
          <div>
            <h6 class="mb-0 font-weight-bold text-primary">${m.name} - ${m.fullName}</h6>
            <small class="text-muted">${m.sector} | ${m.category}</small>
          </div>
          <button class="btn btn-sm btn-outline-primary cpse-explore-btn" data-cpse-id="${m.id}" onclick="document.getElementById('searchModal').classList.remove('active'); openCPSEModal('${m.id}')">View</button>
        </div>
      `).join('');
    });
  }
}
