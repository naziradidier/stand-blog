import datetime
import os
import tkinter
import numpy as np

from PIL import Image as Img
from PIL import ImageTk
import pytesseract
import cv2
from tkinter import *

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

specs_ori = cv2.imread('img/glass.png', -1)
cigar_ori = cv2.imread('img/cigar.png', -1)
mus_ori = cv2.imread('img/mustache.png', -1)

width, height = 800, 450
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cv2image = None
frame = None
gallery = None
filter = 0


def save():
     global cv2image, frame
     time = "img-saved/" + str(datetime.datetime.now().today()).replace(":", "-") +".png"
     frame.save(time)
     print()
      
      
def cancel():
    print()

    
def filtering(i):
     global filter
     if filter != i:
          filter = i
     else:
         filter = 0

 
def mail():
     import smtplib
     from email.mime.multipart import MIMEMultipart
     from email.mime.text import MIMEText
     from email.mime.base import MIMEBase
     from email import encoders
 
     fromaddr = ‘sender@email.com’
     toaddr = [‘sender@email.com’, ‘receiver@email.com’, ‘receiver2@email.com’]
     
     # instance of MIMEMultipart
     msg = MIMEMultipart()
      
     # storing the senders email address
     msg['From'] = fromaddr
      
     # storing the receivers email address
     msg['To'] = ','.join(toaddr)
      
     # storing the subject
     msg['Subject'] = "Your Magic Photo"
      
     # string to store the body of the mail
     body = "Hello,\n\nHere's your awesome magic photo from The PhotoBooth."
      
     # attach the body with the msg instance
     msg.attach(MIMEText(body, 'plain'))
      
     # open the file to be sent
     filename = 'D1G1TALArtboard4.jpg'
     attachment = open('D1G1TALArtboard4.jpg', "rb")
    
     # instance of MIMEBase and named as p
     p = MIMEBase('application', 'octet-stream')
    
     # To change the payload into encoded form
     p.set_payload((attachment).read())
    
     # encode into base64
     encoders.encode_base64(p)
     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      
     # attach the instance 'p' to instance 'msg'
     msg.attach(p)
      
     # creates SMTP session
     s = smtplib.SMTP('smtp.gmail.com', 587)
      
     # start TLS for security
     s.starttls()
      
     # Authentication
     s.login(fromaddr, "password")
      
     # Converts the Multipart msg into a string
     text = msg.as_string()
      
     # sending the mail
     s.sendmail(fromaddr, toaddr, text)
      
     # terminating the session
     s.quit()
      
def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
     overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
     h, w, _ = overlay.shape # Size of foreground
     rows, cols, _ = src.shape # Size of background Image
     y, x = pos[0], pos[1] # Position of foreground/overlay image
     for i in range(h):
          for j in range(w):
               if x + i >= rows or y + j >= cols:
                  continue
               alpha = float(overlay[i][j][3] / 255.0) # read the alpha channel
               src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
           return src
        
        
def load_images():
      pass
  
  
def open_gallery():
    global gallery
    try:
       gallery.deiconify()
       print('Gallery already open...')
      
    except:
         gallery = Toplevel(root)
         gallery.title("Gallery")
         gallery.geometry("500x600")
         container = Frame(gallery, height=600)
          
         canvas = Canvas(container, height=600)
         scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
         scrollable_frame = Frame(canvas)
         cacanvas = Canvas(scrollable_frame)
          
         scrollable_frame.bind(
             "<Configure>",
             lambda e: canvas.configure(
             scrollregion=canvas.bbox("all")
             )
         )
         canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
         canvas.configure(yscrollcommand=scrollbar.set)
        
         load_images()
          
         imgdir = os.path.dirname(__file__) + "\img-saved"
        
         x, y, i = 0, 0, 0
          
         for filename in reversed(os.listdir(imgdir)):
             if filename.endswith(".png"):
                 file = "img-saved/" + filename
                 # print(file)
                 load = Img.open(str(file))
                 image1 = load.resize((250, 185), Img.ANTIALIAS)
                 render = ImageTk.PhotoImage(image1)
                 img = Label(scrollable_frame, image=render)
                 img.image = render
                 if i % 2 == 0:
                     x = 0
                    if i != 0:
                        y += 200
                 else:
                     x = 250
                 img.place(x=x, y=y)
                 print(i, " >> ", filename, " >>> ", x, " - ", y)
                 i += 1
             else:
                 continue
                
             container.pack(fill=BOTH)
            
             canvas.pack(side="left", fill="both", expand=True)
             scrollbar.pack(side="right", fill="y")
             cacanvas.pack(side="left", fill="both", expand=True)
              
# root
root = Tk()
# root.iconbitmap('image/icon.ico')
root.title("Pydev")
root.geometry("970x600")
root.resizable(0, 0)
root.bind('<Escape>', lambda e: root.quit())

# frames
frame = Frame(root, width=970, height=600, background="black")
frame.pack(fill="both", expand=YES)
frame.pack_propagate(FALSE)

# frame filtre
frame_filtre = Frame(frame, width=200, height=600, background="blue")
frame_filtre.grid(row=0, rowspan=6, column=0, columnspan=1, sticky=N + E + W + S)
frame_filtre.grid_propagate(FALSE)

# frame sary
frame_sary = Frame(frame, width=800, height=450, background="purple")
frame_sary.grid(row=0, rowspan=5, column=1, columnspan=4, sticky=N + E + W + S)
frame_sary.grid_propagate(FALSE)

# frame bouton
frame_bouton = Frame(frame, width=800, height=150, background="red")
frame_bouton.grid(row=5, rowspan=1, column=1, columnspan=4, sticky=N + E + W + S)
frame_bouton.grid_propagate(FALSE)

lmain = Label(frame_sary)
lmain.pack()

########
frame_b1 = Frame(frame_bouton, width=300, height=150, background="gray")
frame_b1.grid(row=0, column=0, sticky=N + E + W + S)
frame_b1.grid_propagate(FALSE)
frame_b2 = Frame(frame_bouton, width=200, height=150, background="yellow")
frame_b2.grid(row=0, column=1, sticky=N + E + W + S)
frame_b2.grid_propagate(FALSE)
frame_b3 = Frame(frame_bouton, width=300, height=150, background="red")
frame_b3.grid(row=0, column=2, sticky=N + E + W + S)
frame_b3.grid_propagate(FALSE)

# buttons
bouton_cancel = Button(frame_b1, text="Gallery", bg='#000000', command=open_gallery, 
relief=FLAT, font=("bold", 18), fg="white")

bouton_cancel.pack(padx=60, pady=29)
bouton_take = Button(frame_b2, text="Capture", bg='#000000', command=save, relief=FLAT, 
font=("bold", 18), fg="white")
bouton_take.pack(padx=60, pady=29)

bouton_save = Button(frame_b3, text="Save", bg='#000000', command=save, relief=FLAT, 
font=("bold", 18), fg="white")
bouton_save.pack(padx=60, pady=29)

bou1 = Button(frame_filtre, text='Glass', width=20, bg="black", fg="white", 
relief=FLAT, command=lambda: filtering(1))
bou1.pack(side=TOP, padx=10, pady=12)

bou2 = Button(frame_filtre, text='Cigar', width=20, bg="black", fg="white", 
relief=FLAT, command=lambda: filtering(2))

bou2.pack(side=TOP, padx=10, pady=4)
bou3 = Button(frame_filtre, text='Mustache', width=20, bg="black", fg="white", 
relief=FLAT,
 command=lambda: filtering(3))
bou3.pack(side=TOP, padx=10, pady=8)


def show_frame():
     global filter, frame
     _, frame = cap.read()
     frame = cap.read()[1]
     frame = cv2.flip(frame, 1)
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     faces = face_cascade.detectMultiScale(frame, 1.2, 5, 0, (120, 120), (350, 350))
     for (x, y, w, h) in faces:
          if h > 0 and w > 0:
             glass_symin = int(y + 1.5 * h / 5)
             glass_symax = int(y + 2.5 * h / 5)
             sh_glass = glass_symax - glass_symin
            
             cigar_symin = int(y + 4 * h / 6)
             cigar_symax = int(y + 5.5 * h / 6)
             sh_cigar = cigar_symax - cigar_symin
              
             mus_symin = int(y + 3.5 * h / 6)
             mus_symax = int(y + 5 * h / 6)
             sh_mus = mus_symax - mus_symin
            
             face_glass_roi_color = frame[glass_symin:glass_symax, x:x + w]
             face_cigar_roi_color = frame[cigar_symin:cigar_symax, x:x + w]
             face_mus_roi_color = frame[mus_symin:mus_symax, x:x + w]
              
             specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
             cigar = cv2.resize(cigar_ori, (w, sh_cigar), interpolation=cv2.INTER_CUBIC)
             mustache = cv2.resize(mus_ori, (w, sh_mus), interpolation=cv2.INTER_CUBIC)
            
            if filter == 1:
                transparentOverlay(face_glass_roi_color, specs)
             elif filter == 2:
                transparentOverlay(face_cigar_roi_color, cigar, (int(w / 2), int(sh_cigar / 2)))
             elif filter == 3:
                transparentOverlay(face_mus_roi_color, mustache)
                
 cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
 frame = Img.fromarray(cv2image)
 frametk = ImageTk.PhotoImage(image=frame)
 lmain.frametk = frametk
 lmain.configure(image=frametk)

 # key = cv2.waitKey(1) & 0xFF
 # if key == ord("q"):
 # print("kokokokkkook")
 # return
 #
 # k = cv2.waitKey(30) & 0xff
 # if k == 27:
 # cv2.imwrite('frame.jpg', frame)
 # return
 lmain.after(10, show_frame)
show_frame()
root.mainloop()
