from typing import List
from ..services import create_deny, get_allow, delete_deny, get_deny
from ..utils import is_ipv4_address


def deny(ips):
    invalid_ips = list(filter(lambda x: not is_ipv4_address(x), ips))
    if invalid_ips:
        print(f"Invalid ip address(es): {', '.join(invalid_ips)} ")
        return
    ips = set(ips)
    allowed = set(get_allow())
    currently_denied = set(get_deny())
    if ips & allowed:
        print(
            "Plese lift allow before denying the following: ", ", ".join(ips & allowed)
        )
    to_deny: List = list(ips - allowed - currently_denied)
    if to_deny:
        return create_deny(to_deny)


def lift_deny(ips):
    return delete_deny(list(ips))
