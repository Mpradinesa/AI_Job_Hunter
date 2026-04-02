import cloudscraper
from bs4 import BeautifulSoup
import time
from datetime import datetime

class JobScraper:
    def __init__(self):
        self.base_url_gob = "https://www.getonbrd.com"
        # Mantenemos cloudscraper para evitar bloqueos
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )

    def buscar_getonboard(self, query="full-stack"):
        """Busca en Get on Board Chile (Top 15 y < 7 días)"""
        url = f"{self.base_url_gob}/jobs-{query}-in-chile"
        print(f"🔍 Cazando en Get on Board: {url}...")
        
        try:
            response = self.scraper.get(url)
            if response.status_code != 200: return []

            soup = BeautifulSoup(response.text, 'html.parser')
            avisos = []

            # Get on Board usa etiquetas de tiempo legibles
            for item in soup.find_all('a', class_='gb-results-list__item'):
                if len(avisos) >= 15: break # Límite de 15

                # Filtro de fecha: Si dice "month" o "2 weeks", saltamos.
                fecha_el = item.find('span', class_='date')
                fecha_texto = fecha_el.get_text(strip=True).lower() if fecha_el else ""
                
                if any(x in fecha_texto for x in ["month", "mes", "2 weeks", "2 semanas", "3 weeks"]):
                    continue

                titulo = item.find('strong').get_text(strip=True)
                link = item['href']
                avisos.append({
                    "titulo": titulo,
                    "url": link,
                    "fuente": "Get on Board"
                })
            return avisos
        except Exception as e:
            print(f"Error en Get on Board: {e}")
            return []

    def buscar_indeed(self, cargo="Full Stack"):
        """Busca en Indeed Chile (Top 15 y últimos 7 días via URL)"""
        query = cargo.replace(" ", "+")
        # 'fromage=7' le dice a Indeed que solo queremos lo de la última semana
        url = f"https://cl.indeed.com/jobs?q={query}&l=Chile&sort=date&fromage=7"
        print(f"🔍 Cazando en Indeed Chile: {url}...")
        
        try:
            response = self.scraper.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            avisos = []

            for card in soup.select('.job_seen_beacon'):
                if len(avisos) >= 15: break

                titulo_el = card.select_one('.jobTitle')
                link_el = card.select_one('a[handle]') or card.select_one('a')
                
                if titulo_el and link_el:
                    titulo = titulo_el.get_text(strip=True)
                    link = "https://cl.indeed.com" + link_el['href']
                    avisos.append({
                        "titulo": titulo,
                        "url": link,
                        "fuente": "Indeed"
                    })
            return avisos
        except Exception as e:
            print(f"Error en Indeed: {e}")
            return []

    def buscar_computrabajo(self, cargo="Full Stack"):
        """Busca en CompuTrabajo Chile (Nueva fuente)"""
        query = cargo.lower().replace(" ", "-")
        url = f"https://cl.computrabajo.com/trabajo-de-{query}"
        print(f"🔍 Cazando en CompuTrabajo Chile: {url}...")
        
        try:
            response = self.scraper.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            avisos = []

            for card in soup.select('article.box_offer'):
                if len(avisos) >= 15: break

                # Filtro de fecha: CompuTrabajo suele poner "Ayer" o "Hace X días"
                fecha_el = card.select_one('.fc_aux')
                fecha_texto = fecha_el.get_text(strip=True).lower() if fecha_el else ""
                
                # Si dice "hace más de una semana" o "30 días", saltar
                if "mes" in fecha_texto or "más de" in fecha_texto:
                    continue

                link_el = card.select_one('a.js-o-link')
                if link_el:
                    titulo = link_el.get_text(strip=True)
                    link = "https://cl.computrabajo.com" + link_el['href']
                    avisos.append({
                        "titulo": titulo,
                        "url": link,
                        "fuente": "CompuTrabajo"
                    })
            return avisos
        except Exception as e:
            print(f"Error en CompuTrabajo: {e}")
            return []

    def buscar_todo(self, cargo="Full Stack"):
        """Ejecuta la búsqueda en todas las plataformas"""
        resultados = []
        
        # 1. Get on Board
        resultados.extend(self.buscar_getonboard(cargo.lower().replace(" ", "-")))
        time.sleep(1) 
        
        # 2. Indeed
        resultados.extend(self.buscar_indeed(cargo))
        time.sleep(1)

        # 3. CompuTrabajo (¡Nueva!)
        resultados.extend(self.buscar_computrabajo(cargo))
        
        print(f"📊 Total de avisos frescos recolectados: {len(resultados)}")
        return resultados