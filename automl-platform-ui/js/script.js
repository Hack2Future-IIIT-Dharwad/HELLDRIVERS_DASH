document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            console.log('Register form submitted', { username, password });

            try {
                const response = await fetch('https://api.example.com/register', { // Replace with your API URL
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                console.log('Response received', response);

                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }

                const data = await response.json();
                console.log('Response data', data);
                alert('Registration successful!');
                // Redirect to login page or dashboard
                window.location.href = 'login.html';
            } catch (error) {
                console.error('There has been a problem with your fetch operation:', error);
                alert('Registration failed. Please try again.');
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            console.log('Login form submitted', { username, password });

            try {
                const response = await fetch('https://api.example.com/login', { // Replace with your API URL
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                console.log('Response received', response);

                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }

                const data = await response.json();
                console.log('Response data', data);

                // Store token or user info if needed, e.g. localStorage.setItem('user', JSON.stringify(data.user));

                alert('Login successful!');
                // Redirect to dashboard
                window.location.href = 'dashboard.html'; // Change this to your actual dashboard page
            } catch (error) {
                console.error('There has been a problem with your fetch operation:', error);
                alert('Login failed. Please try again.');
            }
        });
    }
});
