from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

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
    cursor.execute("SELECT username, email, role FROM users WHERE id = %s", (current_user_id,))
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
