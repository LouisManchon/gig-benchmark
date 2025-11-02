document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded');
    
    // ============================================
    // 1. SIDEBAR TOGGLE
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
    // 2. CHOICES.JS - BOOKMAKER + LEAGUE + MATCH
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
        if (bookmakerSelect && !bookmakerSelect.classList.contains('choices__input')) {
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
        if (leagueSelect && !leagueSelect.classList.contains('choices__input')) {
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
        
        // Match - AJOUT ICI
        const matchSelect = document.querySelector('select[name="odds_filter[match]"]');
        if (matchSelect && !matchSelect.classList.contains('choices__input')) {
            if (matchSelect.options.length === 0) {
                const placeholderOption = document.createElement('option');
                placeholderOption.value = '';
                placeholderOption.textContent = 'All matches';
                matchSelect.appendChild(placeholderOption);
            }

            window.matchChoices = new Choices(matchSelect, {
                searchEnabled: true,
                searchPlaceholderValue: 'Search a match...',
                placeholder: true,
                placeholderValue: 'All matches',
                noResultsText: 'No match found',
                itemSelectText: '',
                shouldSort: false,
                removeItemButton: false,
            });
            console.log('✅ Choices initialized on match');

            // 👇 Écouter les changements de sélection
            matchSelect.addEventListener('change', function() {
                const selectedValue = matchSelect.value;
                const selectedText = matchSelect.options[matchSelect.selectedIndex]?.text || 'All matches';
                console.log('✅ Match selected:', { value: selectedValue, text: selectedText });
            }, true);

            // Charger les données des matchs et initialiser le filtrage
            initializeMatchFilter();
        }
    }

    initializeChoices();

    // ============================================
    // FILTRE MATCH DYNAMIQUE
    // ============================================
    function initializeMatchFilter() {
        console.log('🎯 Initializing match filter');
        
        const matchesDataElement = document.getElementById('matches-data');
        let allMatches = [];
        
        if (matchesDataElement) {
            try {
                allMatches = JSON.parse(matchesDataElement.textContent);
                console.log('✅ Matches data loaded:', allMatches.length);
            } catch (e) {
                console.error('❌ Error parsing matches data:', e);
                return;
            }
        } else {
            console.error('❌ matches-data element not found');
            return;
        }
        
        if (!window.matchChoices) {
            console.error('❌ matchChoices not initialized');
            return;
        }
        
        // Fonction pour mettre à jour la liste des matchs
        function updateMatchList() {
            const sportSelect = document.querySelector('select[name="odds_filter[sport]"]');
            const selectedSport = sportSelect ? sportSelect.value : null;
            const selectedLeagues = window.leagueChoices ? 
                window.leagueChoices.getValue(true).filter(v => v !== 'all' && v !== '') 
                : [];
            
            console.log('🔍 Filtering matches:', { sport: selectedSport, leagues: selectedLeagues });
            
            // Filtrer les matchs
            let filteredMatches = allMatches;
            
            // Filtre par sport
            if (selectedSport && selectedSport !== 'all' && selectedSport !== '') {
                filteredMatches = filteredMatches.filter(match => {
                    const matchSportId = match.league?.sport?.id;
                    return String(matchSportId) === String(selectedSport);
                });
                console.log('   → After sport filter:', filteredMatches.length);
            }
            
            // Filtre par ligues
            if (selectedLeagues.length > 0) {
                filteredMatches = filteredMatches.filter(match => {
                    const matchLeagueId = match.league?.id;
                    return selectedLeagues.includes(String(matchLeagueId));
                });
                console.log('   → After league filter:', filteredMatches.length);
            }
            
            // Préparer les choix pour Choices.js
            const choicesArray = [
                { value: '', label: 'All matches', selected: false }
            ];
            
            filteredMatches.forEach(match => {
                const homeTeam = match.home_team?.name || 'Unknown';
                const awayTeam = match.away_team?.name || 'Unknown';
                const matchName = `${homeTeam} - ${awayTeam}`;
                
                choicesArray.push({
                    value: String(match.id),
                    label: matchName,
                    selected: false
                });
            });
            
            console.log('📋 Updating choices with', choicesArray.length, 'options');

            // Mettre à jour Choices.js
            window.matchChoices.clearStore();
            window.matchChoices.setChoices(choicesArray, 'value', 'label', true);

            console.log('✅ Match choices updated');
        }
        
        // Écouter les changements de sport
        const sportSelect = document.querySelector('select[name="odds_filter[sport]"]');
        if (sportSelect) {
            sportSelect.addEventListener('change', function() {
                console.log('🔄 Sport changed');
                updateMatchList();
            });
        }
        
        // Écouter les changements de ligue
        if (window.leagueChoices) {
            const leagueElement = window.leagueChoices.passedElement.element;
            leagueElement.addEventListener('change', function() {
                console.log('🔄 League changed');
                updateMatchList();
            });
        }
        
        // Initialiser au chargement
        console.log('🚀 Initial match list update');
        updateMatchList();
    }
    
    // ============================================
    // 3. FLATPICKR AVEC RACCOURCIS
    // ============================================
    setTimeout(function() {
        const dateInput = document.querySelector('.js-date-range');
        
        if (dateInput && !dateInput._flatpickr) {
            const flatpickrInstance = flatpickr(dateInput, {
                mode: 'range',
                dateFormat: 'Y-m-d',
                conjunction: ' to ',
                onClose: function(selectedDates, dateStr, instance) {
                    console.log('📅 Date selected:', dateStr);
                },
                onReady: function(selectedDates, dateStr, instance) {
                    const calendarContainer = instance.calendarContainer;
                    
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
                                end = new Date();
                                start = new Date();
                                if (shortcut.days < 0) {
                                    start.setDate(start.getDate() + shortcut.days);
                                } else {
                                    start = end;
                                }
                            }
                            
                            instance.setDate([start, end], true);
                        });
                        
                        shortcutsDiv.appendChild(btn);
                    });
                    
                    calendarContainer.appendChild(shortcutsDiv);
                }
            });
            
            console.log('✅ Flatpickr initialized');
        }
    }, 200);

    
    // ============================================
    // 6. RESET BUTTON
    // ============================================
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = window.location.pathname;
        });
    }

// ============================================
    // GESTION SOUMISSION FORMULAIRE
    // ============================================
    const oddsFilterFor = document.querySelector('form[name="odds_filter"]');
    if (oddsFilterFor) {
        oddsFilterFor.addEventListener('submit', function(e) {
            console.log('🚀 Form submitting...');
            
            // Vérifier la valeur du match
            if (window.matchChoices) {
                const matchValue = window.matchChoices.getValue(true);
                console.log('📋 Match value from Choices:', matchValue);
                
                const matchSelect = document.querySelector('select[name="odds_filter[match]"]');
                console.log('📋 Match select value:', matchSelect ? matchSelect.value : 'null');
                
                // Si différents, forcer la mise à jour
                if (matchSelect && matchValue && matchSelect.value !== matchValue) {
                    console.log('⚠️ Values differ! Updating select...');
                    matchSelect.value = matchValue;
                }
            }
            
            // Log tous les champs
            const formData = new FormData(this);
            console.log('📤 Form data being sent:');
            for (let [key, value] of formData.entries()) {
                console.log(`   ${key}: ${value}`);
            }
        });
    }
    // ============================================
    // 7. TABLES TRIABLES
    // ============================================
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
    // 8. EXPORT CSV
    // ============================================
    const exportBtn = document.getElementById('export-csv-btn');
    const oddsFilterForm = document.querySelector('form[name="odds_filter"]');
    
    if (exportBtn && oddsFilterForm) {
        exportBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const params = new URLSearchParams();
            
            const sport = oddsFilterForm.querySelector('[name="odds_filter[sport]"]')?.value;
            const match = oddsFilterForm.querySelector('[name="odds_filter[match]"]')?.value;
            const dateRange = oddsFilterForm.querySelector('[name="odds_filter[dateRange]"]')?.value;
            
            if (sport && sport !== '' && sport !== 'all') {
                params.append('sport', sport);
            }
            
            if (match && match !== '' && match !== 'all') {
                params.append('match', match);
            }
            
            if (dateRange && dateRange !== '') {
                params.append('dateRange', dateRange);
            } else {
                alert('⚠️ Veuillez sélectionner une période');
                return;
            }
            
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
            
            window.location.href = '/odds/export-csv?' + params.toString();
        });
    }
});

// ============================================
// GESTION DU SCRAPING
// ============================================
(function() {
    'use strict';
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScraping);
    } else {
        initScraping();
    }
    
    function initScraping() {
        const scrapingForm = document.getElementById('scraping-form');
        
        if (!scrapingForm) {
            return;
        }
        
        const sportSelect = document.getElementById('sport-scraping');
        const leagueSelect = document.getElementById('league-scraping');
        const submitBtn = document.getElementById('start-scraping-btn');
        
        if (!sportSelect || !leagueSelect || !submitBtn) {
            return;
        }
        
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
                { value: 'bundesliga', label: 'Bundesliga' },
                { value: 'champions_league', label: 'UEFA Champions League'}
            ],
            'basketball': [
                { value: 'all', label: 'All leagues' },
                { value: 'nba', label: 'NBA' },
                { value: 'euroleague', label: 'Euroleague' }
            ],
            'rugby': [
                { value: 'all', label: 'All leagues' },
                { value: 'top14', label: 'Top 14' }
            ],
            'tennis': [
                { value: 'all', label: 'All leagues' },
                { value: 'atp', label: 'ATP' }
            ]
        };

        sportSelect.addEventListener('change', function() {
            const sport = this.value;
            leagueSelect.innerHTML = '';
            
            if (sport && leaguesBySport[sport]) {
                leaguesBySport[sport].forEach(league => {
                    const option = document.createElement('option');
                    option.value = league.value;
                    option.textContent = league.label;
                    leagueSelect.appendChild(option);
                });
                
                leagueSelect.value = 'all';
            }
        });

        scrapingForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (isSubmitting) {
                return false;
            }
            
            isSubmitting = true;
            
            const sport = sportSelect.value;
            const league = leagueSelect.value;
            
            if (!sport || !league) {
                alert('Select sport and league');
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
                console.error('❌ Error:', error);
                if (progressMessage) {
                    progressMessage.textContent = '❌ Error';
                }
            } finally {
                submitBtn.disabled = false;
                if (btnText) btnText.style.display = 'inline';
                if (btnLoader) btnLoader.style.display = 'none';
                isSubmitting = false;
            }
            
            return false;
        });
        
        function resetProgress() {
            if (progressBarFill) progressBarFill.style.width = '0%';
            if (progressPercentage) progressPercentage.textContent = '0%';
            if (progressCount) progressCount.textContent = '0 / 0';
            if (currentMatchName) currentMatchName.textContent = '-';
            if (bookmakersCount) bookmakersCount.textContent = '-';
            if (progressMessage) progressMessage.textContent = 'Initializing...';
        }
        
        async function startScrapingWithProgress(sport, leagues) {
            for (const league of leagues) {
                const scraper = `${sport}.${league}`;
                
                if (progressMessage) {
                    progressMessage.textContent = `🚀 ${league.replace('_', ' ')}...`;
                }
                
                try {
                    const formData = new FormData();
                    formData.append('sport', sport);
                    formData.append('league', league);
                    
                    const response = await fetch('/odds/scraping/trigger', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
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
            return new Promise((resolve) => {
                pollingInterval = setInterval(async () => {
                    try {
                        const response = await fetch(`/api/scraping/status?scraper=${scraper}`);
                        const data = await response.json();
                        
                        if (data.status === 'idle') {
                            return;
                        }

                        if (data.current < lastProgress && data.status !== 'completed') {
                            return;
                        }

                        lastProgress = data.current;
                        
                        const progress = data.total > 0 ? (data.current / data.total) * 100 : 0;
                        
                        if (progressCount) progressCount.textContent = `${data.current} / ${data.total}`;
                        if (progressPercentage) progressPercentage.textContent = `${Math.round(progress)}%`;
                        if (progressBarFill) progressBarFill.style.width = progress + '%';
                        
                        if (data.current_match && currentMatchName) {
                            currentMatchName.textContent = data.current_match;
                        }
                        
                        if (data.bookmakers_count > 0 && bookmakersCount) {
                            bookmakersCount.textContent = `${data.bookmakers_count} bookmakers`;
                        }
                        
                        if (progressMessage) {
                            progressMessage.textContent = data.message || 'In progress...';
                        }
                        
                        if (data.status === 'completed' || (data.current >= data.total && data.total > 0)) {
                            lastProgress = 0;
                            clearInterval(pollingInterval);
                            
                            if (progressMessage) {
                                let msg = `${scraper} finished`;
                                if (data.matches_scraped) msg += `: ${data.matches_scraped} matches`;
                                progressMessage.textContent = msg;
                            }
                            
                            setTimeout(() => resolve(), 2000);
                        }
                        
                    } catch (error) {
                        console.error('❌ Polling error:', error);
                    }
                }, 1500);
                
                setTimeout(() => {
                    if (pollingInterval) clearInterval(pollingInterval);
                    resolve();
                }, 600000);
            });
        }
    }
})();
