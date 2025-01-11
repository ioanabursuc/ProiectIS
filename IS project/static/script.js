/*signup-login*/
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const switchToSignup = document.getElementById('switch-to-signup');
const switchToLogin = document.getElementById('switch-to-login');

loginBtn.addEventListener('click', () => {
    loginForm.classList.add('active');
    signupForm.classList.remove('active');
});

signupBtn.addEventListener('click', () => {
    signupForm.classList.add('active');
    loginForm.classList.remove('active');
});

switchToSignup.addEventListener('click', (e) => {
    e.preventDefault();
    signupForm.classList.add('active');
    loginForm.classList.remove('active');
});

switchToLogin.addEventListener('click', (e) => {
    e.preventDefault();
    loginForm.classList.add('active');
    signupForm.classList.remove('active');
});

// Logare utilizator
async function loginUser() {
    const email = document.querySelector('#login-form input[placeholder="Adresa de email"]').value;
    const password = document.querySelector('#login-form input[placeholder="Parola"]').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
        window.location.href = data.dashboard; // Redirectare la dashboard-ul utilizatorului
    } else {
        alert(data.error);
    }
}

// Înregistrare utilizator
async function registerUser() {
    const username = document.querySelector('#signup-form input[placeholder="Nume complet"]').value;
    const email = document.querySelector('#signup-form input[placeholder="Adresa de email"]').value;
    const password = document.querySelector('#signup-form input[placeholder="Parola"]').value;
    const confirmPassword = document.querySelector('#signup-form input[placeholder="Confirmă parola"]').value;
    const role=document.querySelector('#signup-form input[placeholder="Client/Trainer"]').value;

    if (password !== confirmPassword) {
        alert('Parolele nu se potrivesc!');
        return;
    }

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, role }),
    });

    const data = await response.json();
    if (response.ok) {
        alert(data.message);
        window.location.href = '/'; // Redirecționare la pagina principală
    } else {
        alert(data.error);
    }
}

async function addClient() {
    const clientEmail = prompt("Introduceți emailul clientului:");
    if (!clientEmail) return;

    const response = await fetch('/add-client', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_email: clientEmail })
    });

    const data = await response.json();
    if (response.ok) {
        alert("Client adăugat cu succes!");
        window.location.reload();
    } else {
        alert(data.error);
    }
}

async function createTrainingPlan() {
    const clientId = prompt("Introduceți ID-ul clientului:");
    const planDetails = prompt("Introduceți detaliile planului:");

    if (!clientId || !planDetails) return;

    const response = await fetch('/create-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: clientId, plan_details: planDetails })
    });

    const data = await response.json();
    if (response.ok) {
        alert("Plan de antrenament creat!");
        window.location.reload();
    } else {
        alert(data.error);
    }
}
