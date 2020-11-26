import configparser
import pkgutil
from inspect import getfullargspec

from PyInquirer import prompt

from outline_cli.gmail import Gmail

config = configparser.ConfigParser()
config.read("app.ini", encoding="utf-8")


def get_outline_servers_config():
    return [c for c in config.sections() if "OutlineVPN" in c]


def get_config_from_app_ini(section_name, key):
    return config.get(section_name, key)


def get_public_methods(instance):
    return [
        method
        for method in dir(instance)
        if callable(getattr(instance, method)) and not method.startswith("_")
    ]


def get_outline_server_user_want_to_use(outline_servers):
    return prompt(
        [
            {
                "type": "list",
                "name": "outline_server",
                "message": "Please choose which outline server you want to use? ",
                "choices": outline_servers,
            }
        ]
    )["outline_server"]


def get_method_user_want_to_call(methods):
    return prompt(
        [
            {
                "type": "list",
                "name": "method",
                "message": "Please choose which method you want to call? ",
                "choices": methods,
            }
        ]
    )["method"]


def get_method_arguments(instance, method):
    method_arguments = getfullargspec(getattr(instance, method)).args
    method_arguments.pop(0)  # NOTE: Pop 'self'
    return method_arguments


def execute_method(outline_client, method_user_want_to_call, method_arguments):
    if len(method_arguments) > 0:
        print(
            getattr(outline_client, method_user_want_to_call)(
                **prompt(
                    [
                        {"type": "input", "name": arg, "message": f"{arg} :"}
                        for arg in method_arguments
                    ]
                )
            )
        )
    else:
        print(getattr(outline_client, method_user_want_to_call)())


def get_email_list_from_file(filename):
    with open(filename, "r") as file:
        return [email.strip() for email in file.readlines()]


def get_username_by_email(email):
    # NOTE: first_name.last_name@gmail.com
    return " ".join([c.capitalize() for c in email.split("@")[0].split(".")])


def send_email(email, username, accessUrl):
    gmail_user = get_config_from_app_ini("Gmail", "EMAIL")
    gmail_password = get_config_from_app_ini("Gmail", "APP_PASSWORD")

    gmail = Gmail(gmail_user, gmail_password)
    gmail.draft(
        to_email=email,
        message=pkgutil.get_data(__package__, "templates/mail_template.txt")
        .decode()
        .format(username=username, accessUrl=accessUrl),
    )
    gmail.send()
    gmail.quit()

    print(f"Email sent to {email}")
