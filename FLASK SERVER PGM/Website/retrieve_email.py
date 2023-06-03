import smtplib
import time
import imaplib
import email
import traceback 
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
ORG_EMAIL = "@gmail.com" 
FROM_EMAIL = "finalyearpro833" + ORG_EMAIL 
FROM_PWD = "ohixtjgvxmyirfep" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993
global data
data = list()
def read_email_from_gmail():
    line1 = []
    line2 = []
    confim = "visshwapm@gmail.com"
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
                        email_subject = msg['subject']
                        new_str = str(msg);
                        file = open('Status.txt','w')
                        file.write(new_str)
                        with open("Status.txt") as file: 
                            for line in (file.readlines() [-1:]):
                                line1.append(line)
        
                        file.close()

        for i in range(len(line1)):
            data.append(line1[i].split("  "))
        print(data[0][1])
    except Exception as e:
        traceback.print_exc() 
        print(str(e))

read_email_from_gmail()
