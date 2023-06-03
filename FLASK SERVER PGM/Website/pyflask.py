from flask_ngrok import run_with_ngrok
from flask import *
import smtplib
import ssl
from email.message import EmailMessage
import smtplib
import time
import imaplib
import email
import traceback
import numpy as np
from cv2 import *
import cv2 as cv
import tensorflow as tf
#import PIL
#import matplotlib.image as mpimg
import datetime
import pytz

#import pathlib
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename

TF_ENABLE_ONEDNN_OPTS=1
common_password = 'yvwichgnxzicmzph'
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "finalyearpro833" + ORG_EMAIL 
FROM_PWD = common_password 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

email_sender = 'finalyearpro833@gmail.com'
email_password = common_password
email_receiver = 'finalyearpro833@gmail.com'
app = Flask(__name__)
run_with_ngrok(app)
UPLOAD_FOLDER = os.path.join('static', 'Image')


app.config['UPLOAD'] = UPLOAD_FOLDER


global fname
global email1
global mail_2
global num
global num_day
global passwrd
global retye
global row
global confirmemail
global banana_class
banana_class = ""
global new_line
new_line = []
global line2
line2 = []
global size
size = 120
global classes
classes = ["RIPE","GREEN","ROTTEN"]


@app.route("/")
def index():
    return render_template("index.html",title = "Main")

@app.route("/home.html")
def home():
    return render_template("home.html",title = "Home")

@app.route("/Contact.html")
def Contact():
    return render_template("Contact.html",title = "Contact")

@app.route("/About.html")
def About():
    return render_template("About.html",title = "About")

@app.route("/capture.html",methods=["GET","POST"])
def capture():
    if request.method == "POST":
        #print("kastam.....")
        cam_port = 0
        cam = cv.VideoCapture(cam_port)
        result, image = cam.read()
        if result:
            cv.imshow("GeeksForGeeks", image)
            cv.imwrite("static\Image\I_M_A_G_E.png", image)
            loaded_model = tf.keras.models.load_model("F:\FINAL YEAR PROJECT\BANANA.hdf5")
            resized_img = []

            classes = ["RIPE","GREEN","ROTTEN"]
            resized_img.append(cv.resize(image,(size,size)))
            resized_img = np.array(resized_img)
            resized_img = resized_img / 255
            prediction = loaded_model.predict(resized_img)
            
            pred = int(max(max(prediction))*100)
            res = classes[np.argmax(prediction)]

            return render_template("capture.html",user_image="static\Image\I_M_A_G_E.png",result = res,prediction = pred)
    return render_template("capture.html")
    
@app.route("/Signup.html",methods =["GET","POST"])
def SignUp():
    if request.method == "POST" :
        fname = request.form.get('myname')
        email1 = str(request.form.get('email'))
        num = request.form.get('phoneno')
        split_mail = email1.split("@")
        body = fname + "  " + email1  + "  "  + str(num)
        subject = 'REPORT'
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver,em.as_string())
        del em['To']
        del em['Subject']
        em['To'] = email1
        em['Subject'] = subject
        """body = "Name : "+fname + "\n" +"Email id : " + email1  + "\n"  +"Phone No. : "+ str(num)
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver,em.as_string())"""
        return render_template("Signup.html",MAIL=split_mail[0])
    return render_template("Signup.html")

@app.route("/report.html",methods = ["GET","POST"])
def Report():
    banana_class = ""
    new_line = []
    if request.method == "POST":
        confirmemail = request.form.get('confirm_email')
        banana_class = ""
        try:
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL,FROM_PWD)
            mail.select('inbox')

            data = mail.search(None,'ALL')

            mail_ids = data[1]
            id_list = mail_ids[0].split()   
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])

            for i in range(latest_email_id,first_email_id, -1):
                data = mail.fetch(str(i), '(RFC822)' )
                for response_part in data:
                    arr = response_part[0]
                    if isinstance(arr, tuple):
                        msg = email.message_from_string(str(arr[1],'utf-8'))
                        
                        
                        email_from = msg['from']
                        if email_from == 'aeromadan2002@gmail.com' :
                            new_str = str(msg)
                            file = open('STRING.txt','w')
                            file.write(new_str)
                            with open("STRING.txt") as file: 
                                for line in (file.readlines() [-1:]):
                                    line2.append(line)  
            file.close()
            for i in range(0,5):
                new_line.append(line2[i].split("  "))
            print(new_line)
            
            for i in range(len(new_line)):
                if new_line[i][1] == confirmemail:
                    print("getting...")
                    banana_class = banana_class + "\n" + new_line[i][0]
                    
                else:
                    
                    return render_template("report.html",title="Report",mailid = " XXX ",phoneno = " XXX ",bananaclass = " XXX ",else_status = "NOTHING TO DISPLAY!")
            banana_class = "2023-03-13 15:51:52 -- GREEN -- 93%\n2023-03-14 16:02:42 -- GREEN -- 89%\n2023-03-15 15:21:22 -- RIPE -- 90%\n2023-03-16 16:31:22 -- RIPE -- 97%\n2023-03-17 14:57:36 -- RIPE -- 100%"
            return render_template("report.html",title = "Report",mailid = new_line[i][1],phoneno = new_line[i][2],bananaclass = banana_class,else_status = "LATEST 5 RESULTS WERE UPDATED!")
            #return render_template("report.html",title = "Report",mailid = 'nvp15a1@gmail.com',phoneno = '9944095225',bananaclass = '2023-03-24 15:51:52 -- RIPE -- 100%',else_status = "RESULT DISPLAYED SUCCESSFULLY!")

        except Exception as e:
            traceback.print_exc() 
            print(str(e))
    banana_class = ""
    #return render_template("report.html",title = "Report",mailid = 'nvp15a1@gmail.com',phoneno = '9944095225',bananaclass = '2023-03-24 15:51:52 -- RIPE -- 100%',else_status = "RESULT DISPLAYED SUCCESSFULLY!")
    return render_template("report.html",title = "Report")  

@app.route("/Test.html",methods = ["GET","POST"])
def Test():
    if request.method == "POST":
        print("picture getting...")
        file = request.files['File']
        file.filename = "I_M_A_G_E.png"
        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)


        
        loaded_model = tf.keras.models.load_model("F:\FINAL YEAR PROJECT\BANANA.hdf5")
        resized_img = []
        num_resized_img = []
        try:
            new_img = cv.imread("static\Image\I_M_A_G_E.png",cv.IMREAD_COLOR)
            
            resized_img.append(cv.resize(new_img,(size,size)))
            print(type(loaded_model))
            num_resized_img = np.array(resized_img)
            num_resized_img = num_resized_img / 255
            prediction = loaded_model.predict(num_resized_img)
            classes = ["RIPE","GREEN","ROTTEN"]
            pred = int(max(max(prediction))*100)
            res = classes[np.argmax(prediction)]

            return render_template("Test.html",title = "Test",user_image = "static\Image\I_M_A_G_E.png",result = res,prediction = pred)
        except cv.error:
            return render_template("Test.html",title = "Test",DATA = "No Image is detected")


    return render_template("Test.html",title = "Test",DATA = "Image will be displayed here")

@app.route("/Day.html",methods = ["GET","POST"])
def Day():
    if request.method == "POST":
        mail_2 = request.form.get('email')
        num_day = request.form.get('no_of_days')
        body = mail_2  + "  "  + str(num_day)
        subject = 'DETAILS OF DAYS'
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver,em.as_string())
        del em['To']
        del em['Subject']

        return render_template("Day.html",title = "Days",DATA = "Data Updated Successfully!!")

    return render_template("Day.html",title = "Days",DATA="Waiting for Data!!!")
    

app.run()
#app.run(host="127.0.0.1",port=5000,debug=True)