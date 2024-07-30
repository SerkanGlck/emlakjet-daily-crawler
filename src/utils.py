import pika
import json
import requests
from bs4 import BeautifulSoup
from src.tools.config import Config,ConnectionsConfig
from src.tools.logger import logger

def get_rabbitmq_connection():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=ConnectionsConfig.RABBITMQ_HOST,
                port=ConnectionsConfig.RABBITMQ_PORT,
                virtual_host=ConnectionsConfig.RABBITMQ_VHOST,
                credentials=pika.PlainCredentials(
                    username=ConnectionsConfig.RABBITMQ_USER,
                    password=ConnectionsConfig.RABBITMQ_PASSWORD
                )
            )
        )
        return connection
    except Exception as e:
        logger.error(f"RabbitMQ bağlantısı kurulurken hata: {e}")
        raise

def send_to_queue(queue_name, message):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  
            )
        )
        logger.info(f"Mesaj '{queue_name}' kuyruğuna gönderildi: {message}")
        connection.close()
    except Exception as e:
        logger.error(f"Kuyruğa mesaj gönderirken hata: {e}")

def send_to_result(message):
    send_to_queue(Config.RESULT_QUEUE_NAME, message)

def send_to_dlq(message):
    send_to_queue('dlq', message)

def fetch_listing_ids_and_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        listings = soup.find_all('div', class_='_3qUI9q')

        current_ids_and_links = []
        for listing in listings:
            link_tag = listing.find('a', href=True)
            if link_tag:
                listing_id = listing.get('data-id')
                if listing_id:
                    current_ids_and_links.append((listing_id, link_tag['href']))
        
        return current_ids_and_links
    except Exception as e:
        logger.error(f"İlan ID'leri ve bağlantıları çekilirken hata: {e}")
        return []

def fetch_listing_details(listing_id, listing_link):

    listing_url = f'https://www.emlakjet.com{listing_link}'
    try:
        response = requests.get(listing_url)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1', class_="_3OKyci")
        title = title_tag.text.strip() if title_tag else "Başlık bulunamadı"

        price_tag = soup.find('div', class_='_2TxNQv')
        price = price_tag.text.strip() if price_tag else "Fiyat bulunamadı"

        location_tag = soup.find('div', class_='_3VQ1JB')
        location = location_tag.find('p').text.strip() if location_tag and location_tag.find('p') else "Konum bulunamadı"

        details = {
            'url': listing_url,
            'baslik': title,
            'fiyat': price,
            'konum': location,
            'Ilan Numarasi': listing_id
        }

        detail_tags = soup.find_all('div', class_='_35T4WV')
        for detail in detail_tags:
            info_categories = detail.find_all('div', class_='_1bVOdb')
            if len(info_categories) == 2:
                category = info_categories[0].text.strip()
                info = info_categories[1].text.strip()
                details[category] = info

        return details
    except Exception as e:
        logger.error(f"İlan detayları çekilirken hata: {e}")
        return {}
