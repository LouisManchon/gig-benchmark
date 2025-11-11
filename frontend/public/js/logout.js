/**
 * 🚪 LOGOUT FUNCTIONALITY
 * Handles logout (localStorage + Symfony session)
 */

document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.querySelector('.btn-logout');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();

            console.log('🚪 Logging out...');

            // 1. Remove tokens from localStorage
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');

            // 2. Confirmation message
            console.log('✅ Tokens removed from localStorage');

            // 3. Redirect to login
            window.location.href = '/login';
        });
    }
});