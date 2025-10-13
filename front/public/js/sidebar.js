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

// main.js

// Fonction d'initialisation des plugins
function initPlugins() {
    // --- Choices.js pour multi-select ---
    document.querySelectorAll('.js-bookmaker-select').forEach(select => {
        if (!select.dataset.choicesInit) {
            new Choices(select, {
                removeItemButton: true,
                placeholder: true,
                placeholderValue: 'All',
                searchEnabled: true
            });
            select.dataset.choicesInit = true; // marque comme initialisé
        }
    });

    // --- Flatpickr pour dateRange ---
    document.querySelectorAll('.js-date-range').forEach(input => {
        if (!input._flatpickr) {
            flatpickr(input, {
                mode: 'range',
                dateFormat: 'Y-m-d',
                // Retirer le submit automatique pour éviter les conflits
                onClose: function(selectedDates, dateStr, instance) {
                    // Optionnel : tu peux déclencher un submit ici si tu veux
                    // instance.element.form.submit();
                }
            });
        }
    });
}

// Exécute l'initialisation après que la page est chargée
document.addEventListener('DOMContentLoaded', initPlugins);

