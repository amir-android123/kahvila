import requests
from bs4 import BeautifulSoup
import json
import time
import os
from datetime import datetime
import hashlib
import subprocess
import re
from urllib.parse import unquote

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
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
            }
            response = requests.get(self.wolt_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching Wolt page: {e}")
            return None
    
    def extract_products(self, html_content):
        """Extract products from the HTML content"""
        products = []
        
        # Method 1: Find and parse the items array from URL-encoded JSON
        # Wolt embeds product data in URL-encoded JSON within the HTML
        idx = html_content.find('%22items%22%3A%5B')
        
        if idx < 0:
            print("  No items array found in page")
            return products
        
        # Extract a large chunk starting from items
        chunk = html_content[idx:idx+150000]
        
        # Find end of items array - look for the next key
        end_match = re.search(r'%5D%2C%22options%22', chunk)
        if end_match:
            chunk = chunk[:end_match.start() + 3]
        
        # URL decode
        decoded = unquote(chunk)
        
        # Parse as JSON
        json_str = '{' + decoded + '}'
        
        try:
            data = json.loads(json_str)
            items = data.get('items', [])
            
            for item in items:
                product = self._parse_item(item)
                if product:
                    products.append(product)
            
            print(f"  Found {len(products)} products")
            
        except json.JSONDecodeError as e:
            print(f"  JSON parse error: {e}")
            # Fallback: use regex extraction
            products = self._extract_with_regex(decoded)
        
        return products
    
    def _parse_item(self, item):
        """Parse a single item dictionary into a product"""
        if not isinstance(item, dict):
            return None
            
        name = item.get('name', '')
        if not name or len(name) < 2:
            return None
        
        # Get price (Wolt stores prices in cents)
        price = item.get('price', 0)
        if isinstance(price, int):
            price = price / 100
        
        # Get image URL
        image_url = ''
        images = item.get('images', [])
        if images and isinstance(images, list) and len(images) > 0:
            if isinstance(images[0], dict):
                image_url = images[0].get('url', '')
            elif isinstance(images[0], str):
                image_url = images[0]
        
        # Get description
        description = item.get('description', '') or ''
        
        # Get item ID
        item_id = item.get('id', '') or hashlib.md5(name.encode()).hexdigest()[:16]
        
        return {
            'id': item_id,
            'name': name,
            'description': description,
            'price': round(price, 2),
            'image_url': image_url,
            'category': ''
        }
    
    def _extract_with_regex(self, decoded_content):
        """Fallback regex extraction method"""
        products = []
        
        # Pattern for individual items
        item_pattern = r'"id":"([a-f0-9]+)"[^}]*"name":"([^"]+)"[^}]*"price":(\d+)[^}]*"images":\[\{"url":"([^"]+)"'
        matches = re.findall(item_pattern, decoded_content, re.DOTALL)
        
        for item_id, name, price, image_url in matches:
            if len(name) < 2:
                continue
            products.append({
                'id': item_id,
                'name': name,
                'description': '',
                'price': round(int(price) / 100, 2),
                'image_url': image_url,
                'category': ''
            })
        
        print(f"  Regex found {len(products)} products")
        return products
    
    def get_content_hash(self, products):
        """Generate a hash of the products to detect changes"""
        # Sort by ID for consistent hashing
        sorted_products = sorted(products, key=lambda x: x.get('id', x.get('name', '')))
        content_str = json.dumps(sorted_products, sort_keys=True)
        return hashlib.md5(content_str.encode()).hexdigest()
    
    def save_products(self, products):
        """Save products to JSON file in a clean format"""
        try:
            # Sort products by name for consistent output
            sorted_products = sorted(products, key=lambda x: x.get('name', ''))
            
            # Create clean output format
            output_products = []
            for p in sorted_products:
                output_products.append({
                    'name': p.get('name', ''),
                    'description': p.get('description', ''),
                    'price': p.get('price', 0),
                    'image_url': p.get('image_url', ''),
                    'category': p.get('category', '')
                })
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(output_products, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(output_products)} products to {self.output_file}")
            return True
        except Exception as e:
            print(f"✗ Error saving products: {e}")
            return False
    
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
            
            # Get the directory of the output file
            work_dir = os.path.dirname(os.path.abspath(self.output_file))
            if not work_dir:
                work_dir = os.getcwd()
            
            # Add the products file
            result = subprocess.run(
                ['git', 'add', self.output_file], 
                check=True, 
                cwd=work_dir,
                capture_output=True,
                text=True
            )
            
            # Check if there are changes to commit
            status_result = subprocess.run(
                ['git', 'status', '--porcelain', self.output_file],
                cwd=work_dir,
                capture_output=True,
                text=True
            )
            
            if not status_result.stdout.strip():
                print("  No changes to commit")
                return False
            
            # Commit
            commit_msg = f'Auto-update products - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            subprocess.run(
                ['git', 'commit', '-m', commit_msg], 
                check=True, 
                cwd=work_dir,
                capture_output=True,
                text=True
            )
            
            # Push
            subprocess.run(
                ['git', 'push', 'origin', 'main'], 
                check=True, 
                cwd=work_dir,
                capture_output=True,
                text=True
            )
            
            print("✓ Changes pushed to GitHub!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Git operation failed: {e}")
            if e.stderr:
                print(f"  Error: {e.stderr}")
            return False
        except Exception as e:
            print(f"✗ Error with git: {e}")
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
            self.last_hash = content_hash
            self.save_products(products)
            
            # Calculate differences
            old_names = set(p['name'] for p in old_products)
            new_names = set(p['name'] for p in products)
            added = new_names - old_names
            removed = old_names - new_names
            
            print(f"✓ Products updated: {len(products)} total")
            if added:
                print(f"  + Added: {', '.join(list(added)[:3])}{'...' if len(added) > 3 else ''}")
            if removed:
                print(f"  - Removed: {', '.join(list(removed)[:3])}{'...' if len(removed) > 3 else ''}")
            
            # Push to GitHub and trigger Vercel deployment
            if self.git_commit_and_push():
                time.sleep(2)  # Wait a moment before triggering deployment
                self.trigger_vercel_deployment()
            
            return True
        else:
            print("✓ No changes detected")
            return False
    
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
    # Load configuration
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
    
    print(f"Vercel Deploy: {'Enabled ✓' if VERCEL_DEPLOY_HOOK else 'Disabled ✗'}")
    print()
    
    crawler = WoltCrawler(
        wolt_url=WOLT_URL,
        output_file=OUTPUT_FILE,
        check_interval=CHECK_INTERVAL,
        vercel_deploy_hook=VERCEL_DEPLOY_HOOK
    )
    
    # Run continuously
    crawler.run_continuous()
