from src.utils import get_redis_connection, get_listing_details , send_to_result, send_to_dlq
from src.tools.config import Config
from src.tools.logger import logger
import requests
from bs4 import BeautifulSoup
import time

class Crawler:
    
    def __init__(self):
        self.redis_conn = get_redis_connection()

    def start_queue_consuming(self):
        while True:
            try:
                # Web sayfasından ilanları çek
                response = requests.get(Config.DOMAIN)
                response.raise_for_status() 
                soup = BeautifulSoup(response.text, 'html.parser')
                listings = soup.find_all('div', class_='_3qUI9q')
                # Her ilan için işleme yap
                for listing in listings:
                    link_tag = listing.find('a', href=True)
                    if link_tag:
                        ilan_url = Config.DOMAIN+link_tag['href']
                        if not self.redis_conn.exists(ilan_url):  # Redis'te URL'nin olup olmadığını kontrol et
                            # Detayları çek
                            details = get_listing_details(ilan_url)
                            if details:
                                # Veriyi doğrula ve Redis'e kaydet
                                send_to_result(details)
                                self.redis_conn.set(ilan_url, str(details))  # Veriyi string formatında Redis'e kaydet
                                logger.info(f"İlan URL'si {ilan_url} kaydedildi ve Redis'e eklendi.")
                            else:
                                logger.error(f"İlan URL'si {ilan_url} detayları alınamadı.")
                                send_to_dlq({'url': ilan_url, 'error': 'Detaylar alınamadı'})

                logger.info("Yeni ilanlar için bekleniyor...")
                time.sleep(Config.SLEEP_LONG)
            except Exception as e:
                logger.error(f"Queue tüketilirken hata oluştu: {e}")
                time.sleep(Config.SLEEP_LONG)