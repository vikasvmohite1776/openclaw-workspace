# Automation Tools Suite

Custom Python tools for web scraping, summarization, and SQL insights.

## 📁 Tools Location
`~/.openclaw/workspace/tools/`

## 🕷️ Web Scraping (`scrape.py`)

**Features:**
- Visual progress bar with time elapsed/remaining
- Contact info extraction (emails, names)
- CSV export with timestamps
- Polite rate limiting

**Usage:**
```bash
# Scrape single page
python3 ~/.openclaw/workspace/tools/scrape.py https://example.com

# Scrape multiple + save CSV
python3 ~/.openclaw/workspace/tools/scrape.py https://site1.com https://site2.com
```

**Workflow Integration:**
```python
from tools.scrape import WebScraper
scraper = WebScraper()
results = scraper.scrape_with_progress(urls, scraper.extract_contact_info)
scraper.save_to_csv(results, "leads")
```

---

## 📄 Article Summarizer (`summarize.py`)

**Features:**
- Extracts clean article content
- Basic extractive summarization
- Generates shareable HTML with styling
- Word count and metadata

**Usage:**
```bash
# Summarize article
python3 ~/.openclaw/workspace/tools/summarize.py https://example.com/article

# Custom sentence count
python3 ~/.openclaw/workspace/tools/summarize.py https://example.com --sentences 10
```

**Output:** HTML file with:
- Clean summary box
- Full article content
- Source link
- Metadata (date, word count)

---

## 📊 SQL Insights (`sql_insights.py`)

**Features:**
- Table statistics (row counts, nulls)
- Column analysis (numeric + categorical)
- Automatic HTML report generation
- CSV sample export

**Usage:**
```bash
# Analyze SQLite table
python3 ~/.openclaw/workspace/tools/sql_insights.py 'sqlite:///data.db' --table users

# PostgreSQL example
python3 ~/.openclaw/workspace/tools/sql_insights.py 'postgresql://user:pass@localhost/db' --table sales
```

**Output Files:**
- `table_report_YYYYMMDD_HHMMSS.html` - Full visual report
- `table_sample_YYYYMMDD_HHMMSS.csv` - Sample data
- `table_insights_YYYYMMDD_HHMMSS.json` - Raw statistics

---

## 🔄 Typical Workflows

### Lead Generation Pipeline
1. Search for target companies/people
2. `scrape.py` → extract contact info
3. `save_to_csv()` → structured data
4. Import to Notion/CRM

### Article Sharing Pipeline
1. `summarize.py` → clean HTML summary
2. Upload to cloud storage / email
3. Team gets readable version

### Data Analysis Pipeline
1. `sql_insights.py` → analyze source table
2. Review HTML report for patterns
3. Export CSV sample for deeper analysis
4. Generate charts/visualizations

---

## 📝 Requirements

Already installed:
- `requests`, `beautifulsoup4` - HTTP + HTML parsing
- `pandas`, `tqdm` - Data + progress bars
- `playwright` - Browser automation (optional)
- `sqlalchemy` - Database connections
- `weasyprint` - PDF generation (optional)

---

## 🚀 Future Enhancements

- [ ] Playwright integration for JS-heavy sites
- [ ] PDF export for summaries
- [ ] Scheduled scraping jobs via cron
- [ ] Notion database sync
- [ ] GitHub Actions integration
