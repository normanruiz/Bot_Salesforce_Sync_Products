from Modelo.Terminal import Terminal
from Servicio.ConexionDBSQLServer import ConexionDBSQLServer


class ServiciosAter:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self._terminales = {}

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

    def buscarterminales(self):
        estado = True
        try:
            mensaje = f"Recuperando datos de Ater..."
            self.log.escribir(mensaje)

            datos_conexion = self.configuracion.conexiones[0]
            conexion = ConexionDBSQLServer(self.log)
            conexion.conectar(datos_conexion.driver, datos_conexion.server,
                              datos_conexion.database, datos_conexion.username,
                              datos_conexion.password)
            dataset_origen = conexion.ejecutar_select(datos_conexion.select)
            conexion.desconectar()
            if len(dataset_origen) == 0:
                raise Exception('La tabla de origen se encuentra vacia o no se encontraron registros.')
            for registro in dataset_origen:
                terminal = Terminal()
                terminal.numero = registro[0]
                self.terminales[terminal.numero] = terminal
            mensaje = f"Registros recuperados: {len(self.terminales)}"
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
                return self.terminales