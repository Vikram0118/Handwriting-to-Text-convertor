from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter.ttk import Progressbar
import os, io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'
client = vision_v1.ImageAnnotatorClient()

BG = "#00203F"
FG = "#ADEFD1"
FN = "CONSOLAS"

def progressBar():
    progress = Toplevel()
    progress.title("PROGRESS BAR")
    progress.geometry("500x100")
    progress.config(background=FG)
    bar = Progressbar(progress, 
                      orient=HORIZONTAL, 
                      length=300)
    bar.pack(pady=20)

    def progressbar_work() :
        Label6.config(text="REQUEST MADE...")
        final = 100
        current = 0
        speed = 1
        while(current<final) :
            time.sleep(0.05)
            bar['value'] += (speed/final) * 100
            current += speed
            if(current == 50) :
                Label6.config(text="WAITING FOR SERVER TO RESPOND....")
                convert()
            window.update_idletasks()
        finish.config(state=ACTIVE)
        Label6.config(text="PROCESS COMPLETED")

    def progressbar_destroy() :
        progress.destroy()

    frameprogress = LabelFrame(progress, 
                               bg=BG,
                               borderwidth=0)
    frameprogress.pack()

    start = Button(frameprogress, 
                    text="CONVERT",
                    command=progressbar_work,
                    borderwidth=0,
                    fg=BG, 
                    font=(FN, 10),
                    bg=FG,
                    activebackground=FG,
                    activeforeground=BG,
                    state=ACTIVE)
    start.grid(row=0, column=0)

    finish = Button(frameprogress, 
                    text="FINISH",
                    command=progressbar_destroy,
                    font=(FN, 10),
                    borderwidth=0,
                    fg=BG, 
                    bg=FG,
                    activebackground=FG,
                    activeforeground=BG,
                    state=DISABLED)
    finish.grid(row=0, column=1)
   

def convert():
    print(openSFile.f_name)
    FILE_NAME = openSFile.f_name
    with io.open(FILE_NAME, 'rb') as image :
        content = image.read()
    image = vision_v1.types.Image(content = content)
    response = client.document_text_detection(image = image)
    docText = response.full_text_annotation.text
    print(docText)
    writeToFile = open(openTFile.t_name, "w")
    writeToFile.write(docText + " ")

def add_this_arg(func):
    def wrapped(*args, **kwargs):
        return func(wrapped, *args, **kwargs)
    return wrapped

@add_this_arg
def openSFile(this):
    global imageToDis
    filePath = ""
    filePath = filedialog.askopenfilename(title="File Manager",
                                          filetypes=(
                                            ("jpeg files", "*.jpeg"),
                                            ("png files", "*.png"),
                                            ("jpg files", "*.jpg"),
                                            ("all files", "*.*")
                                          ))
    print(filePath)
    if(filePath != "") : 
        Label4.config(text=filePath)
        this.f_name = filePath

@add_this_arg
def openTFile(this):
    global imageToDis
    filePath = ""
    filePath = filedialog.askopenfilename(title="File Manager",
                                          filetypes=(
                                            ("text files", "*.txt"),
                                            ("all files", "*.*")
                                          ))
    print(filePath)
    if(filePath != "") : 
        Label5.config(text=filePath)
        this.t_name = filePath
        convertButton.config(state=ACTIVE)

window = Tk()
window.title("HANDWRITING TO TEXT CONVERTOR")
window.geometry("600x600")
window.config(background=BG)

width = 30
height = 1

icon = tk.PhotoImage(file="icon.png")
window.iconphoto(True, icon)
upload = tk.PhotoImage(file="upload.png")
conver = tk.PhotoImage(file="convert.png")

Label1= Label(window, 
              text="ICT MINI PROJECT",
              width=width, 
              height= height,
              fg =FG,
              font = (FN, 40, "bold"),  
              bg= BG)
Label1.pack(pady=20)

divideLbael1 = Label(window, 
                    text="_____________________________________________________________________________________________________________________________________",
                    font=(FN, 10),
                    bg=BG,
                    fg=FG)
divideLbael1.pack()

frame1 = LabelFrame(window, 
                    bg=BG,
                    borderwidth=0
                    )
frame1.pack(pady=20)

Label11= Label(frame1,
              text="HANDWRITING ", 
              fg =FG,
              font = (FN, 40, "bold"), 
              bg= BG)
Label11.grid(row=0,column=0)

Label12= Label(frame1,
              text="TO TEXT CONVERTOR", 
              fg =FG,
              font = (FN, 40, "bold"), 
              bg= BG)
Label12.grid(row=0,column=1)

divideLbael2 = Label(window, 
                    text="_____________________________________________________________________________________________________________________________________",
                    font=(FN, 10),
                    bg=BG,
                    fg=FG)
divideLbael2.pack()


frame2 = LabelFrame(window, 
                    bg=BG,
                    borderwidth=0
                    )
frame2.pack(pady=15)

Label21= Label(frame2, 
              text="SELECT THE SOURCE FILE :  ", 
              fg =FG,
              font = (FN, 20, "bold"),
              bg= BG)
Label21.grid(row=0, column=0)

chooseButton22 = Button(frame2, 
                      text="CHOOSE FILE ", 
                      command = openSFile, 
                      image=upload,
                      font=(FN, 15),
                      fg=FG,
                      bg=BG, 
                      activeforeground=FG, 
                      activebackground=BG,
                      compound="left",
                      borderwidth=0
                      )
chooseButton22.grid(row=0, column=1)

Label4= Label(window, 
              fg =FG,
              text="(MAKE SURE THE FILE IS LESS THAN 1 MB)", 
              font = (FN, 15),  
              bg= BG)
Label4.pack()

divideLbael3 = Label(window, 
                    text="----------------------------------------------------------------------",
                    font=(FN, 10),
                    bg=BG,
                    fg=FG)
divideLbael3.pack(pady=15)


frame3 = LabelFrame(window, 
                    bg=BG,
                    borderwidth=0
                    )
frame3.pack()

Label31= Label(frame3, 
              text="SELECT THE TARGET FILE :  ", 
              fg =FG,
              font = (FN, 20, "bold"),
              bg= BG)
Label31.grid(row=0, column=0)

tragetButton32 = Button(frame3, 
                      text="CHOOSE FILE ", 
                      command = openTFile, 
                      image=upload,
                      font=(FN, 15),
                      fg=FG,
                      bg=BG, 
                      activeforeground=FG, 
                      activebackground=BG,
                      compound="left",
                      borderwidth=0
                      )
tragetButton32 .grid(row=0, column=1)

Label5= Label(window, 
              fg =FG,
              text="(MAKE SURE THE TARGET FILE IS OF TYPE *.txt )", 
              font = (FN, 15),  
              bg= BG)
Label5.pack(pady=15)


convertButton = Button(window, 
                       text="CONVERT ", 
                       command=progressBar, 
                       font=(FN, 15), 
                       fg=FG, 
                       image=conver,
                       bg=BG, 
                       activeforeground=FG, 
                       activebackground=BG,
                       compound="left",
                       state=DISABLED,
                       borderwidth=0
                       )
convertButton.pack(pady=30)

Label6= Label(window, 
              fg =FG, 
              font = (FN, 15),  
              bg= BG)
Label6.pack(pady=15)

Label7= Label(window, 
              fg =FG,
              text="DEVELOPED BY : VIKRAM P - VARATHA RAJ M - KUMAR V", 
              font = (FN, 25, "bold"),  
              bg= BG)
Label7.pack(side="bottom", pady=10)

window.mainloop()

