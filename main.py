import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import base64


window = tk.Tk()
window.title("Secret Notes")
window.minsize(height=600, width=350)
bg_color = "#a1adc2"
window.config(bg=bg_color)


label1 = tk.Label(window, text="Enter Your Title", bg= bg_color, font=("Arial", 12, "bold"))
label2 = tk.Label(window, text="Enter Your Secret",bg= bg_color,font=("Arial", 12,"bold"))
label3 = tk.Label(window, text="Enter Master Key",bg= bg_color,font=("Arial", 12,"bold"))

entry1 = tk.Entry(window)
entry2 = tk.Entry(window)

text1 = tk.Text(window)
text1.config(height=15, width=30)

button1 = tk.Button(window, text="Save", fg="Black", bg="white")
button2 = tk.Button(window, text="Decrypt", fg="Black", bg="white")

my_list = []
dictionary = dict()

def sync():
    with open("text.txt", "r", encoding="utf-8") as f:

        for line in f.readlines():
            if line == "\n":
                continue
            if "\n" in line:
                line = line.replace("\n", "")
            my_list.append(line)

        x = 0
        if not len(my_list) == 0:
            while x <= len(my_list) / 2:
                dictionary.update({my_list[x]: my_list[x + 1]})
                x += 2
sync()

def save_note():
    with open("text.txt","a", encoding="utf-8") as file:
        msg_entry1 = entry1.get().strip()
        msg_entry2 = entry2.get().strip()
        if text1.get("1.0",tk.END).strip() == "":
            messagebox.showerror("Error", "Please enter a secret")
            return
        if msg_entry1 in dictionary.keys():
            return messagebox.showerror("Error", "Please enter another title")

        msg_text = text1.get("1.0", tk.END).strip() + msg_entry2

        base64Bytes = base64.b64encode(msg_text.encode("utf-8"))
        base64Bytes_decode = base64Bytes.decode("utf-8")

        if msg_entry1 and msg_entry2 and msg_text:
            file.write(f"\n{msg_entry1}\n{base64Bytes_decode}\n")
            messagebox.showinfo(title="Info", message="Secret Saved")
            entry1.delete("0", tk.END)
            entry2.delete("0", tk.END)
            text1.delete("1.0", tk.END)

        else:
            messagebox.showwarning(title="Warning", message="Please Enter All Information's.")

        file.close()


def get_secret():
        sync()
        try:
            byte64 = dictionary[entry1.get().strip()].encode("utf-8")

            secret_note_byte = base64.b64decode(byte64)
            secret_note = secret_note_byte.decode("utf-8")

            if secret_note.endswith(entry2.get().strip()):
                note = secret_note.replace(entry2.get().strip(), "")
                text1.delete("1.0", tk.END)
                text1.insert(tk.INSERT, note)
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Error: Not Found")



image = Image.open("secret.png")
photo = ImageTk.PhotoImage(image)
panel = tk.Label(window, image=photo, bg=bg_color)
panel.pack()


label1.pack(padx=5, pady=5)

entry1.pack(padx=5, pady=5)

label2.pack(padx=5, pady=5)

text1.pack(padx=5, pady=5)

label3.pack(padx=5, pady=5)

entry2.pack(padx=5, pady=5)

button1.pack(padx=5, pady=5)
button1.config(command=save_note)

button2.pack(padx=5, pady=5)
button2.config(command=get_secret)


window.mainloop()