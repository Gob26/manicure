document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const cityInput = document.getElementById('city-input').value;
    
    const response = await fetch('/api/v1/users/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: 'test_user',
            email: 'test@example.com',
            password: 'secure_password',
            city_name: cityInput,
            role: 'user'
        })
    });

    const result = await response.json();
    console.log(result);
});
