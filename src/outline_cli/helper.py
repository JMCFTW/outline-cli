import configparser
import pkgutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from outline_cli.gmail import Gmail

config = configparser.ConfigParser()
config.read("app.ini", encoding="utf-8")


def get_config_from_app_ini(section_name, key):
    return config.get(section_name, key)


def get_email_list_from_file(filename):
    with open(filename, "r") as file:
        return [email.strip() for email in file.readlines()]


def get_username_by_email(email):
    # NOTE: first_name.last_name@gmail.com
    return " ".join([c.capitalize() for c in email.split("@")[0].split(".")])


def send_email(email, username, accessUrl):
    gmail_user = get_config_from_app_ini("Gmail", "EMAIL")
    gmail_password = get_config_from_app_ini("Gmail", "APP_PASSWORD")

    msg = MIMEMultipart()
    msg["Subject"] = "VPN 開通"
    msg["From"] = gmail_user
    msg["To"] = email
    msg.preamble = "Multipart massage.\n"

    part = MIMEText(
        pkgutil.get_data(__package__, "templates/mail_template.txt")
        .decode()
        .format(username=username, accessUrl=accessUrl)
    )
    msg.attach(part)

    gmail = Gmail(gmail_user, gmail_password)
    gmail.send(msg)
    gmail.quit()

    print(f"Email sent to {email}")
