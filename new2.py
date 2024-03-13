import tkinter as tk
from tkinter import messagebox
import mysql.connector
import validators

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'abc'


def connect_to_mysql():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_websites
                   (id INT AUTO_INCREMENT PRIMARY KEY,
                   ip VARCHAR(255),
                   url VARCHAR(255))''')
    conn.commit()
    return conn

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def is_valid_url(url):
    return validators.url(url)

def block_website():
    ip = ip_entry.get()
    blocked_site = website_entry.get()
    if not ip or not blocked_site:
        messagebox.showerror("Error", "Both IP Address and Website URL are required.")
        return
    if not is_valid_ip(ip):
        messagebox.showerror("Error", "Invalid IP Address")
        return
    if not is_valid_url(blocked_site):
        messagebox.showerror("Error", "Invalid URL")
        return
    try:
        conn = connect_to_mysql()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO blocked_websites(ip, url) VALUES (%s, %s)', (ip, blocked_site))
        conn.commit()
        messagebox.showinfo("Blocked", f"{blocked_site} has been blocked.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Failed to insert into database: {e}")
    finally:
        conn.close()


def unblock_website():
    ip = ip_entry.get()
    blocked_site = website_entry.get()
    if not ip or not blocked_site:
        messagebox.showerror("Error", "Both IP Address and Website URL are required.")
        return
    if not is_valid_ip(ip):
        messagebox.showerror("Error", "Invalid IP Address")
        return
    if not is_valid_url(blocked_site):
        messagebox.showerror("Error", "Invalid URL")
        return
    try:
        conn = connect_to_mysql()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM blocked_websites WHERE ip=%s AND url=%s', (ip, blocked_site))
        conn.commit()
        messagebox.showinfo("Unblocked", f"{blocked_site} has been unblocked.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Failed to delete from database: {e}")
    finally:
        conn.close()

root = tk.Tk()
root.title("Website Blocker")
root.configure(bg="skyblue")

label1 = tk.Label(root, text="Enter Ip Address:", fg='black', bg='skyblue')
label1.place(x=10, y=10)
label1.config(font=('Comic Sans', 12))
ip_entry = tk.Entry(root, width=50)
ip_entry.place(x=150, y=10)

label = tk.Label(root, text="Enter Website url:", fg='black', bg='skyblue')
label.place(x=10, y=40)
label.config(font=('Comic Sans', 12))
website_entry = tk.Entry(root, width=50)
website_entry.place(x=150, y=40)

block_button = tk.Button(root, text="Block", command=block_website, width=15, fg='white', bg='black')
block_button.config(font=('Comic Sans', 12))
block_button.place(x=50, y=80)

unblock_button = tk.Button(root, text="Unblock", command=unblock_website, width=15, fg='white', bg='black')
unblock_button.config(font=('Comic Sans', 12))
unblock_button.place(x=250, y=80)

root.mainloop()
