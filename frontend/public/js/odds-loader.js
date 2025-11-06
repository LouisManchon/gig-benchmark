// Chargement asynchrone des odds
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si on est sur la page odds et que le formulaire n'a pas été soumis
    const urlParams = new URLSearchParams(window.location.search);

    // Chercher les paramètres qui commencent par 'odds_filter'
    let formSubmitted = false;
    for (let [key, value] of urlParams.entries()) {
        if (key.startsWith('odds_filter[') && value) {
            formSubmitted = true;
            break;
        }
    }

    // Si le formulaire a été soumis, ne pas charger en AJAX (déjà chargé par PHP)
    if (formSubmitted) {
        console.log('Form was submitted, skipping AJAX load');
        return;
    }

    console.log('Initial page load - loading data via AJAX...');

    // Afficher un loader
    showLoader();

    // Récupérer la date du jour (déjà dans le champ dateRange)
    const dateRangeInput = document.querySelector('input[name="odds_filter[dateRange]"]');
    const todayDate = dateRangeInput ? dateRangeInput.value : '';

    // Construire l'URL de l'API - Utiliser le chemin Symfony (frontend-api pour éviter le conflit avec Django)
    const baseUrl = window.location.origin;
    const apiUrl = baseUrl + '/frontend-api/odds/load' + (todayDate ? '?dateRange=' + encodeURIComponent(todayDate) : '');

    console.log('Fetching data from:', apiUrl);

    // Appel AJAX
    fetch(apiUrl)
        .then(response => {
            console.log('Response received:', response.status, response.statusText);
            if (!response.ok) {
                throw new Error('HTTP error! status: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('Data parsed:', data);
            if (data.success) {
                console.log('✅ Data loaded successfully');
                console.log('   → Odds count:', data.odds ? data.odds.length : 0);
                console.log('   → AvgTrj count:', data.avgTrj ? data.avgTrj.length : 0);

                // Remplir la table avgTrj
                fillAvgTrjTable(data.avgTrj);

                // Remplir la table des odds
                fillOddsTable(data.odds);

                // Masquer le loader
                hideLoader();
            } else {
                console.error('❌ Error loading data:', data.error);
                hideLoader();
                showError('Error when charghing data: ' + data.error);
            }
        })
        .catch(error => {
            console.error('❌ Fetch error:', error);
            hideLoader();
            showError('Error when charghing data: ' + error.message);
        });
});

function showLoader() {
    const tables = document.querySelector('.tables');
    if (tables) {
        // Ne pas remplacer innerHTML, juste ajouter le loader au début
        const loader = document.createElement('div');
        loader.className = 'loader-container';
        loader.innerHTML = '<div class="loader"></div><p>Search data...</p>';
        tables.insertBefore(loader, tables.firstChild);

        // Masquer les tables pendant le chargement
        const avgtrjTable = tables.querySelector('.avgtrj');
        const allMatchsTable = tables.querySelector('.all_matchs');
        if (avgtrjTable) avgtrjTable.style.display = 'none';
        if (allMatchsTable) allMatchsTable.style.display = 'none';
    }
}

function hideLoader() {
    const loaderContainer = document.querySelector('.loader-container');
    if (loaderContainer) {
        loaderContainer.remove();
    }

    // Réafficher les tables
    const tables = document.querySelector('.tables');
    if (tables) {
        const avgtrjTable = tables.querySelector('.avgtrj');
        const allMatchsTable = tables.querySelector('.all_matchs');
        if (avgtrjTable) avgtrjTable.style.display = '';
        if (allMatchsTable) allMatchsTable.style.display = '';
    }
}

function showError(message) {
    const tables = document.querySelector('.tables');
    if (tables) {
        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = message;
        tables.insertBefore(error, tables.firstChild);
    }
}

function fillAvgTrjTable(avgTrjData) {
    console.log('📊 fillAvgTrjTable called with:', avgTrjData);
    const tbody = document.querySelector('.avgtrj tbody');
    if (!tbody) {
        console.error('❌ avgtrj tbody not found!');
        return;
    }

    console.log('✅ avgtrj tbody found:', tbody);
    tbody.innerHTML = '';

    if (!avgTrjData || avgTrjData.length === 0) {
        console.log('⚠️ No avgTrj data');
        tbody.innerHTML = '<tr><td colspan="4">No data found.</td></tr>';
        return;
    }

    console.log('📝 Adding', avgTrjData.length, 'rows to avgtrj table');

    avgTrjData.forEach(row => {
        const tr = document.createElement('tr');

        // Bookmaker
        const tdBookmaker = document.createElement('td');
        tdBookmaker.textContent = row.bookmaker;
        tr.appendChild(tdBookmaker);

        // Average RTP
        const tdAvgTrj = document.createElement('td');
        tdAvgTrj.textContent = row.avgTrj.toFixed(2) + '%';
        if (row.avgTrj > 90) {
            tdAvgTrj.classList.add('trj-high');
        } else if (row.avgTrj < 90) {
            tdAvgTrj.classList.add('trj-low');
        }
        tr.appendChild(tdAvgTrj);

        // Evolution
        const tdEvol = document.createElement('td');
        tdEvol.classList.add('evol-container');

        const spanArrow = document.createElement('span');
        if (row.evolution === 1) {
            spanArrow.innerHTML = '<span class="arrow-up">↑</span>';
        } else if (row.evolution === -1) {
            spanArrow.innerHTML = '<span class="arrow-down">↓</span>';
        } else {
            spanArrow.innerHTML = '<span class="arrow-stable">→</span>';
        }
        tdEvol.appendChild(spanArrow);

        const spanPrevious = document.createElement('span');
        spanPrevious.classList.add('previous-trj');
        spanPrevious.textContent = row.previousAvgTrj ? row.previousAvgTrj.toFixed(2) + '%' : '-';
        tdEvol.appendChild(spanPrevious);

        tr.appendChild(tdEvol);
        tbody.appendChild(tr);
    });
}

function fillOddsTable(oddsData) {
    console.log('📊 fillOddsTable called with:', oddsData);
    const tbody = document.querySelector('.all_matchs tbody');
    if (!tbody) {
        console.error('❌ all_matchs tbody not found!');
        return;
    }

    console.log('✅ all_matchs tbody found:', tbody);
    tbody.innerHTML = '';

    if (!oddsData || oddsData.length === 0) {
        console.log('⚠️ No odds data');
        tbody.innerHTML = '<tr><td colspan="7">No odds available.</td></tr>';
        return;
    }

    console.log('📝 Adding', oddsData.length, 'rows to odds table');

    oddsData.forEach(item => {
        const tr = document.createElement('tr');

        // Match
        const tdMatch = document.createElement('td');
        const homeTeam = item.odd.match.home_team.name || 'Unknown';
        const awayTeam = item.odd.match.away_team.name || 'Unknown';
        tdMatch.textContent = homeTeam + ' - ' + awayTeam;
        tr.appendChild(tdMatch);

        // Bookmaker
        const tdBookmaker = document.createElement('td');
        tdBookmaker.textContent = item.odd.bookmaker.name || 'Unknown';
        tr.appendChild(tdBookmaker);

        // Home
        const tdHome = document.createElement('td');
        tdHome.textContent = item.odd.cote1 || '-';
        tr.appendChild(tdHome);

        // Draw
        const tdDraw = document.createElement('td');
        tdDraw.textContent = item.odd.coteN || '-';
        tr.appendChild(tdDraw);

        // Away
        const tdAway = document.createElement('td');
        tdAway.textContent = item.odd.cote2 || '-';
        tr.appendChild(tdAway);

        // RTP
        const tdTrj = document.createElement('td');
        tdTrj.textContent = item.odd.trj.toFixed(2) + '%';
        if (item.odd.trj > 90) {
            tdTrj.classList.add('trj-high');
        } else if (item.odd.trj < 90) {
            tdTrj.classList.add('trj-low');
        }
        tr.appendChild(tdTrj);

        // Evolution
        const tdEvol = document.createElement('td');
        tdEvol.classList.add('evol-container');

        const spanArrow = document.createElement('span');
        if (item.evolution === 1) {
            spanArrow.innerHTML = '<span class="arrow-up">↑</span>';
        } else if (item.evolution === -1) {
            spanArrow.innerHTML = '<span class="arrow-down">↓</span>';
        } else {
            spanArrow.innerHTML = '<span class="arrow-stable">→</span>';
        }
        tdEvol.appendChild(spanArrow);

        const spanPrevious = document.createElement('span');
        spanPrevious.classList.add('previous-trj');
        spanPrevious.textContent = item.previousTrj ? item.previousTrj.toFixed(2) + '%' : '-';
        tdEvol.appendChild(spanPrevious);

        tr.appendChild(tdEvol);
        tbody.appendChild(tr);
    });
}
