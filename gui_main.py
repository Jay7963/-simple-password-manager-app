import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from crypto_utils import *


def prompt_master_password():
    master_pw = askstring("Master Password", "Enter your master password:", show='*')
    if master_pw and check_master_password(master_pw):
        return True
    else:
        messagebox.showerror("Error", "Incorrect master password!")
        return False


def save_password_gui():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not site or not username or not password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    key = load_key()
    if save_password(site, username, password, key):
        messagebox.showinfo("Success", f"Password for '{site}' saved successfully.")
    else:
        messagebox.showerror("Error", "Failed to save password.")


def view_passwords_gui():
    key = load_key()
    data = load_passwords(key)

    if data is None:
        messagebox.showerror("Error", "Failed to load passwords.")
        return

    if not data:
        messagebox.showinfo("No Passwords", "No passwords stored.")
        return

    output = ""
    for site, creds in data.items():
        output += f"Site: {site}\nUsername: {creds['username']}\nPassword: {creds['password']}\n\n"

    text_area.delete(1.0, tk.END)  
    text_area.insert(tk.END, output)


def search_password_gui():
    search_term = search_entry.get()

    if not search_term:
        messagebox.showwarning("Search Error", "Please enter a site name to search.")
        return

    key = load_key()
    data = load_passwords(key)

    if data is None:
        messagebox.showerror("Error", "Failed to load passwords.")
        return

    found = False
    output = ""
    for site, creds in data.items():
        if search_term.lower() in site.lower():
            found = True
            output += f"Site: {site}\nUsername: {creds['username']}\nPassword: {creds['password']}\n\n"

    if found:
        text_area.delete(1.0, tk.END)  
        text_area.insert(tk.END, output)
    else:
        messagebox.showinfo("No Results", "No passwords found for that site.")

def setup_window():
    window = tk.Tk()
    window.title("Simple Password Manager")
                                                                                                                                        
    tk.Label(window, text="Site:").grid(row=0, column=0, padx=10, pady=5)
    global site_entry
    site_entry = tk.Entry(window, width=30)
    site_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Username:").grid(row=1, column=0, padx=10, pady=5)
    global username_entry
    username_entry = tk.Entry(window, width=30)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Password:").grid(row=2, column=0, padx=10, pady=5)
    global password_entry
    password_entry = tk.Entry(window, width=30, show="*")
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    save_button = tk.Button(window, text="Save Password", command=save_password_gui)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

    view_button = tk.Button(window, text="View All Passwords", command=view_passwords_gui)
    view_button.grid(row=4, column=0, columnspan=2, pady=10)

    
    tk.Label(window, text="Search Site:").grid(row=5, column=0, padx=10, pady=5)
    global search_entry
    search_entry = tk.Entry(window, width=30)
    search_entry.grid(row=5, column=1, padx=10, pady=5)

    search_button = tk.Button(window, text="Search", command=search_password_gui)
    search_button.grid(row=6, column=0, columnspan=2, pady=10)

    global text_area
    text_area = tk.Text(window, width=50, height=10)
    text_area.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    window.mainloop()

if __name__ == "__main__":
    if not master_password_exists() or prompt_master_password():
        setup_window()
