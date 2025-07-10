import gradio as gr
import os
import json
import string
import secrets
import base64
import hashlib
from cryptography.fernet import Fernet

# === CONFIG ===
DATA_FILE = "vault.json"
MASTER_PASS_HASH_FILE = "master.hash"

# === UTILITIES ===
def generate_key(master_password):
    return base64.urlsafe_b64encode(hashlib.sha256(master_password.encode()).digest())

def load_fernet(master_password):
    key = generate_key(master_password)
    return Fernet(key)

def hash_master_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_master_password(password):
    if not os.path.exists(MASTER_PASS_HASH_FILE):
        with open(MASTER_PASS_HASH_FILE, "w") as f:
            f.write(hash_master_password(password))
        return True, "🔐 Master password set for the first time!"
    stored_hash = open(MASTER_PASS_HASH_FILE).read()
    return hash_master_password(password) == stored_hash, "✅ Master password verified!" if hash_master_password(password) == stored_hash else "❌ Incorrect master password!"

def load_vault():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_vault(vault):
    with open(DATA_FILE, "w") as f:
        json.dump(vault, f, indent=4)

def add_password(master_password, site, username, password_input):
    valid, msg = verify_master_password(master_password)
    if not valid:
        return msg
    fernet = load_fernet(master_password)
    vault = load_vault()
    encrypted = fernet.encrypt(password_input.encode()).decode()
    vault[site] = {"username": username, "password": encrypted}
    save_vault(vault)
    return f"🔐 Password for {site} saved successfully!"

def retrieve_password(master_password, site):
    valid, msg = verify_master_password(master_password)
    if not valid:
        return msg
    vault = load_vault()
    if site not in vault:
        return "❌ No entry found for that site."
    fernet = load_fernet(master_password)
    username = vault[site]["username"]
    decrypted = fernet.decrypt(vault[site]["password"].encode()).decode()
    return f"Username: {username}\nPassword: {decrypted}"

def generate_password(length, use_upper, use_digits, use_symbols):
    chars = string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password, evaluate_strength(password)

def evaluate_strength(password):
    score = 0
    if len(password) >= 12: score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    return ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][score]

# === GRADIO INTERFACE ===

with gr.Blocks(title="🔐 Web Password Manager") as demo:
    gr.Markdown("## 🔐 Secure Password Manager using Gradio + Python")

    with gr.Tab("Add Password"):
        mp1 = gr.Textbox(label="Master Password", type="password")
        site_input = gr.Textbox(label="Site Name")
        user_input = gr.Textbox(label="Username/Email")
        pass_input = gr.Textbox(label="Password (manual or paste)")
        add_btn = gr.Button("Save Password")
        add_output = gr.Textbox(label="Status")
        add_btn.click(add_password, [mp1, site_input, user_input, pass_input], add_output)

    with gr.Tab("Retrieve Password"):
        mp2 = gr.Textbox(label="Master Password", type="password")
        site_query = gr.Textbox(label="Site Name")
        fetch_btn = gr.Button("Get Password")
        fetch_output = gr.Textbox(label="Credentials")
        fetch_btn.click(retrieve_password, [mp2, site_query], fetch_output)

    with gr.Tab("Generate Password"):
        length = gr.Slider(8, 64, step=1, value=16, label="Password Length")
        upper = gr.Checkbox(label="Include Uppercase")
        digits = gr.Checkbox(label="Include Digits")
        symbols = gr.Checkbox(label="Include Symbols")
        gen_btn = gr.Button("Generate")
        gen_pass = gr.Textbox(label="Generated Password")
        strength = gr.Textbox(label="Strength")
        gen_btn.click(generate_password, [length, upper, digits, symbols], [gen_pass, strength])

demo.launch()
