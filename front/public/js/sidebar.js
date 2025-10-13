// side bar closed

document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });
});


/*/ init button for filters

document.getElementById('reset-btn').addEventListener('click', () => {
    document.querySelector('.aside-form').reset();
    window.location.href = window.location.pathname;
}); /*/

// toggle for table

document.addEventListener('DOMContentLoaded', () => {
    function makeTableSortable(tableSelector) {
        const table = document.querySelector(tableSelector);
        if (!table) return;

        table.querySelectorAll('th').forEach((header, index) => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));

                const isNumeric = !isNaN(parseFloat(rows[0].children[index].textContent));

                // sort
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

                // Toggle ordre
                if (header.dataset.sorted === 'asc') {
                    rows.reverse();
                    header.dataset.sorted = 'desc';
                } else {
                    header.dataset.sorted = 'asc';
                }

                // reinject
                tbody.innerHTML = '';
                rows.forEach(r => tbody.appendChild(r));
            });
        });
    }

    // Applique à tes tables
    makeTableSortable('.all_matchs');
    makeTableSortable('.avgtrj'); // si tu veux garder le tri sur l'autre table
});


// check box

document.addEventListener('DOMContentLoaded', () => {
    // Choices.js pour Bookmakers
    const bookmakerSelect = document.querySelector('.js-bookmaker-select');
    if (bookmakerSelect) {
        const choices = new Choices(bookmakerSelect, {
            removeItemButton: true,
            placeholder: true,
            placeholderValue: 'All',
            searchEnabled: true
        });
    }

    // Flatpickr pour dateRange
    flatpickr('.js-date-range', {
        mode: 'range',
        dateFormat: 'Y-m-d',
        onClose: function(selectedDates, dateStr, instance) {
            instance.element.form.submit();
        }
    });

    document.querySelector('#filter-button').addEventListener('click', function() {
    this.form.submit();
    });

});

