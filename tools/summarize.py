#!/usr/bin/env python3
"""
Article Summarizer & PDF Generator
Usage: python3 summarize.py <url> --format pdf
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import sys
import os

def fetch_article(url):
    """Fetch and clean article content"""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unwanted elements
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        tag.decompose()
    
    # Try to find main content
    content = None
    for selector in ['article', 'main', '[role="main"]', '.content', '.post', '.entry']:
        content = soup.select_one(selector)
        if content:
            break
    
    if not content:
        content = soup.find('body')
    
    title = soup.title.string if soup.title else 'Untitled'
    text = content.get_text(separator='\n\n', strip=True)
    
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return {
        'title': title,
        'url': url,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'content': text,
        'word_count': len(text.split())
    }

def summarize_text(text, max_sentences=5):
    """Basic extractive summarization"""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    if len(sentences) <= max_sentences:
        return text
    
    # Simple scoring: sentences with more "important" words
    word_freq = {}
    words = re.findall(r'\w+', text.lower())
    for word in words:
        if len(word) > 4:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    scores = []
    for sent in sentences[:20]:  # Look at first 20 sentences
        score = sum(word_freq.get(w.lower(), 0) for w in re.findall(r'\w+', sent))
        scores.append((score, sent))
    
    # Get top sentences
    top_sentences = sorted(scores, reverse=True)[:max_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: sentences.index(x[1]))
    
    return ' '.join(s[1] for s in top_sentences)

def generate_html(article, summary):
    """Generate shareable HTML"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{article['title']}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }}
        h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .meta {{ color: #666; font-size: 14px; margin-bottom: 30px; }}
        .summary {{ background: #f5f5f5; padding: 20px; border-left: 4px solid #007AFF; margin-bottom: 30px; }}
        .summary h2 {{ margin-top: 0; font-size: 18px; }}
        .content {{ font-size: 16px; }}
        a {{ color: #007AFF; }}
    </style>
</head>
<body>
    <h1>{article['title']}</h1>
    <div class="meta">
        Source: <a href="{article['url']}">{article['url']}</a><br>
        Summarized: {article['date']} | {article['word_count']} words
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>{summary}</p>
    </div>
    
    <div class="content">
        {article['content'][:3000].replace(chr(10), '<br>')}
        {'<p><em>... (content truncated)</em></p>' if len(article['content']) > 3000 else ''}
    </div>
</body>
</html>"""
    
    filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w') as f:
        f.write(html)
    
    return filename

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 summarize.py <url> [--sentences 5]")
        sys.exit(1)
    
    url = sys.argv[1]
    sentences = 5
    
    if '--sentences' in sys.argv:
        idx = sys.argv.index('--sentences')
        sentences = int(sys.argv[idx + 1])
    
    print(f"Fetching {url}...")
    article = fetch_article(url)
    
    print(f"Summarizing ({article['word_count']} words)...")
    summary = summarize_text(article['content'], sentences)
    
    print("\n" + "="*60)
    print(f"TITLE: {article['title']}")
    print(f"WORD COUNT: {article['word_count']}")
    print("="*60)
    print("\nSUMMARY:")
    print(summary)
    print("\n" + "="*60)
    
    filename = generate_html(article, summary)
    print(f"\n✓ Saved to: {filename}")
    print(f"  Open in browser: open {filename}")
