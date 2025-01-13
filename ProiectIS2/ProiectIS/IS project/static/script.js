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
function registerUser() {
    console.log("Funcția registerUser a fost apelată!");
    
    const fullname = document.getElementById("fullname").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const role = document.getElementById("role").value;
    const sex = document.getElementById("sex").value;
    const age = document.getElementById("age").value;
    const weight = document.getElementById("weight").value;
    const height = document.getElementById("height").value;

    if (password !== confirmPassword) {
        alert("Parolele nu se potrivesc!");
        return;
    }

    // Trimite datele către server
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: fullname,
            email: email,
            password: password,
            role: role,
            sex: sex,
            varsta: age,
            greutate: weight,
            inaltime: height,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.message) {
            alert("Cont creat cu succes!");
            window.location.href = '/dashboard-client'; // Schimbă redirect-ul dacă e cazul
        } else if (data.error) {
            alert("Eroare: " + data.error);
        }
    })
    .catch(error => {
        console.error("Eroare:", error);
        alert("A apărut o eroare. Verificați consola.");
    });
}


async function genereazaPlanAlimentar() {
    const obiectiv = document.getElementById('obiectiv-nutritie').value;
    
    fetch('/genereaza_plan_alimentar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ obiectiv: obiectiv })
    })
    .then(response => response.json())
    .then(data => {
        const container = document.getElementById('plan-alimentar-container');
        const caloriiElement = document.getElementById('calorii-zilnice');
        const planDetalii = document.getElementById('plan-detalii');
        
        caloriiElement.textContent = data.calorii_zilnice + ' kcal';
        
        let planHTML = '<ul>';
        for (const [zi, detalii] of Object.entries(data.plan)) {
            planHTML += `<li><strong>${zi}</strong>
                <ul>
                    <li>Mic Dejun: ${detalii.meniu.mic_dejun}</li>
                    <li>Gustare Dimineață: ${detalii.meniu.gustare_dimineața}</li>
                    <li>Prânz: ${detalii.meniu.pranz}</li>
                    <li>Gustare După Prânz: ${detalii.meniu.gustare_dupa_pranz}</li>
                    <li>Cină: ${detalii.meniu.cina}</li>
                </ul>
            </li>`;
        }
        planHTML += '</ul>';
        
        planDetalii.innerHTML = planHTML;
        container.style.display = 'block';
    })
    .catch(error => {
        console.error('Eroare la generarea planului:', error);
        alert('Nu s-a putut genera planul alimentar.');
    });
}

async function schimbaAbonament() {
    const abonamentSelect = document.getElementById('schimba-abonament');
    const abonamentNou = abonamentSelect.value;

    try {
        const response = await fetch('/schimba-abonament', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ abonament: abonamentNou })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('abonament-curent').textContent = data.abonament;
            alert('Abonament actualizat cu succes!');
        } else {
            alert('A apărut o eroare la schimbarea abonamentului.');
        }
    } catch (error) {
        console.error('Eroare la schimbarea abonamentului:', error);
        alert('A apărut o eroare. Te rugăm încearcă din nou.');
    }
}

async function addClient() {
    const email = document.getElementById('client-email').value;

    if (!email) {
        alert("Introduceți un email valid!");
        return;
    }

    try {
        const response = await fetch('/add-client', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_email: email })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Client adăugat cu succes!");
            // Actualizează lista clienților
            const clientList = document.getElementById('client-list');
            const newClient = document.createElement('li');
            newClient.textContent = `${email} - Adăugat recent`;
            clientList.appendChild(newClient);
        } else {
            alert(`Eroare: ${data.error}`);
        }
    } catch (error) {
        console.error("Eroare la adăugarea clientului:", error);
        alert("A apărut o eroare. Verificați consola.");
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

async function displayActivityHistory() {
    const activityList = document.getElementById('activity-list');

    // Datele activităților ar putea fi stocate într-un array în scripturi.js
    const activities = [
        { type: 'Antrenament personal', date: '10.12.2025', trainer: 'Andrei' },
        { type: 'Clasă de grup: HIIT', date: '15.12.2025', trainer: null },
        { type: 'Consultație nutrițională', date: '20.12.2025', trainer: null }
    ];

    activities.forEach(activity => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>${activity.type}</strong> ${activity.trainer ? `cu ${activity.trainer}` : ''} pe <em>${activity.date}</em>
        `;
        activityList.appendChild(listItem);
    });
}

// Apelează funcția la încărcarea paginii
window.addEventListener('DOMContentLoaded', displayActivityHistory);