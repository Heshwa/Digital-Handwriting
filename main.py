
from google.cloud import storage
from google.cloud import vision
from tkinter import filedialog
from tkinter import *
import tkinter.font as tkFont
import speech_recognition as sr
import handwritingio
import os
import io 
import cv2 as cv
from PIL import Image ,ImageTk



Image_path="images.jpg"
key_path='G:\projects\python\handScribble\key.json'
bucket_name='digital_images_storage'
API_TOKEN = "JJ3W4EV2CXB3WNX4"
API_SECRET = "4AF3M7CX8ZJ8Q2V7"


def browse():

    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("PNG", "*.png"),("jpeg files", "*.jpg"), ("all files", "*.*")))
    print('file with {} address is chosen.'.format(filename))
    return filename


def create_bucket():
    storage_client = storage.Client.from_service_account_json(key_path)
    bucket = storage_client.create_bucket(bucket_name)
    print("Bucket {} created.".format(bucket.name))


def upload_image(path):
    storage_client = storage.Client.from_service_account_json(key_path)
    bucket = storage_client.get_bucket(bucket_name)
    filename = "%s/%s" % ('', 'demo.png')
    blob = bucket.blob(filename)
    with open(path, 'rb') as photo:
        blob.upload_from_file(photo)
    blob.make_public()
    print('image has been succefully uploaded ')
    url = blob.public_url
    return url


def detect(url):
    client = vision.ImageAnnotatorClient.from_service_account_json(key_path)
    image = vision.types.Image()
    image.source.image_uri = url
    response = client.text_detection(image=image)
    document = response.full_text_annotation
    return document.text

def sample_recognize():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("please say something...")
        audio=r.listen(source)

        try:
            text=r.recognize_google(audio)
            return text

        except Exception as e:
            print('Error:'+str(e))


def handwritiing(text):
    
    hwio = handwritingio.Client(API_TOKEN, API_SECRET)
    pdf = hwio.render_pdf({
        'text': text,
        'handwriting_id': '2D5S46A80003',
        'height': 'auto',
        'handwriting_color': '(1, 0.5, 0, 0.2)',
    })
    with open('handwriting2.pdf', 'wb') as f:
        f.write(pdf)
    print("Text has been sucessulfy rended in pdf")

def handwritiing_png(text):
    hwio = handwritingio.Client(API_TOKEN, API_SECRET)
    png = hwio.render_png({
    'text': text,
    'handwriting_id': '2D5S46A80003',
    'handwriting_color':'#FFFFFF',
    'height': 'auto',
    })
    with open('handwriting.png', 'wb') as f:
        f.write(png)


def removing_handwriting_logo():
    img=cv.imread('handwriting.png')
    grey=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    _,thre=cv.threshold(grey,230,255,cv.THRESH_BINARY)
    result=cv.bitwise_and(img,img,mask=thre)
    cv.imwrite("output.png",result)


def png_pdf_convert():
    image1 = Image.open('output.png')
    im1 = image1.convert('RGB')
    im1.save('output.pdf')









class Window:
    def __init__(self):
        self.gui = Tk()
        self.gui.geometry("%dx%d+0+0" % (1920,1080))
        
        


        # self.image1 = PhotoImage(file='images.png')
        # w = self.image1.width()
        # h = self.image1.height()
    
        # self.panel1 = Label(self.gui, image=self.image1)
        # self.panel1.pack(side='top', fill='both', expand='yes')


        
        self.gui.title("Digital Handwriting")
        self.heading = Label(self.gui,text='Digital Handwriting',fg='BLack',font=tkFont.Font(family="Roman", size=70, weight="bold", slant="italic"))
        self.image = Button(self.gui, text="Upload Image", fg="Black", command=self.imagetext)
        self.speech = Button(self.gui, text="Tap to Speak", command=self.speechtext)
        self.text = Button(self.gui, text="Activate text", command=self.activateText)
        self.submit = Button(self.gui, text="Submit", command=self.texttext)
        self.TextArea = Text(self.gui, height=23, width=50, font="lucida 13")
        self.TextArea.config(state='disabled')
         

   

        self.heading.place(x=400,y=50)
        self.image.place(x=600,y=200)
        self.speech.place(x=800,y=200)
        self.text.place(x=700,y=250)
        self.TextArea.place(x=150,y=300)
        self.submit.place_forget()
        




        self.gui.mainloop()

    def imagetext(self):
        self.TextArea.config(state='normal')
        self.TextArea.delete(1.0,END)
        path = browse()
         # create_bucket()
        uri = upload_image(path)
        text = detect(uri)
        self.TextArea.insert(END, text)
        # handwritiing(text)
        handwritiing_png(text)
        self.TextArea.config(state='disabled')
        removing_handwriting_logo()
        self.display_image()
        png_pdf_convert()
    
    def activateText(self):
        self.TextArea.config(state='normal')
        self.TextArea.delete(1.0,END)
        self.submit.place(x=550,y=750)
        

    def texttext(self):
        text = self.TextArea.get("1.0",'end-1c')
         # handwritiing(text)
        handwritiing_png(text)
        self.submit.place_forget()
        self.TextArea.config(state='disabled')
        removing_handwriting_logo()
        self.display_image()
        png_pdf_convert()

    def speechtext(self):
        self.TextArea.config(state='normal')
        self.TextArea.delete(1.0,END)
        text = sample_recognize()
        self.TextArea.insert(END,text)
        # handwritiing(text)
        handwritiing_png(text)
        self.submit.place_forget()
        self.TextArea.config(state='disabled')
        removing_handwriting_logo()
        self.display_image()
        png_pdf_convert()
        
        
        

    def display_image(self):
        self.image1 = Image.open('output.png')
        self.render = ImageTk.PhotoImage(self.image1)
        self.panel1 = Label(self.gui, image=self.render)
        self.panel1.place(x=820,y=300)
             
           


if __name__== "__main__":
    
    mywin = Window()
    






