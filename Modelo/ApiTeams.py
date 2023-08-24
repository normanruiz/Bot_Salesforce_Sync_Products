class ApiTeams:
    def __init__(self, subject=None, de=None, to=None, ip=None, port=None):
        self._subject = subject
        self._de = de
        self._to = to
        self._ip = ip
        self._port = port

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        self._subject = subject

    @property
    def de(self):
        return self._de

    @de.setter
    def de(self, de):
        self._de = de

    @property
    def to(self):
        return self.to

    @to.setter
    def to(self, to):
        self._to = to

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, ip):
        self._ip = ip

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port