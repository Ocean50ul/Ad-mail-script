import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from avito_offers import links_to_mail
from secret import password, sender, receiver


def message_builder(lst):
    if len(lst) == 1 and lst[0] == 'Сегодня ничего нет!':
        message = """<html><body><h1>Сегодня ничего нет!</h1></body></html>"""
    else:
        message = f"""\
        <html>
            <body>
                <p>Привет! Сегодня я нашел следующие объекты:</p>
                <ol>
                """
        for item in lst:
            message = message + f"<li> <a href='{item}'>{item}</a> </li>"

        message = message + """</ol></body></html>"""
    return message


smtp_server = "smtp.gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "Объявления на АВИТО"
message["From"] = sender
message["To"] = receiver

print('Preparing message..')
html = message_builder(links_to_mail())
body = MIMEText(html, "html")
message.attach(body)

port = 465

context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login("montybazf@gmail.com", password)
    server.sendmail(
        sender, receiver, message.as_string()
    )

print('E-mail sent!')
