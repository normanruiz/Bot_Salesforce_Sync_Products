from Servicio.Log import Log
from Servicio.Configuracion import Configuracion


class Bot:
    def __init__(self):
        self._estado = True
        self._log = None
        self._configuracion = None

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        self._log = log

    @property
    def configuracion(self):
        return self._configuracion

    @configuracion.setter
    def configuracion(self, configuracion):
        self._configuracion = configuracion

    def iniciar(self):
        status_code = 0
        self.log = Log()
        try:
            self.log.verificar_archivo_log()
            mensaje = f" {'='*128 }"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"Iniciando Bot Salesforce Sync Products..."
            self.log.escribir(mensaje)
            mensaje = f" {'~'*128 }"
            self.log.escribir(mensaje, tiempo=False)

            configuracion = Configuracion(self.log)
            configuracion.cargar()
            self.configuracion = configuracion
            self.estado = self.configuracion.bot.estado
            if not self.estado:
                mensaje = f"Bot apagado por configuracion..."
                self.log.escribir(mensaje)
                return

        except Exception as excepcion:
            status_code = 1
            mensaje = f" {'-'*128 }"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"ERROR - Ejecucion principal: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            if not self.estado:
                mensaje = f" {'-' * 128}"
                self.log.escribir(mensaje, tiempo=False)
                mensaje = f"WARNING!!! - Proceso principal interrumpido, no se realizaran mas acciones..."
                self.log.escribir(mensaje)

            mensaje = f" {'~' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"Finalizando Bot Salesforce Sync State..."
            self.log.escribir(mensaje)
            mensaje = f" {'='*128 }"
            self.log.escribir(mensaje, tiempo=False)
            self.log.cerrar()
            return status_code
