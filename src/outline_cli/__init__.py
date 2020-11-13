from helper import (
    execute_method,
    get_method_arguments,
    get_method_user_want_to_call,
    init_cli,
)


def start_cli():
    outline_client, outline_methods = init_cli()
    method_user_want_to_call = get_method_user_want_to_call(outline_methods)

    method_arguments = get_method_arguments(outline_client, method_user_want_to_call)
    execute_method(outline_client, method_user_want_to_call, method_arguments)
