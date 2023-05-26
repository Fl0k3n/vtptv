from typing import Callable

CONFIRMATION_PROMPT = 'Enter "y" when ready.\n>'
YES_OPTIONS = ['y', 'yes']


def require_router_console_connected(router_name: str):
    require_confirmation(
        f'Console port of router {router_name} must be connected to proceed.', CONFIRMATION_PROMPT)


def require_router_netconf_port_connected(router_name: str, interface_name: str):
    require_confirmation(
        f'Netconf port {interface_name} of router {router_name} must be connected to proceed.',
        CONFIRMATION_PROMPT)


def require_confirmation(info: str, prompt: str, retries: str = 0,
                         confirmation_predicte: Callable[[
                             str], bool] = lambda input: input.strip().lower() in YES_OPTIONS,
                         on_failure: Callable[[str], None] = lambda _: terminate()) -> None:
    user_input = None
    for _ in range(retries + 1):
        print(info)
        user_input = input(prompt)
        if confirmation_predicte(user_input):
            return

    on_failure(user_input)


def terminate(info: str = 'Terminating.'):
    print(info)
    exit(1)
