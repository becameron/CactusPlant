import smtplib, ssl, os
from email.message import EmailMessage



# https://www.youtube.com/watch?v=JRCJ6RtE3xU
def emailNotification(body):
    port = 465
    stmp_server = 'smtp.gmail.com'
    receiver_email = os.environ.get('EMAIL_RECEIVER')
    sender_email = os.environ.get('EMAIL_USER')
    password = os.environ.get('EMAIL_PASS')
    contacts = [receiver_email,sender_email]

    message = f'Subject: New Products and Price Changes!\n\n{body}'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(stmp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email,receiver_email,message)
