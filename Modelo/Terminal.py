class Terminal:
    def __init__(self, numero=None, fecha_actualizacion=None):
        self._numero = numero
        self._fecha_actualizacion = fecha_actualizacion

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def fecha_actualizacion(self):
        return self._fecha_actualizacion

    @fecha_actualizacion.setter
    def fecha_actualizacion(self, fecha_actualizacion):
        self._fecha_actualizacion = fecha_actualizacion

    def to_update_ater(self):
        return ('Classic', self.numero)
