from outline_cli.outline import OutlineVPN

from .helper import (
    execute_method,
    get_config_from_app_ini,
    get_method_arguments,
    get_method_user_want_to_call,
    get_public_methods,
)


def init_outline():
    return OutlineVPN(
        certSha256=get_config_from_app_ini("OutlineVPN", "certSha256"),
        apiUrl=get_config_from_app_ini("OutlineVPN", "apiUrl"),
    )


def init_cli():
    outline_client = init_outline()
    return outline_client, get_public_methods(outline_client)


def start_cli():
    outline_client, outline_methods = init_cli()
    method_user_want_to_call = get_method_user_want_to_call(outline_methods)

    method_arguments = get_method_arguments(outline_client, method_user_want_to_call)
    execute_method(outline_client, method_user_want_to_call, method_arguments)
