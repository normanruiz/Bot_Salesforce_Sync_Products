class ApiTeams:
    def __init__(self, asunto=None, remitente=None, destinatario=None, ip=None, port=None):
        self._asunto = asunto
        self._remitente = remitente
        self._destinatario = destinatario
        self._ip = ip
        self._port = port

    @property
    def asunto(self):
        return self._asunto

    @asunto.setter
    def asunto(self, asunto):
        self._asunto = asunto

    @property
    def remitente(self):
        return self._remitente

    @remitente.setter
    def remitente(self, remitente):
        self._remitente = remitente

    @property
    def destinatario(self):
        return self._destinatario

    @destinatario.setter
    def destinatario(self, destinatario):
        self._destinatario = destinatario

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