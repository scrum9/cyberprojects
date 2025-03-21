import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet, InvalidToken

# Generate and store a key
def generate_key():
    return Fernet.generate_key()

# Encryption function
def encrypt_message():
    message = entry_plain.get()
    if not message:
        messagebox.showwarning("Input Needed", "Please enter a message to encrypt.")
        return

    try:
        key = key_var.get().encode()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(message.encode())
        result_var.set(encrypted.decode())
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")

# Decryption function
def decrypt_message():
    ciphertext = entry_plain.get()
    if not ciphertext:
        messagebox.showwarning("Input Needed", "Please enter encrypted text to decrypt.")
        return

    try:
        key = key_var.get().encode()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(ciphertext.encode())
        result_var.set(decrypted.decode())
    except InvalidToken:
        messagebox.showerror("Invalid Key or Data", "Decryption failed. Invalid key or ciphertext.")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

# Copy generated key to entry field
def generate_and_set_key():
    new_key = generate_key().decode()
    key_var.set(new_key)
    messagebox.showinfo("Key Generated", "A new AES-256 key has been generated.")

# GUI Setup
root = tk.Tk()
root.title("AES-256 Encryption Demo")
root.geometry("500x300")
root.resizable(False, False)

# Input Message
ttk.Label(root, text="Enter Message / Encrypted Text:").pack(pady=5)
entry_plain = ttk.Entry(root, width=60)
entry_plain.pack()

# Key Input
ttk.Label(root, text="Enter AES-256 Key (or generate one):").pack(pady=5)
key_var = tk.StringVar()
entry_key = ttk.Entry(root, textvariable=key_var, width=60)
entry_key.pack()

# Generate Key Button
ttk.Button(root, text="Generate Key", command=generate_and_set_key).pack(pady=5)

# Action Buttons
frame_btns = ttk.Frame(root)
frame_btns.pack(pady=10)
ttk.Button(frame_btns, text="Encrypt", command=encrypt_message).grid(row=0, column=0, padx=10)
ttk.Button(frame_btns, text="Decrypt", command=decrypt_message).grid(row=0, column=1, padx=10)

# Result Field
ttk.Label(root, text="Result:").pack(pady=5)
result_var = tk.StringVar()
entry_result = ttk.Entry(root, textvariable=result_var, width=60, state='readonly')
entry_result.pack()

# Run GUI
root.mainloop()
