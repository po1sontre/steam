class SteamLibrary {
    constructor() {
        this.accounts = [];
        this.genres = new Set();
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadAccounts();
        this.populateGenreFilter();
        this.updateStats();
        this.renderAccounts();
        this.setupSearchDebounce();
    }

    setupEventListeners() {
        document.querySelectorAll('nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation(e.target.getAttribute('href'));
            });
        });

        document.getElementById('genreFilter').addEventListener('change', () => {
            this.filterAccounts();
            this.animateResults();
        });
    }

    setupSearchDebounce() {
        const searchInput = document.getElementById('searchInput');
        let debounceTimeout;

        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimeout);
            debounceTimeout = setTimeout(() => {
                this.filterAccounts();
                this.animateResults();
            }, 300);
        });
    }

    async loadAccounts() {
        try {
            this.accounts = accountsData;
            this.accounts.forEach(account => {
                account.games = account.games.map(game => game.toLowerCase());
            });
        } catch (error) {
            console.error('Error loading accounts:', error);
            this.accounts = [];
        }
    }

    updateStats() {
        const totalAccountsElement = document.getElementById('totalAccounts');
        const totalGamesElement = document.getElementById('totalGames');

        const totalAccounts = this.accounts.length;
        const totalGames = this.accounts.reduce((sum, account) => sum + account.games.length, 0);

        totalAccountsElement.textContent = totalAccounts;
        totalGamesElement.textContent = totalGames;
        document.getElementById('totalGenres').style.display = 'none';
    }

    populateGenreFilter() {
        const filterBox = document.querySelector('.filter-box');
        if (filterBox) {
            filterBox.style.display = 'none';
        }
    }

    renderAccounts(accountsToRender = this.accounts) {
        const container = document.getElementById('accountsContainer');
        container.innerHTML = '';

        if (accountsToRender.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <h3>No accounts found</h3>
                    <p>Try adjusting your search criteria</p>
                </div>
            `;
            return;
        }

        accountsToRender.forEach((account, index) => {
            const MAX_VISIBLE_GAMES = 3;
            const hasMoreGames = account.games.length > MAX_VISIBLE_GAMES;
            
            const card = document.createElement('div');
            card.className = 'account-card';
            
            const gamesList = account.games
                .slice(0, MAX_VISIBLE_GAMES)
                .map(game => `
                    <li class="game-item">
                        <span class="game-name">${this.capitalizeGame(game)}</span>
                    </li>
                `).join('');

            const hiddenGamesList = account.games
                .slice(MAX_VISIBLE_GAMES)
                .map(game => `
                    <li class="game-item hidden expandable-game">
                        <span class="game-name">${this.capitalizeGame(game)}</span>
                    </li>
                `).join('');

            card.innerHTML = `
                <div class="account-info">
                    <div class="account-credentials">
                        <div class="credential-item">
                            <span class="label">Username:</span>
                            <span class="value">${account.username}</span>
                        </div>
                        <div class="credential-item">
                            <span class="label">Password:</span>
                            <span class="value">${account.password}</span>
                        </div>
                        ${account.country ? `
                        <div class="credential-item">
                            <span class="label">Country:</span>
                            <span class="value">${account.country}</span>
                        </div>
                        ` : ''}
                    </div>
                    <div class="games-badge">
                        ${account.games.length} Game${account.games.length !== 1 ? 's' : ''}
                    </div>
                </div>
                <ul class="games-list">
                    ${gamesList}
                    ${hiddenGamesList}
                </ul>
                ${hasMoreGames ? `
                    <button class="expand-button">
                        Show More (${account.games.length - MAX_VISIBLE_GAMES} more games)
                    </button>
                ` : ''}
            `;
            
            if (hasMoreGames) {
                const expandButton = card.querySelector('.expand-button');
                expandButton.addEventListener('click', () => {
                    const expandableGames = card.querySelectorAll('.expandable-game');
                    expandableGames.forEach(game => game.classList.toggle('hidden'));
                    expandButton.textContent = expandButton.textContent.includes('Show More') 
                        ? 'Show Less'
                        : `Show More (${account.games.length - MAX_VISIBLE_GAMES} more games)`;
                });
            }
            
            container.appendChild(card);
        });
    }

    capitalizeGame(game) {
        return game.split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    filterAccounts() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();

        const filtered = this.accounts.filter(account => {
            const matchesSearch = searchTerm === '' || 
                account.games.some(game => game.includes(searchTerm)) ||
                account.username.toLowerCase().includes(searchTerm) ||
                account.country?.toLowerCase().includes(searchTerm);

            return matchesSearch;
        });

        this.renderAccounts(filtered);
    }

    animateResults() {
        const cards = document.querySelectorAll('.account-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    }

    handleNavigation(href) {
        document.querySelectorAll('nav a').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === href) {
                link.classList.add('active');
            }
        });

        document.querySelector('.accounts-grid').classList.toggle('hidden', href === '#about');
        document.querySelector('.search-section').classList.toggle('hidden', href === '#about');
        document.querySelector('.about-section').classList.toggle('hidden', href !== '#about');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SteamLibrary();
});