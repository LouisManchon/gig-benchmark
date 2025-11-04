/**
 * ========================================
 * 🔐 NAVBAR - Gestion authentification (via session serveur)
 * ========================================
 * Affiche/cache les boutons en interrogeant /auth/status
 */

document.addEventListener('DOMContentLoaded', async function () {
  console.log('🔍 Navbar Auth - Initialisation...');

  // 1️⃣ Récupération des éléments de la navbar
  const userStatus = document.getElementById('user-logged-in');
  const btnLogout  = document.getElementById('btn-logout');
  const btnLogin   = document.getElementById('btn-login');
  const btnRegister= document.getElementById('btn-register');

  try {
    // 2️⃣ Interroger le serveur (source d'autorité)
    const res = await fetch('/auth/status', { credentials: 'same-origin' });
    const st  = await res.json();

    console.log('📦 loggedIn (session):', st.loggedIn);

    if (st.loggedIn) {
      // ✅ UTILISATEUR CONNECTÉ
      if (userStatus) userStatus.style.display = 'flex';
      if (btnLogout)  btnLogout.style.display  = 'block';
      if (btnLogin)   btnLogin.style.display   = 'none';
      if (btnRegister)btnRegister.style.display= 'none';

      // Optionnel: afficher le username si dispo
      if (st.user && st.user.username && userStatus) {
        const nameEl = userStatus.querySelector('.js-username');
        if (nameEl) nameEl.textContent = st.user.username;
      }

      console.log('✅ Affichage: Logged in + Logout');

    } else {
      // ❌ UTILISATEUR NON CONNECTÉ
      if (userStatus) userStatus.style.display = 'none';
      if (btnLogout)  btnLogout.style.display  = 'none';
      if (btnLogin)   btnLogin.style.display   = 'block';
      if (btnRegister)btnRegister.style.display= 'block';

      console.log('❌ Affichage: Login + Register');
    }
  } catch (e) {
    console.error('❌ Navbar Auth - Erreur status:', e);
    // En cas d'erreur réseau, fallback = non connecté
    if (userStatus) userStatus.style.display = 'none';
    if (btnLogout)  btnLogout.style.display  = 'none';
    if (btnLogin)   btnLogin.style.display   = 'block';
    if (btnRegister)btnRegister.style.display= 'block';
  }

  // 3️⃣ Gestion du logout (clean + redirection)
  if (btnLogout) {
    btnLogout.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        // Nettoyage "défensif" côté front (si jamais un vieux token traîne)
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        // Appel serveur pour fermer la session
        window.location.href = '/logout';
      } catch (err) {
        console.error('❌ Logout error:', err);
        window.location.href = '/logout';
      }
    });
  }

  console.log('✅ Navbar Auth - Configuration terminée');
});