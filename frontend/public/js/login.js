console.log('🔐 Login script - Initialisation...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔄 DOM chargé pour login.js');

    const loginForm = document.getElementById('login-form');

    if (!loginForm) {
        console.log('❌ Formulaire de connexion non trouvé');
        return;
    }

    console.log('✅ Formulaire de login trouvé');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('📤 Envoi du formulaire de connexion...');

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value;

        console.log('👤 Username:', username);

        try {
            const response = await fetch('http://localhost:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });

            console.log('📡 Réponse reçue, status:', response.status);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('❌ Erreur API:', errorData);
                throw new Error(errorData.detail || 'Identifiants invalides');
            }

            const data = await response.json();
            console.log('📦 Data:', data);

            console.log('📦 Réponse complète:', data);

            if (data.access_token || data.tokens?.access) {
                console.log('✅ Connexion réussie !');
                console.log('💾 Sauvegarde des tokens...');

                // Gérer les 2 formats possibles de réponse
                const accessToken = data.access_token || data.tokens?.access;
                const refreshToken = data.refresh_token || data.tokens?.refresh;

                localStorage.setItem('access_token', accessToken);
                localStorage.setItem('refresh_token', refreshToken);
                localStorage.setItem('user', JSON.stringify(data.user));

                console.log('✅ Token sauvegardé:', accessToken.substring(0, 20) + '...');
                console.log('🔄 Redirection vers /odds...');

                // Attendre 100ms pour être sûr que localStorage est bien écrit
                setTimeout(() => {
                    window.location.replace('/odds');
                }, 100);

            } else {
                throw new Error('Tokens manquants dans la réponse');
            }

        } catch (error) {
            console.error('❌ Erreur de connexion:', error.message);
            alert('Erreur : ' + error.message);
        }
    });
});