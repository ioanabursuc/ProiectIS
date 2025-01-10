from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

app = Flask(__name__, template_folder='frontend')


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
        
        
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup-login')
def signup_login():
    return render_template('signup-login.html')



# Ruta pentru logare
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verifică utilizatorul
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    if user_data and check_password_hash(user_data['password'], password):
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

if __name__ == '__main__':
    app.run(debug=True)
