from .base import BaseStatusFollower, BaseStatus
from .status import AcceptedOrFailedPassword

class AcceptedOrFailedStatusFollower(BaseStatusFollower):
    status_class: BaseStatus = AcceptedOrFailedPassword()

