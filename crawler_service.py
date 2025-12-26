import schedule
import time
import logging
import json
import os
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
, vercel_deploy_hook=None):
        self.crawler = WoltCrawler(wolt_url, output_file, vercel_deploy_hook=vercel_deploy_hook
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
    # Load configuration
    config_file = 'config.json'
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        WOLT_URL = config.get('wolt_url', 'YOUR_WOLT_RESTAURANT_URL_HERE')
        OUTPUT_FILE = config.get('output_file', 'products.json')
        CHECK_INTERVAL = config.get('check_interval_minutes', 5)
        VERCEL_DEPLOY_HOOK = config.get('vercel_deploy_hook', None)
    else:
        WOLT_URL = "YOUR_WOLT_RESTAURANT_URL_HERE"
        OUTPUT_FILE = "products.json"
        CHECK_INTERVAL = 5
        VERCEL_DEPLOY_HOOK = None
    
    if WOLT_URL == "YOUR_WOLT_RESTAURANT_URL_HERE":
        print("\n⚠ WARNING: Please update your config.json file!")
        print("Set your Wolt restaurant URL in config.json\n")
        exit(1)
    
    logging.info(f"Website: https://kahvila-ochre.vercel.app/")
    logging.info(f"Vercel Deploy: {'Enabled' if VERCEL_DEPLOY_HOOK else 'Disabled'}")
    
    service = CrawlerService(WOLT_URL, OUTPUT_FILE, VERCEL_DEPLOY_HOOK)
    service.run(CHECK_INTERVAL)
