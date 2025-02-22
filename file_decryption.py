import os
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64
import winreg

# Lấy đường dẫn thực thi của chương trình
def get_application_path():
    return os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))

# Thiết lập thư mục lưu trữ
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

# Kiểm tra quyền admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Tạo registry menu chuột phải
def create_registry_entries():
    if not is_admin():
        messagebox.showerror("Lỗi", "Cần quyền admin để tạo registry entries!")
        return False
    
    decryption_exe = os.path.join(get_application_path(), "file_decryption.exe")
    
    try:
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\DecryptFile") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Decrypt")
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, decryption_exe)
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "*\\shell\\DecryptFile\\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{decryption_exe}" decrypt "%1"')
        
        messagebox.showinfo("Thành công", "Đã đăng ký Encrypt/Decrypt vào menu chuột phải!")
        return True
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đăng ký registry: {str(e)}")
        return False

# Mã hóa file
def encrypt_file(file_path):
    folders = setup_folders()
    password = simpledialog.askstring("Mật khẩu", "Nhập mật khẩu để mã hóa:", show='*')
    if not password:
        return
    
    key = SHA256.new(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM)
    
    with open(file_path, "rb") as f:
        plaintext = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    encrypted_file = os.path.join(folders['encrypted'], os.path.basename(file_path) + ".enc")
    with open(encrypted_file, "wb") as f:
        f.write(cipher.nonce + tag + ciphertext)
    
    messagebox.showinfo("Thành công", f"File đã mã hóa và lưu tại {encrypted_file}")

# Giải mã file
def decrypt_file(file_path):
    folders = setup_folders()
    password = simpledialog.askstring("Mật khẩu", "Nhập mật khẩu để giải mã:", show='*')
    if not password:
        return
    
    key = SHA256.new(password.encode()).digest()
    
    with open(file_path, "rb") as f:
        nonce, tag, ciphertext = f.read(16), f.read(16), f.read()
    
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        decrypted_file = os.path.join(folders['decrypted'], os.path.basename(file_path).replace(".enc", ""))
        with open(decrypted_file, "wb") as f:
            f.write(plaintext)
        messagebox.showinfo("Thành công", f"File đã giải mã và lưu tại {decrypted_file}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể giải mã file: {str(e)}")

# Chạy chương trình
def main():
    if len(sys.argv) == 1:
        create_registry_entries()
        return
    
    if len(sys.argv) < 3:
        messagebox.showerror("Lỗi", "Không có đường dẫn file được cung cấp.")
        return
    
    action = sys.argv[1]
    file_path = sys.argv[2]
    
    if action == "encrypt":
        encrypt_file(file_path)
    elif action == "decrypt":
        decrypt_file(file_path)
    else:
        messagebox.showerror("Lỗi", "Thao tác không hợp lệ!")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    main()
