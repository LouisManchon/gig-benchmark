/**
 * 🚪 LOGOUT FUNCTIONALITY
 * Gère la déconnexion (localStorage + session Symfony)
 */

document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.querySelector('.btn-logout');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();

            console.log('🚪 Déconnexion en cours...');

            // 1. Supprimer les tokens du localStorage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');

            // 2. Message de confirmation
            console.log('✅ Tokens supprimés du localStorage');

            // 3. Redirection vers login
            window.location.href = '/login';
        });
    }
});