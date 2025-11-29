# LinkForge - Web Crawler

Intelligent website crawler for comprehensive link discovery and site mapping
Powerful Python-based web crawler that systematically explores websites, 
extracts all accessible links, and generates detailed site maps.

## What it does

- Crawls websites starting from a given URL
- Discovers all accessible links within the same domain
- Filters out unwanted file types (PDFs, images, archives, etc.) -> `config.txt`
- Saves results to a clean text file

## Output

All discovered links are saved to `links.txt`, one URL per line.

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the crawler
python crawler.py
