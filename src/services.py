from src.utils import fetch_listing_ids_and_links, fetch_listing_details, send_to_result, send_to_dlq
from src.tools.config import Config
from src.tools.logger import logger
import json
import time

class Crawler:
    def __init__(self):
        self.url = Config.DOMAIN
        self.previous_ids = set()
       

    def start_queue_consuming(self):
        while True:
            try:
                current_ids_and_links = fetch_listing_ids_and_links(self.url)
                new_ids_and_links = [(listing_id, link) for listing_id, link in current_ids_and_links if listing_id not in self.previous_ids]

                if new_ids_and_links:
                    logger.info(f"Toplam {len(new_ids_and_links)} yeni ilan bulundu.")
                    new_data = {}

                    for listing_id, link in new_ids_and_links:
                        details = fetch_listing_details(listing_id, link)
                        if details:
                            new_data[listing_id] = details
                            logger.info(f"İlan ID'si {listing_id} kaydedildi.")
                            send_to_result(details)
                        else:
                            logger.error(f"İlan ID'si {listing_id} detayları alınamadı.")
                            send_to_dlq({'url': link, 'error': 'Detaylar alınamadı'})

                    if new_data:
                        self.previous_ids.update(new_data.keys())

                logger.info("Yeni ilanlar için bekleniyor...")
                time.sleep(Config.SLEEP_LONG)
            except Exception as e:
                logger.error(f"Queue tüketilirken hata oluştu: {e}")
                time.sleep(Config.SLEEP_LONG)
