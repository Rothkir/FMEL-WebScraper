import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_email(image_path):
    sender_email = "YOUR_DISPOSABLE_EMAIL_ACCOUNT_ADDRESS"
    password = "PASSWORD_FOR_SENDER_EMAIL"
    receiver_email = "YOUR_EMAIL_ADDRESS"
    subject = "An appartement has popped up!" 

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the image
    with open(image_path, 'rb') as file:
        img = MIMEImage(file.read())
        img.add_header('Content-Disposition', 'attachment', filename=image_path)
        msg.attach(img)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Replace with your SMTP provider
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()