import xmltodict
from Modelo.ApiSalesforce import ApiSalesforce
from Modelo.ApiTeams import ApiTeams
from Modelo.Autor import Autor
from Modelo.Bot import Bot
from Modelo.Conexion import Conexion


class Configuracion:
    def __init__(self, log):
        self._log = log
        self._configfile = 'config.xml'
        self._bot = None
        self._conexiones = []

    @property
    def log(self):
        return self._log

    @property
    def configfile(self):
        return self._configfile

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot

    @property
    def conexiones(self):
        return self._conexiones

    @conexiones.setter
    def conexiones(self, conexiones):
        self._conexiones = conexiones

    def cargar(self):
        try:
            mensaje = f"Cargando configuracion..."
            self.log.escribir(mensaje)
            with open(self._configfile, 'r', encoding='utf8') as xmlfile:
                xmlconfig = xmlfile.read()
                config = xmltodict.parse(xmlconfig)
            autor = Autor(config["parametros"]["bot"]["autor"]["nombre"],
                          config["parametros"]["bot"]["autor"]["correo"])
            bot = Bot(config["parametros"]["bot"]["nombre"],
                      True if config["parametros"]["bot"]["estado"] == 'True' else False,
                      int(config["parametros"]["bot"]["hilos"]), autor)
            self.bot = bot
            conexion_db = Conexion(config["parametros"]["conexiones_db"]["driver"],
                                   config["parametros"]["conexiones_db"]["server"],
                                   config["parametros"]["conexiones_db"]["database"],
                                   config["parametros"]["conexiones_db"]["username"],
                                   config["parametros"]["conexiones_db"]["password"],
                                   config["parametros"]["conexiones_db"]["select"])
            self.conexiones.append(conexion_db)
            api_salesforce = ApiSalesforce(config["parametros"]["api_salesforce"]["org"],
                                 config["parametros"]["api_salesforce"]["client_id"],
                                 config["parametros"]["api_salesforce"]["client_secret"],
                                 config["parametros"]["api_salesforce"]["username"],
                                 config["parametros"]["api_salesforce"]["password"],
                                 config["parametros"]["api_salesforce"]["version"],
                                 config["parametros"]["api_salesforce"]["select"])
            self.conexiones.append(api_salesforce)
            api_teams = ApiTeams(config["parametros"]["api_teams"]["subject"],
                                 config["parametros"]["api_teams"]["from"],
                                 config["parametros"]["api_teams"]["to"],
                                 config["parametros"]["api_teams"]["ip"],
                                 config["parametros"]["api_teams"]["port"])
            self.conexiones.append(api_teams)
            mensaje = f"Configuracion cargada correctamente..."
            self.log.escribir(mensaje)
            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            mensaje = f"ERROR - Cargando configuracion: {str(excepcion)}"
            self.log.escribir(mensaje)
            mensaje = f"WARNING!!! - Subproceso interrumpido..."
            self.log.escribir(mensaje)
        finally:
            mensaje = f" {'-' * 128}"
            self.log.escribir(mensaje, tiempo=False)
