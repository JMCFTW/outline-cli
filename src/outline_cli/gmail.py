import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Gmail:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.init_server()
        self.init_message()

    def init_server(self):
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.__ehlo()
        self.__login()

    def init_message(self):
        self.message = MIMEMultipart()

    def __ehlo(self):
        self.server.ehlo()

    def __login(self):
        self.server.login(self.user, self.password)

    def send(self):
        self.server.send_message(self.message)

    def quit(self):
        self.server.quit()

    def draft(self, to_email, message, subject="VPN 開通"):
        self.message["Subject"] = subject
        self.message["From"] = self.user
        self.message["To"] = to_email
        self.message.preamble = "Multipart massage.\n"
        part = MIMEText(message)
        self.message.attach(part)
