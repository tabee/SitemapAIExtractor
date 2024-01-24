# SitemapAIExtractor
## Overview
SitemapAIExtractor is a Python-based tool for extracting and analysing information from websites. It uses a series of modules to analyse websites using a sitemap, extract content from each URL, analyse HTML content and save the extracted information in a structured format in a csv-file.

## Modules
- `sitemap_parser.py`: Parses sitemaps to extract URLs.
- `html_parser.py`: Parses HTML content from given URLs.
- `content_analyzer.py`: Analyzes content using predefined keywords and rules.
- `extracted_information_assembler.py`: Orchestrates the extraction of information from URLs in a sitemap and saves the data in a CSV file.
- `main.py`: The main script for executing the information extraction process.

## Getting Started

### Prerequisites
- Python 3.x
- Required Python libraries: `requests`, `bs4` (BeautifulSoup)

### Installation
Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/tabee/SitemapAIExtractor.git
cd SitemapAIExtractor
pip install -r requirements.txt
```

### Usage
To use the SitemapAIExtractor, run the main.py script. You can modify the configuration settings in main.py to suit your specific requirements.
```bash
cd app
python main.py
```
