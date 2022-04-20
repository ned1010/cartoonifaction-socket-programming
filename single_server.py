import os
import socket
import tkinter as tk
from tkinter import *
import cv2  # for image processing
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

# instantiate server's socket
ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# define address params
IP = '127.0.0.1'
PORT = 7008

# bind server and start listening
ServerSocket.bind((IP, PORT))
print('Server is running at IP {} and PORT {}'.format(IP, PORT))
ServerSocket.listen(5)
ThreadCount = 0  # increment the number of connection

# Will load pre-trained data from open Cv using haar cascade algorithm
trained_face_data = cv2.CascadeClassifier('haarcascade_frontalcatface_extended.xml')

# -------------------------------------------------------------------------------------------------
# defining the specifics of the screen that will ask for the image
tk1 = tk.Tk()  # using library to display
tk1.configure(background='white')  # setting background
tk1.geometry('800x600')  # setting size
tk1.title('Download the Image!')  # giving a title to the screen
label = Label(tk1, background='#CDCDCD', font=('calibri', 20, 'bold'))


# ML code for cartoonifying the image
def Image_Changer(ImPath):
    # 1. ORIGINAL
    # opening the image by using the path of the image
    image1 = Image.open(ImPath)
    ogIm = cv2.imread(ImPath)
    # converting the color of the image from BGR to RGB and resizing
    ogIm = cv2.cvtColor(ogIm, cv2.COLOR_BGR2RGB)
    im1 = cv2.resize(ogIm, (960, 540))



    # Detect Cat Face
    # change the colored image into black and white
    grayscaled_image = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("grayscaled-image",grayscaled_image)
    # Detect the faces
    faces = trained_face_data.detectMultiScale(grayscaled_image)

    for (x, y, w, h) in faces:
        # Draw the rectangle around each face
        cv2.rectangle(im1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Display
        cv2.imshow('face-captured', im1)
    cv2.waitKey(0)


    # 2. GRAYSCALE
    # converting the color of the image from BGR to RGB and resizing 
    gsimage = cv2.cvtColor(ogIm, cv2.COLOR_BGR2GRAY)
    im2 = cv2.resize(gsimage, (960, 540))

    # 3. CENTER BLURRED
    # central element of image is replaced by the median of all the pixels
    cv2.medianBlur(gsimage, 5)
    sgsimage = cv2.medianBlur(gsimage, 5)
    im3 = cv2.resize(sgsimage, (960, 540))

    # 4. EDGES
    # getting edges of image by using thresholding technique and resizing 
    edImage = cv2.adaptiveThreshold(sgsimage, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    im4 = cv2.resize(edImage, (960, 540))

    # 5. SHARPER WITH EDGES
    # now that we have an images where all the edges become apparent
    # removing noise and keeping edges sharp by applying bilateral filter
    cImage = cv2.bilateralFilter(ogIm, 9, 300, 300)
    im5 = cv2.resize(cImage, (960, 540))

    # 6. CARTOON
    # masking edged image with our "BEAUTIFY" image
    cim = cv2.bitwise_and(cImage, cImage, mask=edImage)
    im6 = cv2.resize(cim, (960, 540))

    # plotting the images that we have created right now
    images = [im1, im2, im4, im6]
    fig, axes = plt.subplots(2, 2, figsize=(10, 10), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
        ax.set_title("image " + str(i+1))
    j = 1
    for image in images:
        save1 = Button(tk1, text="Download Image " + str(j), command=lambda: save(image, ImPath), padx=100, pady=20)
        save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
        save1.pack(side=TOP, pady=40)
        j=j+1
    plt.show()


# saving the image and giving the option to do so

def save(im, ImPath):
    # giving name, path, and extension
    name = "cartoonified_image"
    path1 = os.path.dirname(ImPath)
    extension = os.path.splitext(ImPath)[1]
    path = os.path.join(path1, name + extension)
    cv2.imwrite(path, cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
    # showing the message after saving
    msg = "Image saved as " + name + " at " + path
    tk.messagebox.showinfo(title = "Your Image has been Downloaded", message = msg)


# Driver Code
while True:
    try:
        ClientSocket, address = ServerSocket.accept()
        ThreadCount += 1
        print('Connection Request: ' + str(ThreadCount))
        ip_address = ClientSocket.recv(1024).decode()
        reply = "Upload Your Image!"
        ClientSocket.send(reply.encode())
        Image_Path = ClientSocket.recv(1024).decode()
        print(Image_Path)
        Image_Changer(Image_Path)
    except:
        print("Something Went Wrong!")
        ClientSocket.close()

ServerSocket.close()
