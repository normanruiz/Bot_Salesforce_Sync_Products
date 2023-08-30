import sqlite3
from datetime import date
import time


class ConexionDBSQLite:
    def __init__(self, log):
        self._log = log
        self._conexion = None
        self._cursor = None
        self._database = None
        self._tabla = 'terminales'

    @property
    def log(self):
        return self._log

    @property
    def conexion(self):
        return self._conexion

    @conexion.setter
    def conexion(self, conexion):
        self._conexion = conexion

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = cursor

    @property
    def tabla(self):
        return self._tabla

    @tabla.setter
    def tabla(self, tabla):
        self._tabla = tabla

    def conectar(self):
        estado = True
        self.database = 'local_db'
        try:
            mensaje = f"Conectando a base de datos {self.database}..."
            self.log.escribir(mensaje)

            self.conexion = sqlite3.connect(f"{self.database}.db")

            mensaje = f"Conexion establecida con base de datos {self.database}..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Conectando a base de datos {self.database}: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

    def desconectar(self):
        estado = True
        try:
            mensaje = f"Cerrando conexion con base de datos {self.database}..."
            self.log.escribir(mensaje)

            self.conexion.close()

            mensaje = f"Conexion a base de datos {self.database} cerrada..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Cerrando conexion a base de datos {self.database}: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

    def validar_tabla(self):
        estado = True
        sql_verificador = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.tabla}';"
        try:
            mensaje = f"Verificando datos locales..."
            self.log.escribir(mensaje)
            mensaje = f"Generando cursor..."
            self.log.escribir(mensaje)
            self.cursor = self.conexion.cursor()
            mensaje = f"Comenzando lectura de datos..."
            self.log.escribir(mensaje)

            self.cursor.execute(sql_verificador)
            if self.cursor.fetchone() is None:
                self.cursor.execute(f'''CREATE TABLE {self.tabla} (terminal text, fecha_actualizacion text)''')

            mensaje = f"Datos locales verificados correctamente..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Verificando datos locales {self.database}: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado

    def ejecutar_select(self):
        estado = True
        consulta = f"SELECT terminal, fecha_actualizacion FROM {self.tabla}"
        data = []
        try:
            mensaje = f"Ejecutando query contra {self.database}..."
            self.log.escribir(mensaje)

            self.validar_tabla()

            mensaje = f"Query: {consulta}"
            self.log.escribir(mensaje)
            mensaje = f"Comenzando lectura de datos..."
            self.log.escribir(mensaje)

            self.cursor.execute(consulta)
            data = self.cursor.fetchall()

            mensaje = f"Lectura de datos finalizada..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Ejecutando query: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return data if estado else estado

    def ejecutar_insert(self, registros):
        estado = True
        insert = f"INSERT INTO {self.tabla} VALUES (?, '{str(date.today())} {time.strftime('%H:%M:%S', time.localtime())}')"
        cursor = None

        try:
            mensaje = f"Ejecutando insert contra {self.database}..."
            self.log.escribir(mensaje)
            mensaje = f"Query: {insert}"
            self.log.escribir(mensaje)
            mensaje = f"Generando cursor..."
            self.log.escribir(mensaje)
            cursor = self.conexion.cursor()
            mensaje = f"Comenzando escritura de datos..."
            self.log.escribir(mensaje)

            cursor.executemany(insert, registros)
            self.conexion.commit()

            mensaje = f"Escritura de datos finalizada..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Ejecutando insert: {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            if cursor:
                cursor.close()
                mensaje = f"Destruyendo cursor..."
                self.log.escribir(mensaje)
            return estado

