# 🔐 Secure Password Manager (Gradio + Python)

A simple and secure **local password manager** built using **Python**, **Gradio**, and the **cryptography** library.

This app allows you to:
- Add and store encrypted passwords
- Retrieve stored passwords securely
- Generate strong, random passwords with strength rating

---

## 🚀 Features

### ✅ Master Password Protection
- Your master password is securely **hashed** and stored the first time.
- It’s used to encrypt/decrypt all other saved passwords.

### 🔒 Encrypted Password Vault
- All your credentials are encrypted using **AES (Fernet)**.
- They are stored in a local JSON file (`vault.json`), never in plain text.

### 🔐 Add Password
- Input your master password, site name, username, and password.
- The password is encrypted and stored securely.

### 🔎 Retrieve Password
- Input your master password and site name.
- If verified, it decrypts and displays the stored username and password.

### 🛠️ Generate Strong Passwords
- Customize password length
- Add uppercase letters, numbers, and symbols
- Get a strength rating from **Very Weak** to **Very Strong**

---

## 📁 File Structure

| File              | Description |
|-------------------|-------------|
| `password_manager.py` | Main application logic using Gradio |
| `vault.json`      | Stores encrypted passwords |
| `master.hash`     | Stores hashed master password for verification |

---

## 🛠️ Requirements

- Python 3.7+
- Install required packages:

bash
pip install gradio cryptography
