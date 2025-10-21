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
    // 2. CHOICES.JS - LEAGUES
    // ============================================
    // let leaguesChoices = null;
    // const leaguesSelect = document.querySelector('select[name="odds_filter[leagues][]"]');
    
    // console.log('League select found:', leaguesSelect);
    // console.log('Choices available:', typeof Choices !== 'undefined');
    
    // if (leagueSelect) {
    //     // Attends un peu que Choices.js soit chargé
    //     setTimeout(function() {
    //         if (typeof Choices !== 'undefined') {
    //             leaguesChoices = new Choices(leaguesSelect, {
    //                 removeItemButton: true,
    //                 searchEnabled: true,
    //                 searchPlaceholderValue: 'Search leagues...',
    //                 placeholder: true,
    //                 placeholderValue: 'All leagues',
    //                 noResultsText: 'No leagues found',
    //                 itemSelectText: 'Click to select'
    //             });
    //             console.log('✅ Choices.js initialized');
    //         } else {
    //             console.error('❌ Choices.js not loaded');
    //         }
    //     }, 100);
    // }
    
    // ============================================
    // 3. FLATPICKR
    // ============================================
    const dateInput = document.querySelector('.js-date-range');
    let flatpickrInstance = null;
    
    if (dateInput) {
        flatpickrInstance = flatpickr(dateInput, {
            mode: 'range',
            dateFormat: 'Y-m-d',
            conjunction: ' to ',
            shorthandCurrentMonth: 'true',
            onClose: function(selectedDates, dateStr, instance) {
                console.log('📅 Date selected:', dateStr);
            }
        });
        console.log('✅ Flatpickr initialized');
    }

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
});
