import tkinter
from PIL import ImageTk, Image
import messagebox
import base64

#window
window = tkinter.Tk()
window.title("Secret Notes")
window.minsize(width=500, height=500)
FONT = ('Arial', 10, 'normal')

#image
image=Image.open('images .jpeg')
img=image.resize((100, 100))
secret_img=ImageTk.PhotoImage(img)

#image label
img_label=tkinter.Label(window, image=secret_img)
img_label.pack()

#title label
title_label = tkinter.Label(text="Enter Your Title", font=FONT)
title_label.config(pady=5)
title_label.pack()

#title entry
title_entry = tkinter.Entry(width=30)
title_entry.pack()

#secret text label
secret_text_label = tkinter.Label(text="Enter Your Secret", font=FONT)
secret_text_label.config(pady=5)
secret_text_label.pack()

#secret text
secret_text = tkinter.Text(width=40, height=10)
secret_text.pack()

#key label
key_label = tkinter.Label(text="Enter Master Key", font=FONT)
key_label.config(pady=5)
key_label.pack()

#key password entry
key_entry = tkinter.Entry(window, show="*", width=20)
key_entry.pack()


#functions and buttons
def encode(key, text):
    enc = []
    for i in range(len(text)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(text[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def save_text():
    title = title_entry.get()
    text = secret_text.get("1.0", 'end-1c')
    key = key_entry.get()
    if title == "" or text == "" or key == "":
        messagebox.showwarning(title="Warning", message="Fill in all the blanks!!!")
    else:
        encrypted_text = encode(key, text)
        with open("mysecret.txt", "a") as file:
            file.write(title)
            file.write("\n")
            file.write(encrypted_text)
            file.write("\n")

        title_entry.delete(0,tkinter.END)
        secret_text.delete("1.0", tkinter.END)
        key_entry.delete(0, tkinter.END)


def show_text():
    encrypted_text = secret_text.get("1.0", 'end-1c')
    key = key_entry.get()
    if encrypted_text == "" and key == "":
        messagebox.showwarning("Warning", "Enter both text and key!!!")
    elif encrypted_text == "":
        messagebox.showwarning("Warning", "Enter a text!!!")
    elif key == "":
        messagebox.showwarning("Warning", "Enter a key!!!")
    else:
        decrypted_text = decode(key, encrypted_text)
        secret_text.delete("1.0", tkinter.END)
        secret_text.insert("1.0", decrypted_text)


#encrypt button
encrypt_button = tkinter.Button(text="Save & Encrypt", font=FONT, command=save_text)
encrypt_button.pack()

#decrypt button
decrypt_button = tkinter.Button(text="Decrypt", font=FONT, command=show_text)
decrypt_button.pack()


window.mainloop()