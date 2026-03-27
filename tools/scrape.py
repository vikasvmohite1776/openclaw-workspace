#!/usr/bin/env python3
"""
Web Scraping Toolkit for OpenClaw
Usage: python3 scrape.py <url> [options]
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time
import re
import json
import csv
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.results = []
    
    def scrape_with_progress(self, urls, extract_fn=None, delay=1):
        """Scrape multiple URLs with visual progress bar"""
        results = []
        start_time = time.time()
        
        with tqdm(total=len(urls), desc="Scraping", unit="page") as pbar:
            for i, url in enumerate(urls):
                try:
                    result = extract_fn(url) if extract_fn else self.extract_basic(url)
                    results.append(result)
                    
                    # Update progress bar with time stats
                    elapsed = time.time() - start_time
                    avg_time = elapsed / (i + 1)
                    remaining = avg_time * (len(urls) - i - 1)
                    pbar.set_postfix({
                        'elapsed': f"{elapsed:.1f}s",
                        'remaining': f"{remaining:.1f}s"
                    })
                    
                    time.sleep(delay)  # Be polite
                    pbar.update(1)
                    
                except Exception as e:
                    results.append({'url': url, 'error': str(e)})
                    pbar.update(1)
        
        return results
    
    def extract_contact_info(self, url):
        """Extract name, email, job title, company from a page"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script/style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            
            # Patterns
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            
            return {
                'url': url,
                'title': soup.title.string if soup.title else '',
                'emails': ', '.join(set(emails)),
                'text_sample': text[:500],
                'scraped_at': datetime.now().isoformat()
            }
        except Exception as e:
            return {'url': url, 'error': str(e)}
    
    def save_to_csv(self, data, filename):
        """Save results to CSV with timestamp"""
        if not data:
            print("No data to save")
            return
        
        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"{filename}_{timestamp}.csv"
        df.to_csv(filepath, index=False)
        print(f"✓ Saved {len(data)} records to {filepath}")
        return filepath

if __name__ == "__main__":
    scraper = WebScraper()
    
    if len(sys.argv) < 2:
        print("Usage: python3 scrape.py <url>")
        print("       python3 scrape.py <url1> <url2> ... --csv output")
        sys.exit(1)
    
    urls = sys.argv[1:]
    results = scraper.scrape_with_progress(urls, scraper.extract_contact_info)
    
    for r in results[:3]:
        print(json.dumps(r, indent=2))
    print(f"\n... and {len(results) - 3} more results")
