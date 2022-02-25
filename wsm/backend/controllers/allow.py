from typing import List, Optional, Set
from ..services import get_deny, create_allow, delete_allow, get_allow
from ..utils import is_ipv4_address


def allow(ips: List) -> Optional[List]:
    invalid_ips: List = list(filter(lambda x: not is_ipv4_address(x), ips))
    if invalid_ips:
        print(f"Invalid ip address(es): {', '.join(invalid_ips)} ")
        return
    ips: Set = set(ips)
    denied: Set = set(get_deny())
    if ips & denied:
        print(
            "Plese lift deny before allowing the following: ", ", ".join(ips & denied)
        )
    currently_allowed: Set = set(get_allow())
    to_allow: List = list(ips - denied - currently_allowed)

    if to_allow:
        return create_allow(to_allow)


def lift_allow(ips: List) -> List:
    return delete_allow(ips)
