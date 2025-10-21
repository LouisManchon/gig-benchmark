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
});
