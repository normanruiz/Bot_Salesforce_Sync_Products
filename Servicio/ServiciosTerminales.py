from Modelo.Terminal import Terminal
from Servicio.ConexionDBSQLite import ConexionDBSQLite


class ServiciosTerminales:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self._terminales = {}
        self._datos_ater = {}
        self._datos_locales = {}
        self._datos_salesforce = {}

    @property
    def log(self):
        return self._log

    @property
    def configuracion(self):
        return self._configuracion

    @property
    def terminales(self):
        return self._terminales

    @terminales.setter
    def terminales(self, terminales):
        self._terminales = terminales

    @property
    def datos_ater(self):
        return self._datos_ater

    @datos_ater.setter
    def datos_ater(self, datos_ater):
        self._datos_ater = datos_ater

    @property
    def datos_locales(self):
        return self._datos_locales

    @datos_locales.setter
    def datos_locales(self, datos_locales):
        self._datos_locales = datos_locales

    @property
    def datos_salesforce(self):
        return self._datos_salesforce

    @datos_salesforce.setter
    def datos_salesforce(self, datos_salesforce):
        self._datos_salesforce = datos_salesforce

    def buscarterminales(self):
        estado = True
        try:
            mensaje = f"Recuperando datos de locales..."
            self.log.escribir(mensaje)

            conexion = ConexionDBSQLite(self.log)
            conexion.conectar()
            dataset_origen = conexion.ejecutar_select()
            conexion.desconectar()
            for registro in dataset_origen:
                terminal = Terminal()
                terminal.numero = registro[0]
                terminal.fecha_actualizacion = registro[0]
                self._datos_locales[terminal.numero] = terminal
            mensaje = f"Registros recuperados: {len(self.datos_locales)}"
            self.log.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Recuperando datos de Ater: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            if estado is False:
                return False
            else:
                return self.datos_locales

    def procesar(self, datos_ater):
        estado = True
        self.datos_ater = datos_ater
        try:
            mensaje = f"Procesando terminales..."
            self.log.escribir(mensaje)

            self.terminales = self.datos_ater

            for key in self.datos_locales:
                self.terminales.pop(key, None)

            mensaje = f"Registros para actualizar: {len(self.terminales)}"
            self.log.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Procesando termianles: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            if estado is False:
                return False
            else:
                return self.terminales

    def registrar(self, terminales_salesforce_ok):
        estado = True
        registros = []
        try:
            mensaje = f"Almacenado terminales sincronizadas..."
            self.log.escribir(mensaje)
            if len(terminales_salesforce_ok) > 0:
                for numero in terminales_salesforce_ok:
                    terminal = Terminal(numero=numero)
                    registros.append(terminal.to_tuple())
                conexion = ConexionDBSQLite(self.log)
                conexion.conectar()
                conexion.ejecutar_insert(registros)
                conexion.desconectar()
            else:
                mensaje = f"Lote vacio, no hay terminales para actualizar..."
                self.log.escribir(mensaje)

            mensaje = f"Registros insertados: {len(terminales_salesforce_ok)}"
            self.log.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Almacenado terminales sincronizadas: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            if estado is False:
                return False
            else:
                return estado