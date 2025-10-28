document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded');
    
    // ============================================
    // 1. SIDEBAR TOGGLE (en premier)
    // ============================================
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            sidebar.classList.toggle('open');
        });
    }
    
    // ============================================
    // 2. CHOICES.JS - BOOKMAKER
    // ============================================
    let bookmakerChoices = null;
    const bookmakerSelect = document.querySelector('select[name="odds_filter[bookmaker][]"]');
    
    console.log('Bookmaker select found:', bookmakerSelect);
    console.log('Choices available:', typeof Choices !== 'undefined');
    
    function initializeChoices() {
        if (typeof Choices === 'undefined') {
            console.log('⏳ Choices.js not ready, waiting...');
            setTimeout(initializeChoices, 100);
            return;
        }
        
        console.log('✅ Choices.js ready');
        
        // Bookmaker
        const bookmakerSelect = document.querySelector('select[name="odds_filter[bookmaker][]"]');
        if (bookmakerSelect) {
            const bookmakerChoices = new Choices(bookmakerSelect, {
                removeItemButton: true,
                searchEnabled: true,
                searchPlaceholderValue: 'Search bookmakers...',
                placeholder: true,
                placeholderValue: 'Select bookmakers',
                noResultsText: 'No bookmakers found',
                itemSelectText: ''
            });
            console.log('✅ Choices initialized on bookmaker');
        }
        
        // League
        const leagueSelect = document.querySelector('select[name="odds_filter[league][]"]');
        if (leagueSelect) {
            window.leagueChoices = new Choices(leagueSelect, {
                removeItemButton: true,
                searchEnabled: true,
                searchPlaceholderValue: 'Search leagues...',
                placeholder: true,
                placeholderValue: 'Select leagues',
                noResultsText: 'No leagues found',
                itemSelectText: ''
            });
            console.log('✅ Choices initialized on league');
        }
    }
    
    initializeChoices();
    
// ============================================
// FLATPICKR AVEC RACCOURCIS INTÉGRÉS
// ============================================
    setTimeout(function() {
        const dateInput = document.querySelector('.js-date-range');
        
        if (dateInput) {
            const flatpickrInstance = flatpickr(dateInput, {
                mode: 'range',
                dateFormat: 'Y-m-d',
                conjunction: ' to ',
                onClose: function(selectedDates, dateStr, instance) {
                    console.log('📅 Date selected:', dateStr);
                },
                onReady: function(selectedDates, dateStr, instance) {
                    // ✅ Ajoute les raccourcis dans le calendrier
                    const calendarContainer = instance.calendarContainer;
                    
                    // Crée le conteneur des raccourcis
                    const shortcutsDiv = document.createElement('div');
                    shortcutsDiv.className = 'flatpickr-shortcuts';
                    shortcutsDiv.style.cssText = `
                        padding: 10px;
                        border-top: 1px solid #e6e6e6;
                        display: grid;
                        grid-template-columns: repeat(4, 1fr);
                        gap: 6px;
                        background: #fff;
                    `;
                    
                    // Définit les raccourcis
                    const shortcuts = [
                        { label: 'Today', days: 0 },
                        { label: 'Yesterday', days: -1 },
                        { label: 'Last 7d', days: -7 },
                        { label: 'Last 30d', days: -30 },
                        { label: 'This month', type: 'thisMonth' },
                        { label: 'Last month', type: 'lastMonth' },
                        { label: 'This year', type: 'thisYear' },
                        { label: 'All time', type: 'allTime' }
                    ];
                    
                    shortcuts.forEach(shortcut => {
                        const btn = document.createElement('button');
                        btn.type = 'button';
                        btn.textContent = shortcut.label;
                        btn.className = 'flatpickr-shortcut-btn';
                        btn.style.cssText = `
                            padding: 6px 8px;
                            font-size: 12px;
                            font-family: "Host Grotesk", sans-serif;
                            background: #f8f9fa;
                            border: 1px solid #e0e0e0;
                            border-radius: 4px;
                            cursor: pointer;
                            transition: all 0.2s;
                            text-align: center;
                        `;
                        
                        btn.addEventListener('mouseenter', () => {
                            btn.style.background = '#7136c4';
                            btn.style.color = 'white';
                            btn.style.borderColor = '#7136c4';
                        });
                        
                        btn.addEventListener('mouseleave', () => {
                            btn.style.background = '#f8f9fa';
                            btn.style.color = 'black';
                            btn.style.borderColor = '#e0e0e0';
                        });
                        
                        btn.addEventListener('click', (e) => {
                            e.preventDefault();
                            
                            let start, end;
                            const now = new Date();
                            
                            if (shortcut.type === 'thisMonth') {
                                start = new Date(now.getFullYear(), now.getMonth(), 1);
                                end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
                            } else if (shortcut.type === 'lastMonth') {
                                start = new Date(now.getFullYear(), now.getMonth() - 1, 1);
                                end = new Date(now.getFullYear(), now.getMonth(), 0);
                            } else if (shortcut.type === 'thisYear') {
                                start = new Date(now.getFullYear(), 0, 1);
                                end = new Date(now.getFullYear(), 11, 31);
                            } else if (shortcut.type === 'allTime') {
                                start = new Date(2020, 0, 1);
                                end = new Date();
                            } else {
                                // Gestion par nombre de jours
                                end = new Date();
                                start = new Date();
                                if (shortcut.days < 0) {
                                    start.setDate(start.getDate() + shortcut.days);
                                } else {
                                    start = end;
                                }
                            }
                            
                            instance.setDate([start, end], true);
                            console.log(`📅 Shortcut: ${shortcut.label}`);
                        });
                        
                        shortcutsDiv.appendChild(btn);
                    });
                    
                    // Ajoute les raccourcis en bas du calendrier
                    calendarContainer.appendChild(shortcutsDiv);
                }
            });
            
            console.log('✅ Flatpickr initialized with shortcuts');
        }
    }, 200);

    // ============================================
    // FILTRE SPORT → LEAGUE
    // ============================================
    const sportSelect = document.querySelector('select[name="odds_filter[sport]"]');

    if (sportSelect) {
        const leaguesDataElement = document.getElementById('leagues-data');
        const leaguesData = leaguesDataElement ? JSON.parse(leaguesDataElement.textContent || '[]') : [];
        
        console.log('📊 Total leagues:', leaguesData.length);
        
        sportSelect.addEventListener('change', function() {
            const selectedSportId = this.value;
            console.log('🎯 Sport changed to:', selectedSportId);
            
            if (window.leagueChoices) {
                // Sauvegarde les valeurs sélectionnées
                const currentValues = window.leagueChoices.getValue(true);
                console.log('Current selected leagues:', currentValues);
                
                // Filtre les leagues par sport
                const filteredLeagues = selectedSportId 
                    ? leaguesData.filter(league => String(league.sport.id) === String(selectedSportId))
                    : leaguesData;
                
                console.log('Filtered leagues:', filteredLeagues.length);
                
                // Prépare les choix pour Choices.js
                const choicesArray = filteredLeagues.map(league => ({
                    value: String(league.id),
                    label: league.name,
                    selected: currentValues.includes(String(league.id))
                }));
                
                // Réinitialise Choices avec les nouvelles options
                window.leagueChoices.clearStore();
                window.leagueChoices.setChoices(choicesArray, 'value', 'label', true);
                
                console.log('✅ League choices updated');
            }
        });
    }
    // ============================================
    // 5. RESET BUTTON
    // ============================================
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('🔄 Reset clicked');
            window.location.href = window.location.pathname;
        });
    }
    
    // ============================================
    // 6. FORM SUBMIT DEBUG
    // ============================================
    const form = document.querySelector('.form-filters');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('🚀 Form submitting');
        });
    }

    // Tables triables
    function makeTableSortable(tableSelector) {
        const table = document.querySelector(tableSelector);
        if (!table) return;

        table.querySelectorAll('th').forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));

                const isNumeric = !isNaN(parseFloat(rows[0].children[index].textContent));

                rows.sort((a, b) => {
                    let aText = a.children[index].textContent.trim();
                    let bText = b.children[index].textContent.trim();

                    if (isNumeric) {
                        aText = parseFloat(aText);
                        bText = parseFloat(bText);
                        return aText - bText;
                    } else {
                        return aText.localeCompare(bText);
                    }
                });

                if (header.dataset.sorted === 'asc') {
                    rows.reverse();
                    header.dataset.sorted = 'desc';
                } else {
                    header.dataset.sorted = 'asc';
                }

                tbody.innerHTML = '';
                rows.forEach(r => tbody.appendChild(r));
            });
        });
    }

    makeTableSortable('.all_matchs');
    makeTableSortable('.avgtrj');


    // ============================================
    // EXPORT CSV AVEC FILTRES
    // ============================================

    const exportBtn = document.getElementById('export-csv-btn');
    const oddsFilterForm = document.querySelector('form[name="odds_filter"]'); // Formulaire des FILTRES seulement
    
    if (exportBtn && oddsFilterForm) {
        exportBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('📊 Export CSV cliqué');
            
            const params = new URLSearchParams();
            
            // ✅ Récupère les valeurs simples SANS le préfixe "odds_filter"
            const sport = oddsFilterForm.querySelector('[name="odds_filter[sport]"]')?.value;
            const match = oddsFilterForm.querySelector('[name="odds_filter[match]"]')?.value;
            const dateRange = oddsFilterForm.querySelector('[name="odds_filter[dateRange]"]')?.value;
            
            // Ajoute sport
            if (sport && sport !== '' && sport !== 'all') {
                params.append('sport', sport);
            }
            
            // Ajoute match
            if (match && match !== '' && match !== 'all') {
                params.append('match', match);
            }
            
            // Ajoute dateRange
            if (dateRange && dateRange !== '') {
                params.append('dateRange', dateRange);
            } else {
                alert('⚠️ Veuillez sélectionner une période de dates pour l\'export');
                return;
            }
            
            // ✅ Récupère les bookmakers cochés
            const bookmakerCheckboxes = oddsFilterForm.querySelectorAll('input[name="odds_filter[bookmaker][]"]:checked');
            if (bookmakerCheckboxes.length > 0) {
                const bookmakerValues = Array.from(bookmakerCheckboxes)
                    .map(cb => cb.value)
                    .filter(v => v !== 'all')
                    .join(',');
                
                if (bookmakerValues) {
                    params.append('bookmaker', bookmakerValues);
                }
            }
            
            // ✅ Récupère les leagues cochées
            const leagueCheckboxes = oddsFilterForm.querySelectorAll('input[name="odds_filter[league][]"]:checked');
            if (leagueCheckboxes.length > 0) {
                const leagueValues = Array.from(leagueCheckboxes)
                    .map(cb => cb.value)
                    .filter(v => v !== 'all')
                    .join(',');
                
                if (leagueValues) {
                    params.append('league', leagueValues);
                }
            }
            
            // Construit l'URL
            const exportUrl = '/odds/export-csv?' + params.toString();
            
            console.log('📤 Export URL:', exportUrl);
            console.log('📋 Params:', {
                sport: sport,
                match: match,
                dateRange: dateRange,
                bookmaker: params.get('bookmaker'),
                league: params.get('league')
            });
            
            // Lance le téléchargement
            window.location.href = exportUrl;
        });
    }
});

// ============================================
// GESTION DU SCRAPING AVEC PROGRESSION
// ============================================

(function() {
    'use strict';
    
    console.log('🧹 Initialisation du scraping...');
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScraping);
    } else {
        initScraping();
    }
    
    function initScraping() {
        console.log('🎬 Setup du scraping');
        
        // ✅ Sélection SPÉCIFIQUE du formulaire de scraping
        const scrapingForm = document.getElementById('scraping-form');
        
        if (!scrapingForm) {
            console.log('ℹ️ Pas de formulaire de scraping sur cette page');
            return;
        }
        
        // Vérification que c'est bien le bon formulaire
        if (scrapingForm.getAttribute('name') === 'odds_filter') {
            console.error('❌ ERREUR: Le formulaire de scraping a le même name que celui des filtres !');
            console.error('   Supprime name="odds_filter" du formulaire de scraping dans ton Twig');
            return;
        }
        
        console.log('✅ Formulaire de scraping trouvé:', scrapingForm);
        
        const sportSelect = document.getElementById('sport-scraping');
        const leagueSelect = document.getElementById('league-scraping');
        const submitBtn = document.getElementById('start-scraping-btn');
        
        if (!sportSelect || !leagueSelect || !submitBtn) {
            console.error('❌ Éléments manquants');
            return;
        }
        
        console.log('✅ Tous les éléments trouvés');
        
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoader = submitBtn.querySelector('.btn-loader');
        const progressContainer = document.getElementById('scraping-progress');
        
        const progressBarFill = document.getElementById('progress-bar-fill');
        const progressCount = document.getElementById('progress-count');
        const progressPercentage = document.getElementById('progress-percentage');
        const currentMatchName = document.getElementById('current-match-name');
        const bookmakersCount = document.getElementById('bookmakers-count');
        const progressMessage = document.getElementById('progress-message');

        let pollingInterval = null;
        let isSubmitting = false;

        const leaguesBySport = {
            'football': [
                { value: 'all', label: 'All leagues' },
                { value: 'ligue_1', label: 'Ligue 1' },
                { value: 'premier_league', label: 'Premier League' },
                { value: 'la_liga', label: 'La Liga' },
                { value: 'serie_a', label: 'Serie A' },
                { value: 'bundesliga', label: 'Bundesliga' }
            ],
            'basketball': [
                { value: 'all', label: 'All leagues' },
                { value: 'nba', label: 'NBA' },
                { value: 'euroleague', label: 'Euroleague' }
            ],
            'rugby': [
                { value: 'all', label: 'All leagues' },
                { value: 'top_14', label: 'Top 14' }
            ],
            'tennis': [
                { value: 'all', label: 'All leagues' },
                { value: 'atp', label: 'ATP' }
            ]
        };

        sportSelect.addEventListener('change', function() {
            const sport = this.value;
            console.log('🔄 Sport changé:', sport);
            
            leagueSelect.innerHTML = '<option value="">Sélectionner...</option>';
            
            if (sport && leaguesBySport[sport]) {
                leaguesBySport[sport].forEach(league => {
                    const option = document.createElement('option');
                    option.value = league.value;
                    option.textContent = league.label;
                    leagueSelect.appendChild(option);
                });
                
                leagueSelect.value = 'all';
                console.log('✅ Leagues chargées');
            }
        });

        scrapingForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (isSubmitting) {
                console.log('⚠️ Soumission déjà en cours');
                return false;
            }
            
            isSubmitting = true;
            console.log('🚀 Scraping soumis !');
            
            const sport = sportSelect.value;
            const league = leagueSelect.value;
            
            console.log('📝 Sport:', sport);
            console.log('📝 League:', league);
            
            if (!sport || sport === '') {
                alert('Select a sport');
                isSubmitting = false;
                return false;
            }
            
            if (!league || league === '') {
                alert('Select a league');
                isSubmitting = false;
                return false;
            }
            
            let leaguesToScrape = [];
            if (league === 'all') {
                leaguesToScrape = leaguesBySport[sport]
                    .filter(l => l.value !== 'all')
                    .map(l => l.value);
            } else {
                leaguesToScrape = [league];
            }
            
            console.log('✅ Leagues à scraper:', leaguesToScrape);
            
            submitBtn.disabled = true;
            if (btnText) btnText.style.display = 'none';
            if (btnLoader) btnLoader.style.display = 'inline';
            
            if (progressContainer) {
                progressContainer.style.display = 'block';
            }
            resetProgress();
            
            try {
                await startScrapingWithProgress(sport, leaguesToScrape);
            } catch (error) {
                console.error('❌ Erreur:', error);
                if (progressMessage) {
                    progressMessage.textContent = '❌ Erreur lors du scraping';
                }
            } finally {
                submitBtn.disabled = false;
                if (btnText) btnText.style.display = 'inline';
                if (btnLoader) btnLoader.style.display = 'none';
                isSubmitting = false;
            }
            
            return false;
        });
        
        console.log('✅ Listeners ajoutés');
        
        function resetProgress() {
            if (progressBarFill) progressBarFill.style.width = '0%';
            if (progressPercentage) progressPercentage.textContent = '0%';
            if (progressCount) progressCount.textContent = '0 / 0';
            if (currentMatchName) currentMatchName.textContent = '-';
            if (bookmakersCount) bookmakersCount.textContent = '-';
            if (progressMessage) progressMessage.textContent = 'Initialisation...';
        }
        
        async function startScrapingWithProgress(sport, leagues) {
            console.log('🎯 Démarrage:', sport, leagues);
            
            for (const league of leagues) {
                const scraper = `${sport}.${league}`;
                
                console.log(`📡 Lancement ${scraper}`);
                
                if (progressMessage) {
                    progressMessage.textContent = `🚀 ${league.replace('_', ' ')}...`;
                }
                
                try {
                    const formData = new FormData();
                    formData.append('sport', sport);
                    formData.append('league', league);

                    console.log('=== FormData Debug ===');
                    for (let pair of formData.entries()) {
                        console.log(pair[0] + ': ' + pair[1]);
                    }
                    
                    const response = await fetch('/odds/scraping/trigger', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    console.log('📊', result);
                    
                    if (result.success) {
                        await pollScrapingProgress(scraper);
                    } else {
                        if (progressMessage) progressMessage.textContent = `❌ ${league}`;
                        await new Promise(r => setTimeout(r, 2000));
                    }
                    
                } catch (error) {
                    console.error(`❌ ${league}:`, error);
                    if (progressMessage) progressMessage.textContent = `❌ ${league}`;
                    await new Promise(r => setTimeout(r, 2000));
                }
            }
            
            if (progressMessage) progressMessage.textContent = 'Finished';
            setTimeout(() => window.location.reload(), 3000);
        }

        let lastProgress = 0;
        
        async function pollScrapingProgress(scraper) {
            console.log('👂 DEBUT polling pour:', scraper);
            
            return new Promise((resolve) => {
                pollingInterval = setInterval(async () => {
                    try {
                        const url = `/api/scraping/status?scraper=${scraper}`;
                        console.log('📡 Appel:', url);
                        
                        const response = await fetch(url);
                        console.log('📥 Response status:', response.status);
                        
                        const data = await response.json();
                        console.log('📊 Data reçue:', data);
                        
                        if (data.status === 'idle') {
                            console.log('⏳ Status: idle, on attend...');
                            return;
                        }

                        if (data.current < lastProgress && data.status !== 'completed') {
                            console.log(`⚠️ Progression en arrière ignorée: ${data.current} < ${lastProgress}`);
                            return;
                        }

                        lastProgress = data.current;
                        
                        const progress = data.total > 0 ? (data.current / data.total) * 100 : 0;
                        console.log(`📈 Progress: ${data.current}/${data.total} = ${progress}%`);
                        
                        // Mise à jour de l'interface
                        if (progressCount) progressCount.textContent = `${data.current} / ${data.total}`;
                        if (progressPercentage) progressPercentage.textContent = `${Math.round(progress)}%`;
                        if (progressBarFill) progressBarFill.style.width = progress + '%';
                        
                        if (data.current_match && currentMatchName) {
                            console.log('🏟️ Match actuel:', data.current_match);
                            currentMatchName.textContent = data.current_match;
                        }
                        
                        if (data.bookmakers_count > 0 && bookmakersCount) {
                            console.log('📚 Bookmakers:', data.bookmakers_count);
                            bookmakersCount.textContent = `${data.bookmakers_count} bookmakers`;
                        }
                        
                        if (progressMessage) {
                            progressMessage.textContent = data.message || 'En cours...';
                        }
                        
                        // Si terminé
                        if (data.status === 'completed' || (data.current >= data.total && data.total > 0)) {
                            console.log('✅ SCRAPING TERMINÉ !');
                            lastProgress = 0;
                            clearInterval(pollingInterval);
                            
                            if (progressMessage) {
                                let msg = `${scraper} finished`;
                                if (data.matches_scraped) msg += `: ${data.matches_scraped} matchs`;
                                progressMessage.textContent = msg;
                            }
                            
                            setTimeout(() => resolve(), 2000);
                        }
                        
                    } catch (error) {
                        console.error('❌ Erreur polling:', error);
                    }
                }, 1500);
                
                setTimeout(() => {
                    console.log('⏱️ Timeout polling atteint');
                    if (pollingInterval) clearInterval(pollingInterval);
                    resolve();
                }, 600000);
            });
        }
    }
})();

// 🎨 MODE DÉMO - Progress Bar visible pour le style
(function() {
    const DEMO_MODE = false;  // ← Mets false quand tu as fini le style
    
    if (DEMO_MODE) {
        console.log('🎨 MODE DÉMO activé');
        
        // Récupère les éléments
        const progressContainer = document.getElementById('scraping-progress');
        const progressBarFill = document.getElementById('progress-bar-fill');
        const progressPercentage = document.getElementById('progress-percentage');
        const progressCount = document.getElementById('progress-count');
        const currentMatchName = document.getElementById('current-match');
        const bookmakersCount = document.getElementById('bookmakers-count');
        const progressMessage = document.getElementById('progress-message');
        
        // Log pour debug
        console.log('Progress container:', progressContainer);
        console.log('Progress bar fill:', progressBarFill);
        
        // Affiche et remplit
        if (progressContainer) {
            progressContainer.style.display = 'block';
            console.log('✅ Progress container affiché');
        }
        
        if (progressBarFill) {
            progressBarFill.style.width = '65%';
            progressBarFill.setAttribute('aria-valuenow', '65');
            console.log('✅ Barre à 65%');
        }
        
        if (progressPercentage) {
            progressPercentage.textContent = '65%';
        }
        
        if (progressCount) {
            progressCount.textContent = '12 / 18';
        }
        
        if (currentMatchName) {
            currentMatchName.textContent = 'Paris Saint-Germain - Olympique de Marseille';
        }
        
        if (bookmakersCount) {
            bookmakersCount.textContent = '13 bookmakers';
        }
        
        if (progressMessage) {
            progressMessage.textContent = '🚀 Scraping en cours...';
        }
        
        console.log('🎨 Valeurs de démo appliquées');
    }
})();
