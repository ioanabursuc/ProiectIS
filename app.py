from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection
from abc import ABC, abstractmethod
import random

app = Flask(__name__, template_folder='frontend')
app.secret_key = 'cheie_secretă_sigură'  # Setează o cheie secretă puternică pentru sesiuni


# Clase pentru roluri
class ClientRole:
    def __init__(self, user):
        self.user = user

    def get_dashboard(self):
        return "dashboard-client.html"

class TrainerRole:
    def __init__(self, user):
        self.user = user

    def get_dashboard(self):
        return "dashboard-trainer.html"

class User:
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    def get_role(self):
        if self.role == "Client":
            return ClientRole(self)
        elif self.role == "Trainer":
            return TrainerRole(self)
        else:
            raise ValueError("Rol necunoscut!")


# Interfață pentru generarea planurilor alimentare
class GeneratorPlanAlimentar(ABC):
    @abstractmethod
    def genereaza_plan(self, sex, varsta, greutate, inaltime):
        pass

# Strategii concrete pentru generarea planurilor
class GeneratorPlanSlabire(GeneratorPlanAlimentar):
    def genereaza_plan(self, sex, varsta, greutate, inaltime):
        # Calculează necesarul caloric bazal (Harris-Benedict)
        if sex == 'masculin':
            tmb = 88.362 + (13.397 * greutate) + (4.799 * inaltime) - (5.677 * varsta)
        else:
            tmb = 447.593 + (9.247 * greutate) + (3.098 * inaltime) - (4.330 * varsta)

        # Ajustează caloriile pentru deficit caloric (80% din TMB)
        calorii_zilnice = tmb * 0.8

        # Generează meniul pentru plan de slăbire
        meniu_mic_dejun = [
            "Omletă din 2 ouă albe cu spanac și roșii",
            "Ovăz cu iaurt grecesc și fructe de pădure",
            "Smoothie verde cu proteină"
        ]
        meniu_gustare_dimineata = [
            "Măr cu migdale",
            "Batoane proteice mici",
            "Stick-uri de morcov cu hummus"
        ]
        meniu_pranz = [
            "Salată cu piept de pui la grătar",
            "File de pește cu legume la aburi",
            "Quinoa cu ton și legume"
        ]
        meniu_gustare_dupa_pranz = [
            "Iaurt grecesc cu nucă",
            "Shake proteic cu lapte vegetal",
            "Ou fiert"
        ]
        meniu_cina = [
            "Somon la cuptor cu sparangh",
            "Tocăniță de legume cu tofu",
            "Supă cremă de legume"
        ]

        # Generează planul pe o lună (30 de zile)
        plan_lunar = {}
        for zi in range(1, 31):
            plan_zilnic = {
                'mic_dejun': random.choice(meniu_mic_dejun),
                'gustare_dimineata': random.choice(meniu_gustare_dimineata),
                'pranz': random.choice(meniu_pranz),
                'gustare_dupa_pranz': random.choice(meniu_gustare_dupa_pranz),
                'cina': random.choice(meniu_cina)
            }
            plan_lunar[f'Ziua {zi}'] = {
                'meniu': plan_zilnic,
                'calorii_estimate': round(calorii_zilnice)
            }

        return plan_lunar

class GeneratorPlanMasaMusculara(GeneratorPlanAlimentar):
    def genereaza_plan(self, sex, varsta, greutate, inaltime):
        # Calculează necesarul caloric bazal (Harris-Benedict)
        if sex == 'masculin':
            tmb = 88.362 + (13.397 * greutate) + (4.799 * inaltime) - (5.677 * varsta)
        else:
            tmb = 447.593 + (9.247 * greutate) + (3.098 * inaltime) - (4.330 * varsta)

        # Ajustează caloriile pentru surplus caloric ușor (120% din TMB)
        calorii_zilnice = tmb * 1.2

        # Generează meniul pentru plan de masă musculară
        meniu_mic_dejun = [
            "Omletă din 4 ouă cu brânză și șuncă",
            "Clătite proteice cu unt de arahide",
            "Porridge cu proteine și banane"
        ]
        meniu_gustare_dimineata = [
            "Shake proteic cu fulgi de ovăz",
            "Brânză cottage cu nuci",
            "Wrap cu ton și avocado"
        ]
        meniu_pranz = [
            "Piept de pui cu orez brun și legume",
            "Pastă integrală cu șuncă și brânză",
            "File de vită cu cartofi dulci"
        ]
        meniu_gustare_dupa_pranz = [
            "Baton proteic",
            "Smoothie cu proteină și fructe",
            "Sardele pe pâine integrală"
        ]
        meniu_cina = [
            "Cotlet de porc cu legume la grătar",
            "Curry de pui cu orez",
            "Paste integrale cu sos de ton"
        ]

        # Generează planul pe o lună (30 de zile)
        plan_lunar = {}
        for zi in range(1, 31):
            plan_zilnic = {
                'mic_dejun': random.choice(meniu_mic_dejun),
                'gustare_dimineata': random.choice(meniu_gustare_dimineata),
                'pranz': random.choice(meniu_pranz),
                'gustare_dupa_pranz': random.choice(meniu_gustare_dupa_pranz),
                'cina': random.choice(meniu_cina)
            }
            plan_lunar[f'Ziua {zi}'] = {
                'meniu': plan_zilnic,
                'calorii_estimate': round(calorii_zilnice)
            }

        return plan_lunar

class GeneratorPlanIngrasare(GeneratorPlanAlimentar):
    def genereaza_plan(self, sex, varsta, greutate, inaltime):
        # Calculează necesarul caloric bazal (Harris-Benedict)
        if sex == 'masculin':
            tmb = 88.362 + (13.397 * greutate) + (4.799 * inaltime) - (5.677 * varsta)
        else:
            tmb = 447.593 + (9.247 * greutate) + (3.098 * inaltime) - (4.330 * varsta)

        # Ajustează caloriile pentru surplus caloric mai mare (150% din TMB)
        calorii_zilnice = tmb * 1.5

        # Generează meniul pentru plan de îngrășare
        meniu_mic_dejun = [
            "Clătite cu brânză și miere",
            "Ouă cu șuncă, brânză și pâine prăjită",
            "Smoothie gras cu unt de arahide"
        ]
        meniu_gustare_dimineata = [
            "Banană cu unt de migdale",
            "Shake cu lapte integral și proteine",
            "Plăcintă cu brânză"
        ]
        meniu_pranz = [
            "Mămăligă cu brânză și jumări",
            "Paste carbonara",
            "Tocăniță cu carne și mămăligă"
        ]
        meniu_gustare_dupa_pranz = [
            "Pizza mică",
            "Brioșă cu ciocolată",
            "Plăcintă cu mere"
        ]
        meniu_cina = [
            "Pulpe de pui cu cartofi prăjiți",
            "Hamburger cu cartofi",
            "Lasagna cu multă brânză"
        ]

        # Generează planul pe o lună (30 de zile)
        plan_lunar = {}
        for zi in range(1, 31):
            plan_zilnic = {
                'mic_dejun': random.choice(meniu_mic_dejun),
                'gustare_dimineata': random.choice(meniu_gustare_dimineata),
                'pranz': random.choice(meniu_pranz),
                'gustare_dupa_pranz': random.choice(meniu_gustare_dupa_pranz),
                'cina': random.choice(meniu_cina)
            }
            plan_lunar[f'Ziua {zi}'] = {
                'meniu': plan_zilnic,
                'calorii_estimate': round(calorii_zilnice)
            }

        return plan_lunar

class GeneratorPlanMentinere(GeneratorPlanAlimentar):
    def genereaza_plan(self, sex, varsta, greutate, inaltime):
        # Calculează necesarul caloric bazal (Harris-Benedict)
        if sex == 'masculin':
            tmb = 88.362 + (13.397 * greutate) + (4.799 * inaltime) - (5.677 * varsta)
        else:
            tmb = 447.593 + (9.247 * greutate) + (3.098 * inaltime) - (4.330 * varsta)

        # Ajustează caloriile pentru menținere (100% din TMB)
        calorii_zilnice = tmb

        # Generează meniul pentru plan de menținere
        meniu_mic_dejun = [
            "Ouă scraminate cu toast integral",
            "Iaurt grecesc cu cereale și fructe",
            "Smoothie echilibrat"
        ]
        meniu_gustare_dimineata = [
            "Fructe proaspete",
            "Nuci și semințe",
            "Brânză cottage"
        ]
        meniu_pranz = [
            "Salată cu pui la grătar",
            "Pește cu garnitură de legume",
            "Quinoa cu legume și proteină"
        ]
        meniu_gustare_dupa_pranz = [
            "Fruct cu brânză",
            "Shake proteic ușor",
            "Biscuiți integrali"
        ]
        meniu_cina = [
            "Somon cu legume",
            "Tocăniță de legume cu carne slabă",
            "Supă cremă și file de pește"
        ]

        # Generează planul pe o lună (30 de zile)
        plan_lunar = {}
        for zi in range(1, 31):
            plan_zilnic = {
                'mic_dejun': random.choice(meniu_mic_dejun),
                'gustare_dimineata': random.choice(meniu_gustare_dimineata),
                'pranz': random.choice(meniu_pranz),
                'gustare_dupa_pranz': random.choice(meniu_gustare_dupa_pranz),
                'cina': random.choice(meniu_cina)
            }
            plan_lunar[f'Ziua {zi}'] = {
                'meniu': plan_zilnic,
                'calorii_estimate': round(calorii_zilnice)
            }

        return plan_lunar

# Context care utilizează strategia
class ContextGeneratorPlanAlimentar:
    def __init__(self, generator: GeneratorPlanAlimentar):
        self._generator = generator
    
    def genereaza_plan(self, sex, varsta, greutate, inaltime):
        return self._generator.genereaza_plan(sex, varsta, greutate, inaltime)

# Funcție de generare a planului alimentar
def genereaza_plan_alimentar(obiectiv, sex, varsta, greutate, inaltime):
    if obiectiv == 'slabire':
        generator = GeneratorPlanSlabire()
    elif obiectiv == 'masa_musculara':
        generator = GeneratorPlanMasaMusculara()
    elif obiectiv == 'ingrasare':
        generator = GeneratorPlanIngrasare()
    elif obiectiv == 'mentinere':
        generator = GeneratorPlanMentinere()
    else:
        raise ValueError('Obiectiv invalid')
    
    context = ContextGeneratorPlanAlimentar(generator)
    return context.genereaza_plan(sex, varsta, greutate, inaltime)

# Rute
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup-login')
def signup_login():
    return render_template('signup-login.html')


@app.route('/dashboard-client.html')
def dashboard_client():
    if 'user_id' not in session:
        return redirect('/signup-login')  # Redirecționează utilizatorii neconectați

    current_user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, email, role, sex, varsta, greutate, inaltime FROM users WHERE id = %s", (current_user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_data:
        if user_data['role'] != "Client":
            return "Acces interzis! Acest dashboard este pentru clienți.", 403

        return render_template('dashboard-client.html', user=user_data)
    else:
        return "Utilizatorul nu a fost găsit!", 404


@app.route('/dashboard-trainer.html')
def dashboard_trainer():
    if 'user_id' not in session:
        return redirect('/signup-login')  # Redirecționează utilizatorii neconectați

    current_user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, email, role FROM users WHERE id = %s", (current_user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_data:
        if user_data['role'] != "Trainer":
            return "Acces interzis! Acest dashboard este pentru antrenori.", 403

        return render_template('dashboard-trainer.html', user=user_data)
    else:
        return "Utilizatorul nu a fost găsit!", 404


@app.route('/genereaza_plan_alimentar', methods=['POST'])
def genereaza_plan_alimentar_ruta():
    if 'user_id' not in session:
        return jsonify({"error": "Utilizator neautentificat!"}), 401

    data = request.json
    obiectiv = data.get('obiectiv')
    
    # Preluare date utilizator din baza de date
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT sex, varsta, greutate, inaltime FROM users WHERE id = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user_data:
        return jsonify({"error": "Date utilizator indisponibile"}), 404

    plan = genereaza_plan_alimentar(
        obiectiv, 
        user_data['sex'], 
        user_data['varsta'], 
        user_data['greutate'], 
        user_data['inaltime']
    )
    
    return jsonify(plan)

# Ruta pentru logare
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    if user_data and check_password_hash(user_data['password'], password):
        # Setează sesiunea utilizatorului
        session['user_id'] = user_data['id']

        user = User(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            role=user_data['role']
        )
        role = user.get_role()
        dashboard = role.get_dashboard()

        return jsonify({
            "message": "Logare reușită!",
            "dashboard": dashboard
        })
    else:
        return jsonify({"error": "Email sau parolă incorectă!"}), 401


# Ruta pentru delogare
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Șterge ID-ul utilizatorului din sesiune
    return redirect('/signup-login')


# Ruta pentru înregistrare
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    role = data['role']

    if role not in ["Client", "Trainer"]:
        return jsonify({"error": "Rol invalid!"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, password, role)
        )
        conn.commit()
        return jsonify({"message": "Cont creat cu succes!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/schimba-abonament', methods=['POST'])
def schimba_abonament():
    if 'user_id' not in session:
        return jsonify({"error": "Utilizator neautentificat!"}), 401

    data = request.json
    abonament_nou = data['abonament']

    # Actualizează abonamentul utilizatorului în baza de date
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET abonament = %s WHERE id = %s", (abonament_nou, session['user_id']))
    conn.commit()

    # Obține detaliile actualizate ale utilizatorului
    cursor.execute("SELECT abonament FROM users WHERE id = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify({"abonament": user_data['abonament']})


# Ruta pentru adăugarea unui client (pentru trainer)
@app.route('/add-client', methods=['POST'])
def add_client():
    if 'user_id' not in session:
        return jsonify({"error": "Utilizator neautentificat!"}), 401

    data = request.json
    client_email = data['client_email']
    current_user_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s AND role = 'Client'", (client_email,))
    client = cursor.fetchone()

    if client:
        cursor.execute("INSERT INTO trainer_clients (trainer_id, client_id) VALUES (%s, %s)", (current_user_id, client['id']))
        conn.commit()
        return jsonify({"message": "Client adăugat cu succes!"})
    else:
        return jsonify({"error": "Clientul nu a fost găsit!"}), 404


# Ruta pentru crearea unui plan de antrenament (pentru trainer)
@app.route('/create-plan', methods=['POST'])
def create_plan():
    if 'user_id' not in session:
        return jsonify({"error": "Utilizator neautentificat!"}), 401

    data = request.json
    client_id = data['client_id']
    plan_details = data['plan_details']
    current_user_id = session['user_id']

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO training_plans (trainer_id, client_id, plan_details) VALUES (%s, %s, %s)", (current_user_id, client_id, plan_details))
    conn.commit()
    return jsonify({"message": "Plan creat cu succes!"})


if __name__ == '__main__':
    app.run(debug=True)