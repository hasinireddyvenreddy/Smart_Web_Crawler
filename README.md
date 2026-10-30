# Smart Web Crawler & Data Extraction Engine

## About the Project

This is my Task 4 project for the **Algoryx Python Developer Internship**.

I created this project using Python to crawl websites and collect useful information from web pages. It extracts details like page titles, headings, paragraphs, links, images, and metadata.

The collected information is saved in JSON and CSV files so that it can be viewed and used later.

## Features

- Crawls web pages automatically.
- Extracts website information using BeautifulSoup.
- Collects titles, headings, paragraphs, links, and images.
- Follows internal links up to a given depth.
- Avoids visiting the same URL more than once.
- Checks robots.txt before crawling.
- Handles network errors with retry attempts.
- Saves extracted data in JSON and CSV formats.
- Searches website content using keywords.
- Displays crawling statistics.
- Saves activity details in a log file.

## Technologies Used

- Python
- Requests
- BeautifulSoup4
- lxml
- JSON
- CSV
- python-dotenv

## Project Structure

```text
Smart_Web_Crawler/
│
├── crawler/
│   ├── __init__.py
│   ├── web_crawler.py
│   ├── parser.py
│   └── exporter.py
│
├── output/
│   ├── data.json
│   └── data.csv
│
├── logs/
│   └── crawler.log
│
├── config.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## How to Run the Project

First, create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

## Configuration

The crawling settings can be changed in the `.env` file.

```env
MAX_DEPTH=2
MAX_PAGES=10
REQUEST_TIMEOUT=15
REQUEST_DELAY=1
MAX_RETRIES=3
USER_AGENT=SmartWebCrawler/1.0
```

## Output

After running the project, the extracted data is saved in:

- `output/data.json`
- `output/data.csv`

The crawling logs are saved in:

- `logs/crawler.log`

## Project Testing

I tested my crawler using Python.org.

It successfully crawled 10 web pages, extracted the required information, searched for the keyword "Python", and saved the results in JSON and CSV formats.

It also displayed crawling statistics, including the number of pages visited, failed downloads, and execution time.

## Internship

**Algoryx Python Developer Internship – Task 4**