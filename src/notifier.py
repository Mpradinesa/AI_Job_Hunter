import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class JobNotifier:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        self.destinatario = os.getenv("EMAIL_RECEIVER")

    def enviar_resumen_diario(self, lista_resultados):
        """
        Recibe una lista de diccionarios con los resultados de la IA.
        """
        if not lista_resultados:
            print("📭 No hay avisos relevantes para enviar.")
            return

        msg = MIMEMultipart("alternative")
        msg['From'] = f"Tu Asistente IA <{self.email_user}>"
        msg['To'] = self.destinatario
        msg['Subject'] = f"💼 Resumen de Empleos: {len(lista_resultados)} Vacantes Encontradas"

        # Construimos el HTML de cada aviso para el cuerpo del correo
        bloques_empleos = ""
        for item in lista_resultados:
            argumentos = "".join([f"<li>✅ {arg}</li>" for arg in item['argumentos_ganadores']])
            
            bloques_empleos += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 8px; background-color: #fcfcfc;">
                <h3 style="color: #1a73e8; margin-top: 0;">{item['titulo']} ({item['porcentaje']}% Match)</h3>
                <p><strong>Análisis:</strong> {item['analisis']}</p>
                <p><strong>💡 Torpedo para postular:</strong></p>
                <ul style="font-size: 0.9em;">{argumentos}</ul>
                <p style="color: #d32f2f; font-size: 0.9em;">⚠️ <strong>Ojo:</strong> {item['advertencia']}</p>
                <a href="{item['url']}" style="color: #1a73e8; font-weight: bold;">Ver aviso y postular ↗️</a>
            </div>
            """

        html_final = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333; max-width: 700px; margin: auto;">
            <h2 style="text-align: center; color: #2e7d32;">🚀 Reporte Diario de Caza de Empleos</h2>
            <p>Hola Moni, aquí tienes el resumen de las mejores oportunidades de hoy:</p>
            {bloques_empleos}
            <p style="text-align: center; font-size: 0.8em; color: #888; border-top: 1px solid #eee; padding-top: 20px;">
                Cazador de Empleos IA - 2026 🏹
            </p>
          </body>
        </html>
        """

        msg.attach(MIMEText(html_final, 'html'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_user, self.email_pass)
                server.send_message(msg)
            print(f"📧 ¡Resumen enviado con éxito con {len(lista_resultados)} avisos!")
        except Exception as e:
            print(f"❌ Error al enviar el resumen: {e}")