/**
 * ========================================
 * 🔐 NAVBAR - Authentication management (via server session)
 * ========================================
 * Show/hide buttons by querying /auth/status
 */

document.addEventListener('DOMContentLoaded', async function () {
  console.log('🔍 Navbar Auth - Initialization...');

  // 1️⃣ Get navbar elements
  const userStatus = document.getElementById('user-logged-in');
  const btnLogout  = document.getElementById('btn-logout');
  const btnLogin   = document.getElementById('btn-login');
  const btnRegister= document.getElementById('btn-register');

  try {
    // 2️⃣ Query the server (source of authority)
    const res = await fetch('/auth/status', { credentials: 'same-origin' });
    const st  = await res.json();

    console.log('📦 loggedIn (session):', st.loggedIn);

    if (st.loggedIn) {
      // ✅ USER LOGGED IN
      if (userStatus) userStatus.style.display = 'flex';
      if (btnLogout)  btnLogout.style.display  = 'block';
      if (btnLogin)   btnLogin.style.display   = 'none';
      if (btnRegister)btnRegister.style.display= 'none';

      // Optional: display username if available
      if (st.user && st.user.username && userStatus) {
        const nameEl = userStatus.querySelector('.js-username');
        if (nameEl) nameEl.textContent = st.user.username;
      }

      console.log('✅ Display: Logged in + Logout');

    } else {
      // ❌ USER NOT LOGGED IN
      if (userStatus) userStatus.style.display = 'none';
      if (btnLogout)  btnLogout.style.display  = 'none';
      if (btnLogin)   btnLogin.style.display   = 'block';
      if (btnRegister)btnRegister.style.display= 'block';

      console.log('❌ Display: Login + Register');
    }
  } catch (e) {
    console.error('❌ Navbar Auth - Status error:', e);
    // In case of network error, fallback = not logged in
    if (userStatus) userStatus.style.display = 'none';
    if (btnLogout)  btnLogout.style.display  = 'none';
    if (btnLogin)   btnLogin.style.display   = 'block';
    if (btnRegister)btnRegister.style.display= 'block';
  }

  // 3️⃣ Handle logout (clean + redirect)
  if (btnLogout) {
    btnLogout.addEventListener('click', async (e) => {
      e.preventDefault();
      try {
        // Defensive cleanup on front-end (in case an old token is lingering)
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');

        // Server call to close the session
        window.location.href = '/logout';
      } catch (err) {
        console.error('❌ Logout error:', err);
        window.location.href = '/logout';
      }
    });
  }

  console.log('✅ Navbar Auth - Configuration completed');
});