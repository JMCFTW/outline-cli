from inspect import getfullargspec

from PyInquirer import prompt

from outline_cli.helper import get_config_from_app_ini
from outline_cli.outline import OutlineVPN


def init_outline():
    client = OutlineVPN(
        certSha256=get_config_from_app_ini("OutlineVPN", "certSha256"),
        apiUrl=get_config_from_app_ini("OutlineVPN", "apiUrl"),
    )
    method_list = [
        f for f in dir(client) if callable(getattr(client, f)) and not f.startswith("_")
    ]
    return client, method_list


def init_cli():
    client, method_list = init_outline()
    method = prompt(
        [
            {
                "type": "list",
                "name": "method",
                "message": "Please choose which method you want to call? ",
                "choices": method_list,
            }
        ]
    )["method"]

    method_arguments = getfullargspec(getattr(client, method)).args
    method_arguments.pop(0)  # NOTE: Pop 'self'
    if len(method_arguments) > 0:
        print(
            getattr(client, method)(
                **prompt(
                    [
                        {"type": "input", "name": arg, "message": f"{arg} :"}
                        for arg in method_arguments
                    ]
                )
            )
        )
    else:
        print(getattr(client, method)())
