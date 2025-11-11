console.log('🔐 Login script - Initialization...');

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔄 DOM loaded for login.js');

    const loginForm = document.getElementById('login-form');

    if (!loginForm) {
        console.log('❌ Login form not found');
        return;
    }

    console.log('✅ Login form found');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('📤 Sending login form...');

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

            console.log('📡 Response received, status:', response.status);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('❌ API Error:', errorData);
                throw new Error(errorData.detail || 'Invalid credentials');
            }

            const data = await response.json();
            console.log('📦 Data:', data);

            console.log('📦 Full response:', data);

            if (data.access_token || data.tokens?.access) {
                console.log('✅ Login successful!');
                console.log('💾 Saving tokens...');

                // Handle both possible response formats
                const accessToken = data.access_token || data.tokens?.access;
                const refreshToken = data.refresh_token || data.tokens?.refresh;

                localStorage.setItem('access_token', accessToken);
                localStorage.setItem('refresh_token', refreshToken);
                localStorage.setItem('user', JSON.stringify(data.user));

                console.log('✅ Token saved:', accessToken.substring(0, 20) + '...');
                console.log('🔄 Redirecting to /odds...');

                // Wait 100ms to ensure localStorage is written
                setTimeout(() => {
                    window.location.replace('/odds');
                }, 100);

            } else {
                throw new Error('Missing tokens in response');
            }

        } catch (error) {
            console.error('❌ Login error:', error.message);
            alert('Error: ' + error.message);
        }
    });
});