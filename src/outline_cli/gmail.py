import smtplib


class Gmail:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.init_server()

    def init_server(self):
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.__ehlo()
        self.__login()

    def __ehlo(self):
        self.server.ehlo()

    def __login(self):
        self.server.login(self.user, self.password)

    def send(self, msg):
        self.server.send_message(msg)

    def quit(self):
        self.server.quit()
