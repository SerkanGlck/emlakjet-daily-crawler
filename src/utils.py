import pika
import requests
from bs4 import BeautifulSoup
from src.tools.config import Config, ConnectionsConfig
from src.tools.logger import logger
from src.schemas import IlandetailSchema
import redis
from src.tools.iso8601 import tarihi_cevir
from datetime import datetime, timedelta

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
            body=str(message),  # JSON yerine string olarak gönderiyoruz
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

def get_listing_links():
    response = requests.get(Config.DOMAIN)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('div', class_='_3qUI9q')

    url_list = []
    for listing in listings:
        link_tag = listing.find('a', href=True)
        if link_tag:
            listing_link = link_tag['href']
            # Add URL scheme
            if not listing_link.startswith(('http://', 'https://')):
                listing_link = f'https://www.emlakjet.com{listing_link}'
            url_list.append(listing_link)

    return url_list

def get_listing_details(listing_url):
    response = requests.get(listing_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', class_="_3OKyci")
    title = title_tag.text.strip() if title_tag else "Title not found"

    price_tag = soup.find('div', class_='_2TxNQv')
    price = price_tag.text.strip() if price_tag else "Price not found"

    location_tag = soup.find('div', class_='_3VQ1JB')
    location = location_tag.find('p').text.strip() if location_tag and location_tag.find('p') else "Location not found"

    details = {
        'url': listing_url,
        'baslik': title,
        'fiyat': price,
        'konum': location,
        'Ilan_Numarasi': listing_url.split('/')[-1]  # URL'den ID oluşturmak için basit bir yöntem
    }

    ilan_detaylari = soup.find_all('div', class_='_35T4WV')
    for detay in ilan_detaylari:
        bilgi_kategori = detay.find_all('div', class_='_1bVOdb')
        if len(bilgi_kategori) == 2:
            kategori = bilgi_kategori[0].text.strip()
            bilgi = bilgi_kategori[1].text.strip()
            # Şemada olan anahtarlarla uyumlu hale getirmek için anahtar isimlerini dönüştüreceğiz
            if kategori == 'Net Metrekare':
                details['Net_Metrekare'] = bilgi
            elif kategori == 'Oda Sayısı':
                details['Oda_Sayısı'] = bilgi
            elif kategori == 'Bulunduğu Kat':
                details['Bulunduğu_Kat'] = bilgi
            elif kategori == 'Isıtma Tipi':
                details['Isıtma_Tipi'] = bilgi
            elif kategori == 'Kullanım Durumu':
                details['Kullanım_Durumu'] = bilgi
            elif kategori == 'Yapı Tipi':
                details['Yapı_Tipi'] = bilgi
            elif kategori == 'Site İçerisinde':
                details['Site_İçerisinde'] = bilgi
            elif kategori == 'Banyo Sayısı':
                details['Banyo_Sayısı'] = bilgi
            elif kategori == 'WC Sayısı':
                details['WC_Sayısı'] = bilgi
            elif kategori == 'Türü':
                details['Türü'] = bilgi
            elif kategori == 'Tipi':
                details['Tipi'] = bilgi
            elif kategori == 'Brüt Metrekare':
                details['Brüt_Metrekare'] = bilgi
            elif kategori == 'Binanın Yaşı':
                details['Binanın_Yaşı'] = bilgi
            elif kategori == 'Binanın Kat Sayısı':
                details['Binanın_Kat_Sayısı'] = bilgi
            elif kategori == 'İzin Belge No':
                details['İzin_Belge_No'] = bilgi
            elif kategori == 'Yapı Durumu':
                details['Yapı_Durumu'] = bilgi
            elif kategori == 'Eşya Durumu':
                details['Eşya_Durumu'] = bilgi
            elif kategori == 'Takas':
                details['Takas'] = bilgi
            elif kategori == 'Salon Metrekare':
                details['Salon_Metrekare'] = bilgi
            elif kategori == 'Fiyat Durumu':
                details['Fiyat_Durumu'] = bilgi

    # Tarih formatlama
    try:
        if 'İlan Oluşturma Tarihi' in details:
            details['İlan_Oluşturma_Tarihi'] = tarihi_cevir(details['İlan_Oluşturma_Tarihi'])
        if 'İlan Güncelleme Tarihi' in details:
            details['İlan_Güncelleme_Tarihi'] = tarihi_cevir(details['İlan_Güncelleme_Tarihi'])
    except Exception as e:
        details['Tarih_Donusturme_Hatasi'] = str(e)
    try:
        if 'İlan_Oluşturma_Tarihi' in details:
            ilan_olusturma_tarihi = datetime.fromisoformat(details['İlan_Oluşturma_Tarihi'])
            if datetime.now() - ilan_olusturma_tarihi > timedelta(days=1):
                return None  # 1 günden eski ise ilanı atla
    except Exception as e:
        details['Tarih_Donusturme_Hatasi'] = str(e)
        return None
    # Validate using Marshmallow schema
    schema = IlandetailSchema()
    validated_data = schema.load(details) 
    return validated_data

def get_redis_connection():
    try:
        redis_conn = redis.StrictRedis(
            host=ConnectionsConfig.REDIS_HOST,
            port=ConnectionsConfig.REDIS_PORT,
            password=ConnectionsConfig.REDIS_PASSWORD,
            decode_responses=True
        )
        return redis_conn
    except Exception as e:
        logger.error(f"Redis bağlantısı kurulurken hata: {e}")
        raise