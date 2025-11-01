/**
 * ========================================
 * 🔐 NAVBAR - Gestion authentification
 * ========================================
 * Affiche/cache les boutons selon le token JWT
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔍 Navbar Auth - Initialisation...');

    // 1️⃣ Récupérer le token du localStorage
    const accessToken = localStorage.getItem('access_token');
    const isLoggedIn = !!accessToken; // true si token existe

    console.log('📦 Token présent:', isLoggedIn);

    // 2️⃣ Récupérer les éléments de la navbar
    const userStatus = document.getElementById('user-logged-in');
    const btnLogout = document.getElementById('btn-logout');
    const btnLogin = document.getElementById('btn-login');
    const btnRegister = document.getElementById('btn-register');

    // 3️⃣ Afficher/cacher selon l'état de connexion
    if (isLoggedIn) {
        // ✅ UTILISATEUR CONNECTÉ
        console.log('✅ Affichage: Logged in + Logout');

        if (userStatus) userStatus.style.display = 'flex';
        if (btnLogout) btnLogout.style.display = 'block';
        if (btnLogin) btnLogin.style.display = 'none';
        if (btnRegister) btnRegister.style.display = 'none';

    } else {
        // ❌ UTILISATEUR NON CONNECTÉ
        console.log('❌ Affichage: Login + Register');

        if (userStatus) userStatus.style.display = 'none';
        if (btnLogout) btnLogout.style.display = 'none';
        if (btnLogin) btnLogin.style.display = 'block';
        if (btnRegister) btnRegister.style.display = 'block';
    }

    console.log('✅ Navbar Auth - Configuration terminée');
});
