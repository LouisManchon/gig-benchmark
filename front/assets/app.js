import './bootstrap.js';
/*
 * Welcome to your app's main JavaScript file!
 *
 * This file will be included onto the page via the importmap() Twig function,
 * which should already be in your base.html.twig.
 */
import './styles/app.css';

document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');

    if (!sidebar || !toggleBtn) return; // sécurité si l'élément n'existe pas

    toggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('sidebar-closed');
        toggleBtn.textContent = sidebar.classList.contains('sidebar-closed') ? '➡' : '⬅';
    });
});


console.log('This log comes from assets/app.js - welcome to AssetMapper! 🎉');
