# Wolt Crawler - Automatic Product Monitor

This crawler automatically monitors your Wolt restaurant page and updates the website when new items are added.

## Features

- 🔄 Automatic monitoring of Wolt product listings
- 📦 Extracts product names and images
- 💾 Saves to JSON file that the website reads
- 🔔 Detects and logs new additions/removals
- ⏰ Configurable check intervals
- 📝 Detailed logging

## Setup Instructions

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4 schedule
```

### 2. Configure Your Wolt URL

Edit `wolt_crawler.py` or `crawler_service.py` and replace:

```python
WOLT_URL = "YOUR_WOLT_RESTAURANT_URL_HERE"
```

with your actual Wolt restaurant URL (e.g., `https://wolt.com/en/fin/helsinki/restaurant/your-restaurant`)

### 3. Run the Crawler

#### Option A: Windows Batch File (Easiest)
Double-click `run_crawler.bat`

#### Option B: Direct Python
```bash
python wolt_crawler.py
```

#### Option C: As a Service (with scheduling)
```bash
python crawler_service.py
```

## Configuration Options

In `wolt_crawler.py` or `crawler_service.py`, you can adjust:

- `CHECK_INTERVAL`: Time between checks (in seconds for wolt_crawler.py, minutes for crawler_service.py)
- `OUTPUT_FILE`: Path to the JSON file (default: `products.json`)

## How It Works

1. **Crawler fetches** your Wolt page HTML
2. **Extracts products** using pattern matching
3. **Compares** with previous data to detect changes
4. **Updates** `products.json` if changes are found
5. **Website automatically** loads products from `products.json`

## Files

- `wolt_crawler.py` - Main crawler script (continuous mode)
- `crawler_service.py` - Service wrapper with scheduling
- `run_crawler.bat` - Windows batch file to run easily
- `products.json` - Generated file with product data (auto-created)
- `crawler.log` - Log file (auto-created by service)

## Logs

The crawler logs all activities including:
- New products added
- Products removed
- Update timestamps
- Errors (if any)

## Troubleshooting

### Crawler not finding products
- Make sure your Wolt URL is correct
- Check if Wolt has changed their HTML structure
- Look at `crawler.log` for error details

### Website not showing products
- Make sure `products.json` exists in the website root
- Check browser console for errors
- Ensure your web server serves JSON files correctly

### Automatic updates not working
- Keep the crawler running in the background
- Check the `CHECK_INTERVAL` setting
- Verify the crawler has write permissions

## Running as Background Service

### Windows
You can run the crawler in the background using Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Action: Start a program
5. Program: `pythonw.exe` (no console window)
6. Arguments: `"c:\Bon Bon\crawler_service.py"`
7. Start in: `c:\Bon Bon`

### Linux
Create a systemd service or use cron:
```bash
*/5 * * * * cd /path/to/Bon\ Bon && python3 wolt_crawler.py
```

## Security Notes

- The crawler only reads public Wolt pages
- No authentication required
- Respects Wolt's public data
- Use reasonable check intervals (5+ minutes recommended)

## Support

If you encounter issues:
1. Check `crawler.log` for errors
2. Verify your Wolt URL is accessible
3. Ensure all dependencies are installed
4. Check that Python is in your PATH
