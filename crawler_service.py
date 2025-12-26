import schedule
import time
import logging
from wolt_crawler import WoltCrawler
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)

class CrawlerService:
    def __init__(self, wolt_url, output_file='products.json'):
        self.crawler = WoltCrawler(wolt_url, output_file)
        
    def job(self):
        """Job to run periodically"""
        logging.info("Running scheduled check...")
        try:
            self.crawler.check_for_updates()
        except Exception as e:
            logging.error(f"Error during check: {e}")
    
    def run(self, interval_minutes=5):
        """Run the service with scheduled checks"""
        logging.info(f"Starting Wolt Crawler Service")
        logging.info(f"Check interval: {interval_minutes} minutes")
        
        # Run once immediately
        self.job()
        
        # Schedule recurring checks
        schedule.every(interval_minutes).minutes.do(self.job)
        
        # Run the scheduler
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Service stopped by user")


if __name__ == "__main__":
    # Configuration
    WOLT_URL = "YOUR_WOLT_RESTAURANT_URL_HERE"  # Replace with your Wolt URL
    OUTPUT_FILE = "products.json"
    CHECK_INTERVAL = 5  # Minutes between checks
    
    if WOLT_URL == "YOUR_WOLT_RESTAURANT_URL_HERE":
        print("\n⚠ WARNING: Please update WOLT_URL in the script!")
        print("Edit crawler_service.py and set your Wolt restaurant URL\n")
        exit(1)
    
    service = CrawlerService(WOLT_URL, OUTPUT_FILE)
    service.run(CHECK_INTERVAL)
