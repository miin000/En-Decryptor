import os
import sys
import subprocess
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_application_path():
    return os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

def setup_folders():
    base_path = get_application_path()
    folders = {
        'encrypted': os.path.join(base_path, "Encrypted"),
        'decrypted': os.path.join(base_path, "Decrypted"),
        'key': os.path.join(base_path, "Key")
    }
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    return folders

def create_registry_entries():
    if not is_admin():
        messagebox.showerror("Lỗi", "Cần quyền admin để tạo registry entries!")
        return False
    exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0])
    try:
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\EncryptFile") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Encrypt")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, exe_path)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\EncryptFile\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{exe_path}" encrypt "%1"')
        return True
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đăng ký registry: {str(e)}")
        return False

def derive_key_from_password(password):
    hasher = SHA256.new(password.encode())
    return hasher.digest()

def encrypt_file(file_path):
    setup_folders()
    password = simpledialog.askstring("Nhập mật khẩu", "Nhập mật khẩu để mã hóa:", show='*')
    if not password:
        return
    try:
        key = derive_key_from_password(password)
        cipher = AES.new(key, AES.MODE_EAX)
        with open(file_path, 'rb') as f:
            data = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(data)
        encrypted_file = os.path.join(setup_folders()['encrypted'], os.path.basename(file_path) + ".enc")
        with open(encrypted_file, 'wb') as f:
            f.write(cipher.nonce)
            f.write(tag)
            f.write(ciphertext)
        messagebox.showinfo("Thành công", f"File đã được mã hóa và lưu tại: {encrypted_file}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi mã hóa file: {str(e)}")

def decrypt_file(file_path):
    setup_folders()
    key_file = filedialog.askopenfilename(title="Chọn Key File", filetypes=[("Key Files", "*.key")], initialdir=setup_folders()['key'])
    if not key_file:
        messagebox.showerror("Lỗi", "Không có key file nào được chọn.")
        return
    try:
        with open(key_file, 'rb') as f:
            key = f.read()
        with open(file_path, 'rb') as f:
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        decrypted_file = os.path.join(setup_folders()['decrypted'], os.path.basename(file_path).replace(".enc", ""))
        with open(decrypted_file, 'wb') as f:
            f.write(plaintext)
        messagebox.showinfo("Thành công", f"File đã được giải mã và lưu tại: {decrypted_file}")
    except ValueError:
        messagebox.showerror("Lỗi", "Giải mã thất bại: Key không hợp lệ hoặc file bị hỏng.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

def main():
    if len(sys.argv) == 1:
        create_registry_entries()
        return
    if len(sys.argv) < 3:
        messagebox.showerror("Lỗi", "Không đủ tham số")
        sys.exit(1)
    action = sys.argv[1].lower()
    file_path = sys.argv[2]
    if not os.path.exists(file_path):
        messagebox.showerror("Lỗi", f"File không tồn tại: {file_path}")
        sys.exit(1)
    if action == "encrypt":
        encrypt_file(file_path)
    elif action == "decrypt":
        decrypt_file(file_path)
    else:
        messagebox.showerror("Lỗi", f"Hành động không hợp lệ: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()