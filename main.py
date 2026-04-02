import time
import os
import sys
from src.scraper import JobScraper
from src.brain import JobHunterBrain
from src.notifier import JobNotifier

def ejecutar_cazador():
    print("\n" + "="*50)
    print("🏹 INICIANDO CAZA DE EMPLEO (MULTI-PLATAFORMA)")
    print(f"📅 Fecha: {time.strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*50)
    
    # 1. Inicialización de herramientas
    try:
        scraper = JobScraper()
        brain = JobHunterBrain()
        notificador = JobNotifier()
    except Exception as e:
        print(f"❌ Error al inicializar herramientas: {e}")
        return

    # 2. Rastreo de vacantes
    print("\n🔍 Rastreando vacantes en Get on Board, Indeed y CompuTrabajo...")
    empleos = scraper.buscar_todo("Full Stack Python") 
    
    if not empleos:
        print("📭 No se encontraron nuevos empleos en esta pasada.")
        return

    total_recolectados = len(empleos)
    print(f"✅ Se encontraron {total_recolectados} vacantes para filtrar.\n")

    # --- FILTRO DE RELEVANCIA PRE-IA ---
    palabras_no_deseadas = ["java", "qa", "tester", "angular", "golang", "ruby"]
    empleos_filtrados = []
    
    for emp in empleos:
        titulo_min = emp.get('titulo', '').lower()
        if not any(p in titulo_min for p in palabras_no_deseadas):
            empleos_filtrados.append(emp)
    
    total = len(empleos_filtrados)
    print(f"🎯 Tras el filtro inicial, quedan {total} avisos relevantes para analizar por IA.")

    # --- 🚀 NUEVA LÓGICA: LISTA PARA EL RESUMEN ---
    resultados_para_correo = []

    # 3. Bucle de análisis uno a uno
    for i, empleo in enumerate(empleos_filtrados, 1):
        titulo = empleo.get('titulo', 'Sin título')
        fuente = empleo.get('fuente', 'Desconocida')
        url_empleo = empleo.get('url', '#')

        print(f"[{i}/{total}] 🚀 Analizando en {fuente}: {titulo}...")
        
        try:
            resultado_json = brain.analyze_job(titulo, url_empleo) 
            
            porcentaje = resultado_json.get('porcentaje', 0)
            # Guardamos los datos necesarios para el correo
            resultado_json['titulo'] = titulo
            resultado_json['url'] = url_empleo

            print(f"📊 Puntaje de Match: {porcentaje}%")

            # 4. FILTRO DEL 80%
            if porcentaje >= 80:
                print(f"✨ ¡AÑADIDO AL RESUMEN! {porcentaje}% es ideal.")
                resultados_para_correo.append(resultado_json)
            else:
                print(f"⏭️ {porcentaje}% no es suficiente (mínimo 80%). Pasando al siguiente...")

        except Exception as e:
            print(f"⚠️ Error analizando este empleo: {e}")

        if i < total: 
            print(f"⚡ Procesando a máxima velocidad...")
            time.sleep(2)

    # --- 📧 ENVÍO DEL CORREO ÚNICO AL FINAL ---
    if resultados_para_correo:
        print(f"\n📧 Enviando resumen con {len(resultados_para_correo)} matches encontrados...")
        notificador.enviar_resumen_diario(resultados_para_correo)
    else:
        print("\n📭 No se encontraron matches sobre el 80%, no se envió correo.")

    print("\n" + "="*50)
    print("✅ CAZA FINALIZADA CON ÉXITO")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        ejecutar_cazador()
    except KeyboardInterrupt:
        print("\n\n👋 Caza interrumpida por el usuario. ¡Hasta la próxima!")
        sys.exit()