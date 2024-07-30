# Emlakjet Web Crawler

## Proje Açıklaması

Bu proje, emlakjet.com sitesinden günlük kiralık konut ilanlarının verilerini çekmek için geliştirilmiş bir Python uygulamasıdır. Uygulama, emlakjet sitesindeki günlük kiralık kategorisindeki son 1 gün içinde girilen verileri alır, redis ile önbellekler ve ilan id leri farklı ise marshmallow ile işleyip RabbitMQ kuyruğuna gönderir.

## Özellikler

- **Veri Çekme:** Emlakjet sitesinden günlük kiralık konut ilanlarını çekme.
- **Veri İşleme:** Çekilen verilerin marshmallow ile işlenmesi ve düzenlenmesi. (henüz tamamlanmadı)
- **Redis Entegrasyonu:** Redis ile verileri önbellekleme ve veri tekrarının kayıt edilmemesi. (henüz tamamlanmadı)
- **RabbitMQ Entegrasyonu:** İşlenen verileri RabbitMQ kuyruğuna gönderme.

## Bağımlılıklar

Bu proje, aşağıdaki Python kütüphanelerini kullanır:

- `pika`: RabbitMQ ile iletişim için
- `redis`: Redis ile veri yönetimi için
- `logging`: Uygulama içi loglama için
- `dotenv`: Çevresel değişkenlerin yönetimi için
- `os`: Çevresel değişkenlere erişim için
- `requests`: HTTP istekleri için
- `marshmallow`: JSON verilerini serileştirme ve doğrulama için
- `json`: JSON verilerini işleme için
- `time`: Zaman yönetimi için
- `beautifulsoup4`: HTML parsing ve veri çekme için

## Kurulum

### Çevresel Değişkenler

Uygulamanın çalışması için bir `.env` dosyasına ihtiyaç vardır. `.env.a` dosyasındaki bilgileri kendinize uyarlamanız gerekmektedir. aşağıdaki örnek yapılandırmaları kullanabilirsiniz:

```env
APP_NAME=emlakjet-web-crawler
DOMAIN=www.emlakjet.com/gunluk-kiralik-konut
QUEUE_NAME=emlakjet_keywords
RESULT_QUEUE_NAME=result_emlakjet

RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_VHOST=/

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

SLEEP_LONG=60
SLEEP_SHORT=1
REQUEST_TIMEOUT=15
DEBUG=true
```

**Repoyu klonlayın:**

```sh
git clone https://github.com/serkanglck/emlakjet-daily-crawler.git
cd emlakjet-daily-crawler
```


## Bağımlılıkları Yükleme

Bu projede bağımlılıkları yönetmek için `Pipenv` kullanıyoruz. Aşağıdaki adımları takip ederek gerekli bağımlılıkları yükleyebilirsiniz:

1. **Pipenv'yi Yükleyin:** Eğer `Pipenv` yüklü değilse, aşağıdaki komutu kullanarak yükleyin:
    ```bash
    pip install pipenv
    ```

2. **Bağımlılıkları Yükleyin:** Proje dizininde, bağımlılıkları yüklemek için aşağıdaki komutu çalıştırın:
    ```bash
    pipenv install
    ```

    Bu komut, `Pipfile` dosyasındaki bağımlılıkları yükler ve sanal ortamı oluşturur.


Bu adımları takip ederek projeyi çalıştırmak için gerekli bağımlılıkları yükleyebilirsiniz.

## Yapılandırma

Uygulama yapılandırması, ortam değişkenleri kullanılarak yönetilir. Referans olarak bir örnek `.env.example` dosyası sağlanmıştır.

1. **Örnek ortam dosyasını kopyalayarak kendi yapılandırmanızı oluşturun:**

    ```sh
    cp .env.example .env
    ```

2. **Değişkenlerinizi ayarlamak için `.env` dosyasını düzenleyin.**

## Kullanım

1. **Uygulamayı çalıştırın:**

    ```sh
    python main.py
    ```

## Docker kullanarak çalıştırmak (henüz tamamlanmadı)



 **Docker ile projeyi pull etmek için:**

    ```sh
    docker pull serkanglck/emlakjet-crawler:latest
    ```
  **Docker ile çalıştırmak için:**

    ```sh
    docker run --env-file .env.a emlakjet-crawler
    ```

## Loglama

Loglama, uygulamanın işlemlerini takip etmek için uygulanmıştır. Loglar, farklı seviyelerde (INFO, ERROR) konsola yazdırılır.
