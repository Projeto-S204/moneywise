import smtplib
from email.mime.text import MIMEText

def enviar_email(destinatario, assunto, corpo):
    remetente = 'suportemw011@gmail.com'
    senha = 'krofvxeymfmvsjwx'

    msg = MIMEText(corpo, 'html')
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
