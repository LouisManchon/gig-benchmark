document.addEventListener('DOMContentLoaded', () => {
    // Sidebar toggle
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // init button for filters

    document.getElementById('reset-btn').addEventListener('click', () => {
            document.querySelector('.aside-form').reset();
            window.location.href = window.location.pathname;
        });

    // Choices.js pour Bookmakers
    const bookmakerSelect = document.querySelector('.js-bookmaker-select');
    let choicesInstance = null;
    
    if (bookmakerSelect) {
        choicesInstance = new Choices(bookmakerSelect, {
            removeItemButton: true,
            placeholder: true,
            placeholderValue: 'All',
            searchEnabled: true,
            itemSelectText: '',
        });
    }

    // Flatpickr pour dateRange
    const dateInput = document.querySelector('.js-date-range');
    let flatpickrInstance = null;
    
    if (dateInput) {
        flatpickrInstance = flatpickr(dateInput, {
            mode: 'range',
            dateFormat: 'Y-m-d',
            conjunction: ' to ',  // ✅ Important pour le format
            onClose: function(selectedDates, dateStr, instance) {
                console.log('Date selected:', dateStr);  // ✅ DEBUG
            }
        });
        console.log('Flatpickr initialized:', flatpickrInstance);
    } else {
        console.error('Date input with class .js-date-range not found!');
    }

    // AJAX for filters
    const filterForm = document.querySelector('form[name="odds_filter"]');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault(); // no refresh
            
            // Rdata from form
            const formData = new FormData(this);
            const params = new URLSearchParams(formData);
            
            //Send AJAX request
            fetch('?' + params.toString(), {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                // Parse HTML
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Update tables
                const newAvgTable = doc.querySelector('.avgtrj tbody');
                const newMatchTable = doc.querySelector('.all_matchs tbody');
                
                if (newAvgTable) {
                    document.querySelector('.avgtrj tbody').innerHTML = newAvgTable.innerHTML;
                }
                if (newMatchTable) {
                    document.querySelector('.all_matchs tbody').innerHTML = newMatchTable.innerHTML;
                }
                
                // update URL
                history.pushState({}, '', '?' + params.toString());
            })
            .catch(error => {
                console.error('Erreur:', error);
            });
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
