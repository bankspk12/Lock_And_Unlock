import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password):
    # สร้าง Fernet key โดยใช้ hashlib และ base64
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_file(key, file_path):
    with open(file_path, "rb") as file:
        data = file.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(key, file_path):
    with open(file_path, "rb") as file:
        data = file.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data)

    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("ไฟล์ข้อความ", "*.txt"), ("ไฟล์ Excel", "*.xlsx")])
    return file_path

def show_status_message(message):
    status_label.config(text=message)

def decrypt_and_save():
    window.withdraw()  # ซ่อนหน้าต่างหลักไว้

    password_window = tk.Toplevel()  # สร้างหน้าต่างใหม่สำหรับกรอกรหัสผ่าน
    password_window.title("กรอกรหัสผ่าน")
    password_window.geometry("300x150")  # ปรับขนาดของหน้าต่างใหม่

    entry_password = tk.Entry(password_window, show="*")  # Entry สำหรับรหัสผ่าน
    entry_password.pack(pady=10)

    def on_enter_key(event):
        decrypt_file_with_password()

    entry_password.bind("<Return>", on_enter_key)

    def decrypt_file_with_password():
        password = entry_password.get()  # รับรหัสผ่านจาก Entry
        key = generate_key(password)
        file_path = select_file()
        decrypt_file(key, file_path)
        show_status_message("ไฟล์ถูกถอดรหัสเรียบร้อยแล้ว")

        password_window.destroy()  # ปิดหน้าต่างกรอกรหัสผ่าน
        window.deiconify()  # แสดงหน้าต่างหลักอีกครั้ง

    decrypt_button = tk.Button(password_window, text="ถอดรหัส", command=decrypt_file_with_password, font=("Helvetica", 14))
    decrypt_button.pack()

    # สร้างปุ่ม "ย้อนกลับ" และกำหนดให้เมื่อกดจะปิดหน้าต่างกรอกรหัสผ่านและแสดงหน้าต่างหลักอีกครั้ง
    back_button = tk.Button(password_window, text="ย้อนกลับ", command=lambda: (password_window.destroy(), window.deiconify()), font=("Helvetica", 14))
    back_button.pack()

    window.withdraw()  # ซ่อนหน้าต่างหลักไว้

def encrypt_and_save():
    password_window = tk.Toplevel()  # สร้างหน้าต่างใหม่สำหรับกรอกรหัสผ่าน
    password_window.title("กรอกรหัสผ่าน")
    password_window.geometry("300x150")  # ปรับขนาดของหน้าต่างใหม่

    entry_password = tk.Entry(password_window, show="*")  # Entry สำหรับรหัสผ่าน
    entry_password.pack(pady=10)

    def on_enter_key(event):
        encrypt_file_with_password()

    entry_password.bind("<Return>", on_enter_key)

    def encrypt_file_with_password():
        password = entry_password.get()  # รับรหัสผ่านจาก Entry
        key = generate_key(password)
        file_path = select_file()
        encrypt_file(key, file_path)
        show_status_message("ไฟล์ถูกเข้ารหัสเรียบร้อยแล้ว")

        password_window.destroy()  # ปิดหน้าต่างกรอกรหัสผ่าน
        window.deiconify()  # แสดงหน้าต่างหลักอีกครั้ง

    encrypt_button = tk.Button(password_window, text="เข้ารหัส", command=encrypt_file_with_password, font=("Helvetica", 14))
    encrypt_button.pack()

    # สร้างปุ่ม "ย้อนกลับ" และกำหนดให้เมื่อกดจะปิดหน้าต่างกรอกรหัสผ่านและแสดงหน้าต่างหลักอีกครั้ง
    back_button = tk.Button(password_window, text="ย้อนกลับ", command=lambda: (password_window.destroy(), window.deiconify()), font=("Helvetica", 14))
    back_button.pack()

    window.withdraw()  # ซ่อนหน้าต่างหลักไว้

def exit_program():
    window.destroy()  # ทำการทำลายหน้าต่างหลักเพื่อออกจากโปรแกรม

window = tk.Tk()
window.title("โปรแกรมการเข้ารหัสและถอดรหัสไฟล์")
window.geometry("400x325")  # กำหนดขนาดหน้าต่างหลัก
window.configure(bg="#66FFFF")

label = tk.Label(window, text="เลือกทำรายการ", font=("Helvetica", 30), fg="Green")
label.pack(pady=10)

encrypt_button = tk.Button(window, text="เข้ารหัส", command=encrypt_and_save, font=("Helvetica", 20))
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(window, text="ถอดรหัส", command=decrypt_and_save, font=("Helvetica", 20))
decrypt_button.pack(pady=10)

exit_button = tk.Button(window, text="ออกจากโปรแกรม", command=exit_program, font=("Helvetica", 20), bg="#e74c3c", fg="white")
exit_button.pack(pady=10)

status_label = tk.Label(window, text="", font=("Helvetica", 12), fg="blue")
status_label.pack()

window.mainloop()
