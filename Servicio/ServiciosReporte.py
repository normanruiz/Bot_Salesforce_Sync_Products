from datetime import date
import time
import os
from email.message import EmailMessage
import smtplib


class ServiciosReporte:
    def __init__(self, log, configuracion):
        self._log = log
        self._configuracion = configuracion
        self._archivo = None

    @property
    def log(self):
        return self._log

    @property
    def configuracion(self):
        return self._configuracion

    @property
    def archivo(self):
        return self._archivo

    @archivo.setter
    def archivo(self, archivo):
        self._archivo = archivo

    def generar_reporte(self, terminales_ok, terminales_fallidas):
        estado = True
        datos_conexion = self.configuracion.conexiones[2]
        file = f"Reporte-{date.today()}"
        try:
            mensaje = f"Generando reporte..."
            self.log.escribir(mensaje)

            with open(f"{file}.html", "w", encoding="utf8") as archivo:
                archivo.write(f"<!DOCTYPE html>\n")
                archivo.write(f"<html lang=\"en\">\n")
                archivo.write(f"<head>\n")
                archivo.write(f"\t<meta charset=\"UTF-8\">\n")
                archivo.write(f"\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
                archivo.write(f"\t<title>Reporte {date.today()}</title>\n")
    
                archivo.write("\t<style type=\"text/css\" media=\"screen\">\n")
                archivo.write("\t\tbody{background-color: white;margin: 10px 60px;padding: 10px 60px;}\n")
                archivo.write("\t\th1{margin: 20px;padding: 20px;border: 2px solid blue;border-radius: 6px;box-shadow: 6px 6px 10px black;text-decoration: underline;}\n")
                archivo.write("\t\th2{display: inline-block;margin: 10px 20px;padding: 10px 20px;border: 2px solid;border-radius: 6px;box-shadow: 6px 6px 10px black;}\n")
                archivo.write("\t\th2#ok{border-color: green;}\n")
                archivo.write("\t\th2#fail{border-color: red;}\n")
                archivo.write("\t\tp>i{margin: 10px 20px;padding: 10px 20px;}\n")
                archivo.write("\t\tp>b{margin: 10px 20px;padding: 10px 20px;}\n")
                archivo.write("\t\ttable{border: 2px solid lightgray;border-radius: 6px;margin: 10px 20px;padding: 10px 20px;border-spacing: 20px 10px;}\n")
                archivo.write("\t\ttd{padding: 6px 20px;border-radius: 4px;background-color: rgb(127,160,160);}\n")
                archivo.write("\t</style>\n")

                archivo.write(f"</head>\n")
                archivo.write(f"<body>\n")
                archivo.write(f"\t<h1>Reporte Bot Salesforce Sync Products</h1>\n")
                archivo.write(f"\t<p><i>Fecha: {date.today()} Hora: {time.strftime('%H:%M:%S', time.localtime())}</i></p>\n")
                archivo.write(f"\t<h2 id=\"ok\">Terminales sincronizadas: {len(terminales_ok)}</h2>\n")
                if len(terminales_ok) == 0:
                    archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
                else:
                    archivo.write(f"\t<table>\n")
                    archivo.write(f"\t\t<tbody>\n")
                    archivo.write(f"\t\t\t<tr>\n")
                    contador = 0
                    for numero in terminales_ok:
                        if contador < 5:
                            archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                            contador += 1
                        else:
                            archivo.write(f"\t\t\t</tr>\n")
                            contador = 1
                            archivo.write(f"\t\t\t<tr>\n")
                            archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                    else:
                        archivo.write(f"\t\t\t</tr>\n")
                    archivo.write(f"\t\t</tbody>\n")
                    archivo.write(f"\t</table>\n")
                archivo.write(f"\t<h2 id=\"fail\">Terminales con sincronizacion fallida: {len(terminales_fallidas)}</h2>\n")
                if len(terminales_fallidas) == 0:
                    archivo.write(f"\t<p><b>No se detectaron termianles en este estadio.</b></p>\n")
                else:
                    archivo.write(f"\t<table>\n")
                    archivo.write(f"\t\t<tbody>\n")
                    archivo.write(f"\t\t\t<tr>\n")
                    contador = 0
                    for numero in terminales_fallidas:
                        if contador < 5:
                            archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                            contador += 1
                        else:
                            archivo.write(f"\t\t\t</tr>\n")
                            contador = 1
                            archivo.write(f"\t\t\t<tr>\n")
                            archivo.write(f"\t\t\t\t<td>{numero}</td>\n")
                    else:
                        archivo.write(f"\t\t\t</tr>\n")
                    archivo.write(f"\t\t</tbody>\n")
                    archivo.write(f"\t</table>\n")
                archivo.write(f"</body>\n")
                archivo.write(f"</html>\n")

            asunto = datos_conexion.asunto
            remitente = datos_conexion.remitente
            destinatario = datos_conexion.destinatario
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = asunto
            with open(f"{file}.html", "rb") as f:
                email.add_attachment(
                    f.read(),
                    filename=f"{file}.html",
                    maintype="text",
                    subtype="html"
                )
            s = smtplib.SMTP(datos_conexion.ip, datos_conexion.port)
            s.send_message(email)
            s.quit()

            #os.remove(f"{archivo}.html")

            mensaje = f"Subproceso finalizado..."
            self.log.escribir(mensaje)
        except Exception as excepcion:
            estado = False
            mensaje = f"ERROR - Generando reporte: {type(excepcion)} {str(excepcion)}"
            self.log.escribir(mensaje)
        finally:
            return estado
