from .api import specification


class CQiStatus:
    ''' A base class from which all other status inherit. '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = None


class StatusOk(CQiStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.STATUS_OK


class StatusConnectOk(CQiStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.STATUS_CONNECT_OK


class StatusByeOk(CQiStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.STATUS_BYE_OK


class StatusPingOk(CQiStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.STATUS_PING_OK


lookup = {
    specification.STATUS_OK: StatusOk,
    specification.STATUS_CONNECT_OK: StatusConnectOk,
    specification.STATUS_BYE_OK: StatusByeOk,
    specification.STATUS_PING_OK: StatusPingOk
}
