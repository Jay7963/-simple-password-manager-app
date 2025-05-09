import json
import os
import hashlib
from cryptography.fernet import Fernet


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def set_master_password(pw):
    hashed = hash_password(pw)
    with open("master.hash", "w") as f:
        f.write(hashed)

def check_master_password(entered):
    if not os.path.exists("master.hash"):
        return False
    hashed_entered = hash_password(entered)
    with open("master.hash", "r") as f:
        saved_hash = f.read()
    return hashed_entered == saved_hash

def master_password_exists():
    return os.path.exists("master.hash")

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("key.key"):
        generate_key()
    return open("key.key", "rb").read()


def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

def save_password(site, username, password, key):
    data = {}

    if os.path.exists("data.json"):
        with open("data.json", "rb") as file:
            encrypted = file.read()
            try:
                decrypted = decrypt_data(encrypted, key)
                data = json.loads(decrypted)
            except:
                return False  

    data[site] = {"username": username, "password": password}
    encrypted = encrypt_data(json.dumps(data), key)

    with open("data.json", "wb") as file:
        file.write(encrypted)

    return True


def load_passwords(key):
    if not os.path.exists("data.json"):
        return {}

    with open("data.json", "rb") as file:
        encrypted = file.read()
        try:
            decrypted = decrypt_data(encrypted, key)
            data = json.loads(decrypted)
            return data
        except:
            return None  
