import os 
import pandas as pd
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import tkinter.messagebox
import smtplib
import PyPDF2
import re
import glob
import sys
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pd.options.mode.chained_assignment = None  # default='warn'

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
root = Tk()
root.title("Certificate Generator")
root.geometry('280x100') 


def show_image(root,l,l2,l3,l4,name_event):
    file = askopenfile(mode ='r', filetypes =[('Image Files', ['*.jpg','*.jpeg','*.png'])]) 
    C1=l.get(1.0, "end-1c")
    C2=l2.get(1.0, "end-1c")
    C3=l3.get(1.0, "end-1c")
    C4=l4.get(1.0, "end-1c")
    C5=name_event.get(1.0, "end-1c")
    img = Image.open(file.name)
    rgb = Image.new('RGB', img.size, (255, 255, 255)) 
    rgb.paste(img, mask=img.split()[3]) 
    draw = ImageDraw.Draw(rgb)
    draw.text( (int(C1),int(C2)), "FIRST_NAME MIDDLE_NAME LAST_NAME", (0,0,255), font=ImageFont.truetype("arial.ttf", 35) )
    draw.text( (int(C3),int(C4)), C5, (0,0,255), font=ImageFont.truetype("arial.ttf", 35) )
    im1 = rgb.resize((1000,800))
    im1.show()
    b2 = Button(root, text = "Next",command=lambda:open_image(root,int(C1),int(C2),int(C3),int(C4),file.name,C5))
    b2.place(x=150, y=200)


def send_mail(root,name_event,email1,password):
    email1=email1.get()
    password=password.get()
    files=[]
    mypath = 'Certificates'
    
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(email1,password)
    if(re.search(regex, email1)):
        for file in glob.glob(mypath + "/*.pdf"):
            if file.endswith('.pdf'):
                files.append(file)
            else:
                pass
        for i,j,k in zip(files,name,email):
            with open(i, "rb") as attachment:
       
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {i}",
            )
            msg = MIMEMultipart()
            msg['Subject'] = name_event+' Certificate'
            msg['From'] = email1
            msg['To'] = k
            body = "Thank you "+j+", for participating in "+name_event+". Your certificate is attached to this email for you to download and print.\n"
            body2="INSTAGRAM_LINK"+"\n"
            body3="Follow us on Instagram"+"\n"
            msg.attach(MIMEText(body, "plain"))
            msg.attach(MIMEText(body2, "plain"))
            msg.attach(MIMEText(body3, "plain"))
            msg.attach(part)
            text = msg.as_string()
            s.sendmail(email1, k, text)
        s.quit()
    else:
        tkinter.messagebox.showinfo("Error!!","Invalid Email Id Format")
    
def open_image(root,C1,C2,C3,C4,file,C5):
    mypath = 'Certificates'
    if(len(os.listdir(mypath))==0):
        pass
    else:
        for f in glob.glob(mypath + "/*.pdf"):
            os.remove(f)
    for i in range(len(ID)):
        img = Image.open(file)
        rgb = Image.new('RGB', img.size, (255, 255, 255))  # white background
        rgb.paste(img, mask=img.split()[3]) 
        draw = ImageDraw.Draw(rgb)
        
        font = ImageFont.truetype("arial.ttf", 35)
        draw.text( (C1,C2),name[i], (0,0,255), font=font )
        draw.text( (C3,C4),C5, (0,0,255), font=font )
        rgb.save( 'Certificates\\'+C5+"_"+str(ID[i])+"_"+name[i]+'.pdf', "PDF", resolution=100.0)
    tkinter.messagebox.showinfo("Information","Done!!!!")
    root.quit()
    root=Tk()
    root.title("Send Mail")
    root.geometry('400x350')
    label1=Label(root, text = "Email-ID ")
    label1.config(font =("Courier", 12))
    label1.place(x=25, y=30)
    label2=Label(root, text = "Password ")
    label2.config(font =("Courier", 12))
    label2.place(x=25, y=90)
    email1=tk.StringVar()
    password=tk.StringVar()
    e1 = tk.Entry(root, show=None,textvariable = email1 ,font=('Courier', 12))  
    e2 = tk.Entry(root, show='*',textvariable = password ,font=('Courier', 12))
    e1.place(x=140, y=30)
    e2.place(x=140, y=90)
    button=Button(root, text = "Send",command=lambda:send_mail(root,C5,e1,e2))
    button.place(x=50, y=200)
    


def make_certi( ID, name):
    
    root = Tk()
    root.title("Certificate")
    root.geometry('300x280') 
    T = Text(root, height = 1, width = 12)
    T2=Text(root, height = 1, width = 12)
    T3 = Text(root, height = 1, width = 12)
    T4=Text(root, height = 1, width = 12)
    T.place(x=20, y=50)
    T2.place(x=140, y=50)
    T3.place(x=20, y=110)
    T4.place(x=140, y=110)
    name = Label(root, text = "Name of Student Coordinates")
    name.config(font =("Courier", 12))
    name.place(x=25, y=12)
    name2 = Label(root, text = "Name of Event Coordinates")
    name2.config(font =("Courier", 12))
    name2.place(x=25, y=70)
    l = Label(root, text = "X")
    l.config(font =("Courier", 8))
    l.place(x=60, y=30)
    l2 = Label(root, text = "Y")
    l2.config(font =("Courier", 8))
    l2.place(x=190, y=30)
    l3 = Label(root, text = "X")
    l3.config(font =("Courier", 8))
    l3.place(x=60, y=90)
    l4 = Label(root, text = "Y")
    l4.config(font =("Courier", 8))
    l4.place(x=190, y=90)
    label= Label(root, text = "Name of Event")
    label.config(font =("Courier", 10))
    label.place(x=25, y=160)
    name_event=Text(root, height = 1, width = 12)
    name_event.place(x=140, y=160)
    b1 = Button(root, text = "Upload Image",command=lambda:show_image(root,T,T2,T3,T4,name_event))
    b1.place(x=50, y=200)
    
def open_file():
    global ID,name,email
    ID=[]
    name=[]
    email=[]
    
    file = askopenfile(mode ='r', filetypes =[('Data Files', '*.xlsx')]) 
    data=pd.read_excel(file.name)
    len1=len(data["id"])
    for i in range(len1):
        spl=data["name"][i].split(" ")
        name.append(" ".join([j.title() for j in spl]))
        ID.append(i+1)
        email.append(data["email"][i])
    filename = make_certi( ID, name) 
    
label= Label(root, text = "Select Data File of xlsx format")
label.config(font =("Courier", 8))
label.place(x=5, y=25)
btn = Button(root, text ='Browse', command = lambda:open_file()) 
btn.place(x=70, y=50)
mainloop() 


