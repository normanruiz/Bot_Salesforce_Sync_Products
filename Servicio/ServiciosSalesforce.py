from Modelo.ApiSalesforce import ApiSalesforce
from Servicio.ConexionAPISalesforce import ConexionAPISalesforce


class ServiciosSalesforce:
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

    def sincronizar(self, terminales):
        self.terminales = terminales
        datos_respuesta = (True, [], [])
        try:
            mensaje = f"Actualizando producto a terminales con estado 4 y 12..."
            self.log.escribir(mensaje)

            if len(self.terminales) > 0:
                datos_api = self.configuracion.conexiones[1]
                file_datos_csv = 'Externalid__c,Name,Product2Id\n'
                for numero, terminal in self.terminales.items():
                    file_datos_csv += f"{terminal.numero},{datos_api.name},{datos_api.product2id}\n"
                api_salesforce = ConexionAPISalesforce(self.log)
                api_salesforce.autenticarse(datos_api)
                datos_respuesta = api_salesforce.actualizar(file_datos_csv)
            else:
                mensaje = f"Lote vacio, no hay terminales para actualizar..."
                self.log.escribir(mensaje)

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            datos_respuesta = (False, [], [])
            mensaje = f"Error - Actualizando producto a terminales con estado 4 y 12: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
            return datos_respuesta
