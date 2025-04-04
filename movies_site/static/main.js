function toggleFavorite(element, itemId, title, posterPath, mediaType) {
    fetch('/favorites/toggle_fav', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: itemId,
            title: title,
            poster_path: posterPath,
            media_type: mediaType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            element.classList.add('active');
        } else {
            element.classList.remove('active');
        }
        showToast(data.message, data.success ? 'success' : 'info');
        
        // If we're on the favorites page, remove the card if item was removed
        if (window.location.pathname === '/favorites' && !data.success) {
            const card = element.closest('.movie-card');
            card.style.animation = 'fadeOut 0.3s';
            setTimeout(() => card.remove(), 300);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error updating favorites', 'error');
    });
}

function addToFavorites(itemId, title, posterPath, mediaType) {
    fetch('/add_fav', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: itemId,
            title: title,
            poster_path: posterPath,
            media_type: mediaType
        })
    })
    .then(response => response.json())
    .then(data => {
        Toastify({
            text: data.message,
            duration: 3000,
            gravity: "bottom",
            position: "right",
            backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
    });
}

let currentPage = 1;
let loading = false;
let lastQuery = '';
let currentCategory = 'all';

document.addEventListener('DOMContentLoaded', () => {
    // Add click handlers for category filters
    document.querySelectorAll('[data-category]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            currentCategory = e.target.dataset.category;
            currentPage = 1;
            const container = document.querySelector('.movies-container');
            container.innerHTML = ''; // Clear current content
            loadMoreMovies(true);  // Add true parameter to indicate this is a category change
        });
    });

    // Autocomplete suggestions
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('autocomplete-results');
    let autocompleteTimeout;

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            clearTimeout(autocompleteTimeout);
            const query = this.value.trim();
            if (query.length < 2) {
                resultsContainer.innerHTML = '';
                resultsContainer.style.display = 'none';
                return;
            }
            autocompleteTimeout = setTimeout(() => {
                fetch('/api/autocomplete?q=' + encodeURIComponent(query))  // Updated endpoint
                    .then(response => response.json())
                    .then(data => {
                        let html = '';
                        data.forEach(item => {
                            const title = item.title;
                            const poster = item.poster_path ? 'https://image.tmdb.org/t/p/w92' + item.poster_path : '';
                            const year = item.year ? `(${item.year})` : '';
                            const rating = item.vote_average ? `★ ${item.vote_average.toFixed(1)}` : '';
                            
                            html += `
                                <div class="autocomplete-item" data-id="${item.id}" data-media="${item.media_type}">
                                    ${poster ? `<img src="${poster}" alt="${title}">` : ''}
                                    <div class="autocomplete-info">
                                        <span class="title">${title} ${year}</span>
                                        <div class="meta">
                                            <span class="type">${item.media_type}</span>
                                            ${rating ? `<span class="rating">${rating}</span>` : ''}
                                        </div>
                                    </div>
                                </div>`;
                        });
                        resultsContainer.innerHTML = html;
                        resultsContainer.style.display = data.length ? 'block' : 'none';
                    });
            }, 300);
        });

        // Click handler for suggestions
        resultsContainer.addEventListener('click', function(e) {
            const item = e.target.closest('.autocomplete-item');
            if (item) {
                const id = item.getAttribute('data-id');
                const media = item.getAttribute('data-media');
                window.location.href = `/detail/${media}/${id}`;
            }
        });
    }

    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!resultsContainer.contains(e.target) && e.target !== searchInput) {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
        }
    });

    setupThemeToggle();

    // Remove the infinite scroll event listener if we're on the detail page
    if (!window.location.pathname.startsWith('/detail/')) {
        window.addEventListener('scroll', () => {
            if ((window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight - 800) {
                loadMoreMovies();
            }
        });
    }
});

function createMovieCard(item) {
    const title = item.title || item.name;
    const year = item.release_date ? item.release_date.split('-')[0] : 
                item.first_air_date ? item.first_air_date.split('-')[0] : '';
    const rating = item.vote_average ? item.vote_average.toFixed(1) : '';
    const mediaType = item.media_type || 'movie';
    
    return `
    <div class="movie-card" onclick="window.location.href='/detail/${mediaType}/${item.id}'">
        <div class="movie-poster">
            ${item.poster_path 
                ? `<img src="https://image.tmdb.org/t/p/w500${item.poster_path}" alt="${title}" loading="lazy">`
                : '<div class="no-poster">No Image Available</div>'
            }
            <div class="favorite-icon" onclick="event.stopPropagation(); toggleFavorite(this, '${item.id}', '${title.replace(/'/g, "\\'")}', '${item.poster_path}', '${mediaType}')">
                <svg viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                </svg>
            </div>
        </div>
        <div class="movie-info">
            <span class="media-type">${mediaType}</span>
            <h3>${title}</h3>
            <div class="card-meta">
                ${rating ? `<span class="rating">★ ${rating}</span>` : ''}
                ${year ? `<span class="year">${year}</span>` : ''}
            </div>
        </div>
    </div>
    `;
}

function showLoadingState() {
    const container = document.querySelector('.movies-container');
    const loadingContainer = document.createElement('div');
    loadingContainer.classList.add('loading-container');
    
    for (let i = 0; i < 12; i++) {
        loadingContainer.insertAdjacentHTML('beforeend', `
            <div class="movie-card skeleton">
                <div class="movie-poster skeleton"></div>
                <div class="movie-info">
                    <div class="skeleton" style="height: 24px; width: 80%;"></div>
                    <div class="skeleton" style="height: 20px; width: 60%; margin-top: 8px;"></div>
                </div>
            </div>
        `);
    }
    container.appendChild(loadingContainer);
}

function removeLoadingState() {
    const loadingContainer = document.querySelector('.loading-container');
    if (loadingContainer) {
        loadingContainer.remove();
    }
}

function loadMoreMovies(isCategoryChange = false) {
    if (loading) return;
    
    loading = true;
    if (!isCategoryChange) {
        currentPage++;
    }
    
    showLoadingState();
    
    const searchParams = new URLSearchParams(window.location.search);
    const query = searchParams.get('q');
    let url = query 
        ? `/search?q=${query}&page=${currentPage}`  // Updated path
        : `/home?page=${currentPage}`;  // Updated path

    // Add category parameter if not showing all
    if (currentCategory !== 'all') {
        url += `&category=${currentCategory}`;
    }

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        removeLoadingState();
        const container = document.querySelector('.movies-container');
        if (isCategoryChange) {
            container.innerHTML = ''; // Clear existing content for category changes
        }
        data.items.forEach(movie => {
            container.insertAdjacentHTML('beforeend', createMovieCard(movie));
        });
        loading = false;
    })
    .catch(error => {
        console.error('Error loading more movies:', error);
        removeLoadingState();
        loading = false;
    });
}

// Back to Top Button
const backToTop = document.createElement('div');
backToTop.className = 'back-to-top';
backToTop.innerHTML = '↑';
document.body.appendChild(backToTop);

window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
        backToTop.classList.add('visible');
    } else {
        backToTop.classList.remove('visible');
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

function addToWatchLater(itemId, title, posterPath, mediaType) {
    const watchLaterList = JSON.parse(localStorage.getItem('watchLater') || '[]');
    const item = { itemId, title, posterPath, mediaType };
    
    if (!watchLaterList.some(i => i.itemId === itemId)) {
        watchLaterList.push(item);
        localStorage.setItem('watchLater', JSON.stringify(watchLaterList));
        
        Toastify({
            text: "Added to Watch Later",
            duration: 3000,
            gravity: "bottom",
            position: "right",
            backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
        }).showToast();
    }
}

// Updated Theme Toggle
function setupThemeToggle() {
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');

    // Set initial theme
    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
    }

    function switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    }

    toggleSwitch.addEventListener('change', switchTheme, false);
}

// Modern Toast Notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.innerHTML = `
        <span>${type === 'success' ? '✓' : '✕'}</span>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon
    const themeIcon = document.querySelector('.theme-icon');
    themeIcon.textContent = newTheme === 'dark' ? '🌙' : '☀️';
}

// Initialize theme
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Set initial icon
    const themeIcon = document.querySelector('.theme-icon');
    themeIcon.textContent = savedTheme === 'dark' ? '🌙' : '☀️';
    
    // Remove old theme toggle setup
    const oldToggle = document.querySelector('.theme-switch input[type="checkbox"]');
    if (oldToggle) {
        oldToggle.removeEventListener('change', switchTheme);
    }
});
