import socket
import tkinter as tk
from tkinter import *
import easygui  # to open the firebox

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ClientSocket.connect(('127.0.0.1', 7008))  # connects the client
# for sending unique IP
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)  # gets local IP address of the client
ClientSocket.send(ip_address.encode())  # sending the ip address to the server
print(ClientSocket.recv(2048).decode())  # prints out the question


# -----------------------------------------------------------------
def tkinter_pop_box():
    tk1 = tk.Tk()
    def upload():
        ImagePath = easygui.fileopenbox()
        print(ImagePath)
        if ".jpg" in ImagePath:
            print("Valid Image File")
        else:
            print("Add a Valid Image File")
            tk1.after(1000, lambda: tk1.destroy())
            tkinter_pop_box()
        ClientSocket.send((str(ImagePath)).encode())
        tk1.after(1000, lambda: tk1.destroy())
    tk1.geometry('800x800')
    tk1.title('Upload Your Image to See the Magic')
    tk1.configure(background='white')
    label = Label(tk1, background='#CDCDCD', font=('calibri', 20, 'bold'))
    upload = Button(tk1, text = "Please Add Valid JPG or PNG file", command=upload, padx=20, pady=30)
    upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    upload.pack(side=TOP, pady=300)
    tk1.mainloop()
tkinter_pop_box()
# -----------------------------------------------------------------

ClientSocket.close()
