from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# In-memory store for passwords
passwords = []

def generate_random_password(length=12):
    charset = string.ascii_letters + string.digits + "!@#$%^&*()_+~"
    return ''.join(random.choice(charset) for _ in range(length))

@app.route('/generate', methods=['GET'])
def generate_passwords():
    global passwords
    passwords = [generate_random_password() for _ in range(3)]
    return jsonify({"suggested_passwords": passwords})

@app.route('/api/add', methods=['POST'])
def add_password():
    global passwords
    data = request.get_json()
    custom_password = data.get('password', '').strip()

    if custom_password:
        passwords.insert(0, custom_password)
        return jsonify({"message": "Password added successfully", "passwords": passwords}), 201
    else:
        return jsonify({"error": "Password cannot be empty"}), 400

@app.route('/api/passwords', methods=['GET'])
def get_passwords():
    return jsonify({"passwords": passwords})

if __name__ == '__main__':
    app.run(debug=True)
