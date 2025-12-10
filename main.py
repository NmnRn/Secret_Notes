import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import ImageTk, Image
import base64


# Window Settings
window = tk.Tk()
window.title("Secret Notes")
window.minsize(height=600, width=350)
bg_color = "#a1adc2"
window.config(bg=bg_color)


# Labels
label1 = tk.Label(window, text="Enter Your Title", bg=bg_color, font=("Arial", 12, "bold"))
label2 = tk.Label(window, text="Enter Your Secret", bg=bg_color, font=("Arial", 12, "bold"))
label3 = tk.Label(window, text="Enter Master Key", bg=bg_color, font=("Arial", 12, "bold"))

# Entries
entry_title = tk.Entry(window)
entry_key = tk.Entry(window)

# Secret Text Box
text_box = tk.Text(window, height=15, width=30)

# Buttons
button_save = tk.Button(window, text="Save", fg="black", bg="white")
button_decrypt = tk.Button(window, text="Decrypt", fg="black", bg="white")

# Data Structures
lines_list = []
notes_dict = {}


# ---------------------- SYNC FUNCTION ----------------------

def sync():
    """Reads text.txt and loads saved notes into dictionary."""
    global lines_list, notes_dict
    lines_list.clear()
    notes_dict.clear()

    try:
        with open("text.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    lines_list.append(line)

        # Load pairs into dictionary (title → encoded string)
        for i in range(0, len(lines_list), 2):
            title = lines_list[i]
            encoded = lines_list[i + 1]
            notes_dict[title] = encoded

    except FileNotFoundError:
        # Session starts clean if file does not exist
        open("text.txt", "w", encoding="utf-8").close()


sync()


# ---------------------- SAVE FUNCTION ----------------------

def save_note():
    title = entry_title.get().strip()
    key = entry_key.get().strip()
    secret_text = text_box.get("1.0", tk.END).strip()

    # Validations
    if not secret_text:
        return messagebox.showerror("Error", "Please enter a secret")

    if title in notes_dict:
        return messagebox.showerror("Error", "This title already exists. Enter another title.")

    if "_" in key:
        return messagebox.showerror("Error", 'Your password must not contain "_"')

    # Prepare encrypted text
    full_message = f"{secret_text}_{key}_"
    encoded_bytes = base64.b64encode(full_message.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")

    # Save to file
    with open("text.txt", "a", encoding="utf-8") as f:
        f.write(f"\n{title}\n{encoded_string}\n")

    # Update in-memory dictionary
    notes_dict[title] = encoded_string

    # Clean inputs
    entry_title.delete(0, tk.END)
    entry_key.delete(0, tk.END)
    text_box.delete("1.0", tk.END)

    messagebox.showinfo("Info", "Secret saved successfully.")


# ---------------------- DECRYPT FUNCTION ----------------------

def get_secret():
    title = entry_title.get().strip()
    key = entry_key.get().strip()

    if not title:
        return messagebox.showerror("Error", "Please enter your title")

    if not key:
        return messagebox.showerror("Error", "Please enter your master key")

    try:
        encoded = notes_dict[title].encode("utf-8")
        decoded_msg = base64.b64decode(encoded).decode("utf-8")

        if decoded_msg.endswith(f"_{key}_"):
            note = decoded_msg.replace(f"_{key}_", "")
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.INSERT, note)
        else:
            messagebox.showerror("Error", "Not Found")

    except Exception:
        messagebox.showerror("Error", "Not Found")


# ---------------------- UI SETUP ----------------------

# Load image
try:
    image = ImageTk.PhotoImage(image=Image.open("secret.jpg"))
    label4 = tk.Label(image=image)
    label4.pack()
except Exception as e:
    print(e)


label1.pack(padx=5, pady=5)
entry_title.pack(padx=5, pady=5)

label2.pack(padx=5, pady=5)
text_box.pack(padx=5, pady=5)

label3.pack(padx=5, pady=5)
entry_key.pack(padx=5, pady=5)

button_save.pack(padx=5, pady=5)
button_save.config(command=save_note)

button_decrypt.pack(padx=5, pady=5)
button_decrypt.config(command=get_secret)

window.mainloop()
