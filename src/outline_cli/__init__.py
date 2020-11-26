from outline_cli.outline import OutlineVPN

from .helper import (
    execute_method,
    get_config_from_app_ini,
    get_method_arguments,
    get_method_user_want_to_call,
    get_public_methods,
    get_outline_servers_config,
    get_outline_server_user_want_to_use,
)


def init_outline(section):
    return OutlineVPN(
        certSha256=get_config_from_app_ini(section, "certSha256"),
        apiUrl=get_config_from_app_ini(section, "apiUrl"),
    )


def init_cli():
    outline_servers = get_outline_servers_config()
    outline_client = init_outline(
        section=outline_servers[0]
        if len(outline_servers) == 1
        else get_outline_server_user_want_to_use(outline_servers)
    )
    return outline_client, get_public_methods(outline_client)


def start_cli():
    outline_client, outline_methods = init_cli()
    method_user_want_to_call = get_method_user_want_to_call(outline_methods)

    method_arguments = get_method_arguments(outline_client, method_user_want_to_call)
    execute_method(outline_client, method_user_want_to_call, method_arguments)
