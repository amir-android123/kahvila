import requests
from bs4 import BeautifulSoup
import json
import time
import os
from datetime import datetime
import hashlib
import subprocess

class WoltCrawler:
    def __init__(self, wolt_url, output_file='products.json', check_interval=300, vercel_deploy_hook=None):
        """
        Initialize the Wolt crawler
        
        Args:
            wolt_url: Your Wolt restaurant/store URL
            output_file: Path to the JSON file that stores products
            check_interval: Seconds between checks (default 5 minutes)
            vercel_deploy_hook: Vercel Deploy Hook URL (optional)
        """
        self.wolt_url = wolt_url
        self.output_file = output_file
        self.check_interval = check_interval
        self.vercel_deploy_hook = vercel_deploy_hook
        self.last_hash = None
        
    def fetch_wolt_page(self):
        """Fetch the Wolt page HTML"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.wolt_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching Wolt page: {e}")
            return None
    
    def extract_products(self, html_content):
        """Extract products from the HTML content"""
        import re
        from urllib.parse import unquote
        
        # Find all URL-encoded JSON data containing product information
        pattern = r'%22name%22%3A%22([^%]+(?:%[0-9A-F]{2}[^%]*)*)%22.*?%22images%22%3A%5B%7B%22url%22%3A%22(https%3A%2F%2Fimageproxy\.wolt\.com%2Fassets%2F[a-f0-9]+)%22'
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        
        products = []
        seen_names = set()
        
        for name_encoded, url_encoded in matches:
            name = unquote(name_encoded)
            url = unquote(url_encoded)
            
            if name not in seen_names:
                seen_names.add(name)
                products.append({
                    'name': name,
                    'image_url': url,
                    'price': 0.00  # You can add price extraction logic here
                })
        
        # Also search for the reverse pattern (images before name)
        pattern2 = r'%22images%22%3A%5B%7B%22url%22%3A%22(https%3A%2F%2Fimageproxy\.wolt\.com%2Fassets%2F[a-f0-9]+)%22.*?%22name%22%3A%22([^%]+(?:%[0-9A-F]{2}[^%]*)*)%22'
        matches2 = re.findall(pattern2, html_content, re.IGNORECASE)
        
        for url_encoded, name_encoded in matches2:
            name = unquote(name_encoded)
            url = unquote(url_encoded)
            
            if name not in seen_names:
                seen_names.add(name)
                products.append({
                    'name': name,
                    'image_url': url,
                    'price': 0.00
                })
        
        return products
    
    def get_content_hash(self, products):
        """Generate a hash of the products to detect changes"""
        content_str = json.dumps(products, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()
    
    def save_products(self, products):
        """Save products to JSON file"""
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(products)} products to {self.output_file}")
            return True
        except Exception
    
    def trigger_vercel_deployment(self):
        """Trigger Vercel deployment via Deploy Hook"""
        if not self.vercel_deploy_hook:
            return False
        
        try:
            print("🚀 Triggering Vercel deployment...")
            response = requests.post(self.vercel_deploy_hook)
            if response.status_code in [200, 201]:
                print("✓ Vercel deployment triggered successfully!")
                return True
            else:
                print(f"✗ Vercel deployment failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error triggering Vercel deployment: {e}")
            return False
    
    def git_commit_and_push(self):
        """Commit and push changes to GitHub"""
        try:
            print("📤 Committing and pushing to GitHub...")
            subprocess.run(['git', 'add', self.output_file], check=True, cwd=os.path.dirname(os.path.abspath(self.output_file)) or '.')
            subprocess.run(['git', 'commit', '-m', f'Auto-update products - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'], check=True, cwd=os.path.dirname(os.path.abspath(self.output_file)) or '.')
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, cwd=os.path.dirname(os.path.abspath(self.output_file)) or '.')
            print("✓ Changes pushed to GitHub!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Git operation failed: {e}")
            return False
        except Exception as e:
            print(f"✗ Error with git: {e}")
            return False as e:
            print(f"Error saving products: {e}")
            return False
    
    def load_existing_products(self):
        """Load existing products from JSON file"""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def check_for_updates(self):
        """Check if there are new products"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for updates...")
        
        html_content = self.fetch_wolt_page()
        if not html_content:
            
            # Push to GitHub and trigger Vercel deployment
            if self.git_commit_and_push():
                time.sleep(2)  # Wait a moment before triggering deployment
                self.trigger_vercel_deployment()
            
            print("✗ Failed to fetch page")
            return False
        
        products = self.extract_products(html_content)
        if not products:
            print("✗ No products found")
            return False
        
        content_hash = self.get_content_hash(products)
        
        if self.last_hash is None:
            # First run
            self.last_hash = content_hash
            self.save_products(products)
            print(f"✓ Initial load: {len(products)} products")
            return True
        
        if content_hash != self.last_hash:
            # Content changed
            old_products = self.load_existing_products()
      Load configuration
    config_file = 'config.json'
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        WOLT_URL = config.get('wolt_url', 'YOUR_WOLT_RESTAURANT_URL_HERE')
        OUTPUT_FILE = config.get('output_file', 'products.json')
        CHECK_INTERVAL = config.get('check_interval_minutes', 5) * 60  # Convert to seconds
        VERCEL_DEPLOY_HOOK = config.get('vercel_deploy_hook', None)
    else:
        # Fallback to hardcoded values
        WOLT_URL = "YOUR_WOLT_RESTAURANT_URL_HERE"
        OUTPUT_FILE = "products.json"
        CHECK_INTERVAL = 300
        VERCEL_DEPLOY_HOOK = None
    
    print("=" * 60)
    print("Wolt Crawler - Automatic Product Monitor with Vercel Deploy")
    print("=" * 60)
    
    if WOLT_URL == "YOUR_WOLT_RESTAURANT_URL_HERE":
        print("\n⚠ WARNING: Please update your config.json file!")
        print("Set your Wolt restaurant URL in config.json\n")
        exit(1)
    
    print(f"Website: https://kahvila-ochre.vercel.app/")
    print(f"Vercel Deploy: {'Enabled ✓' if VERCEL_DEPLOY_HOOK else 'Disabled ✗'}")
    print()
    
    crawler = WoltCrawler(
        wolt_url=WOLT_URL,
        output_file=OUTPUT_FILE,
        check_interval=CHECK_INTERVAL,
        vercel_deploy_hook=VERCEL_DEPLOY_HOOK
    
    def run_once(self):
        """Run the crawler once"""
        return self.check_for_updates()
    
    def run_continuous(self):
        """Run the crawler continuously"""
        print(f"Starting Wolt Crawler...")
        print(f"Monitoring: {self.wolt_url}")
        print(f"Check interval: {self.check_interval} seconds")
        print(f"Output file: {self.output_file}")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_for_updates()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n\nCrawler stopped by user")


if __name__ == "__main__":
    # Configuration
    WOLT_URL = "YOUR_WOLT_RESTAURANT_URL_HERE"  # Replace with your Wolt URL
    OUTPUT_FILE = "products.json"
    CHECK_INTERVAL = 300  # 5 minutes
    
    print("=" * 60)
    print("Wolt Crawler - Automatic Product Monitor")
    print("=" * 60)
    
    if WOLT_URL == "YOUR_WOLT_RESTAURANT_URL_HERE":
        print("\n⚠ WARNING: Please update WOLT_URL in the script!")
        print("Edit wolt_crawler.py and set your Wolt restaurant URL\n")
        exit(1)
    
    crawler = WoltCrawler(
        wolt_url=WOLT_URL,
        output_file=OUTPUT_FILE,
        check_interval=CHECK_INTERVAL
    )
    
    # Run continuously
    crawler.run_continuous()
