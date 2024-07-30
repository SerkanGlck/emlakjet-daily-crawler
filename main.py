import logging
from time import sleep
from src.services import Crawler
from src.tools.config import Config

def main():
    logging.basicConfig(level=logging.INFO)
    
    crawler = Crawler()
    
    while True:
        try:
            crawler.start_queue_consuming()
        except Exception as e:
            logging.error("An error occurred while consuming the queue.", exc_info=e)
        finally:
            logging.info(f"Sleeping for {Config.SLEEP_LONG} seconds.")
            sleep(Config.SLEEP_LONG)

if __name__ == '__main__':
    main()