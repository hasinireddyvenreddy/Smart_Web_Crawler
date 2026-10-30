import logging

from crawler.web_crawler import WebCrawler
from crawler.parser import HTMLParser
from crawler.exporter import DataExporter

from config import JSON_FILE, CSV_FILE, LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

crawler = WebCrawler()
parser = HTMLParser()
exporter = DataExporter()

try:
    start_url = "https://www.python.org"

    print("\n========== SMART WEB CRAWLER ==========\n")

    crawler.crawl(start_url)

    print("\n========== PARSING DATA ==========\n")

    extracted_data = []

    for page in crawler.pages_crawled:
        data = parser.extract_data(
            page["html"],
            page["url"]
        )

        extracted_data.append(data)

    print("\n========== EXPORTING DATA ==========\n")

    exporter.export_json(extracted_data, JSON_FILE)
    exporter.export_csv(extracted_data, CSV_FILE)

    print("\n========== CRAWLING RESULTS ==========")

    print("Total pages visited:", len(crawler.visited_urls))
    print("Successfully crawled:", len(crawler.pages_crawled))
    print("Extracted records:", len(extracted_data))
    print("\n========== KEYWORD SEARCH ==========")

    keyword = "Python"

    search_results = parser.search_keyword(
        extracted_data,
        keyword
    )

    print(f"Results for '{keyword}':")

    for result in search_results:
        print(
            "Title:", result["title"],
            "| URL:", result["url"]
        )

    print("Total matching pages:", len(search_results))
    print("\n========== CRAWLING STATISTICS ==========")

    statistics = crawler.get_statistics()

    for name, value in statistics.items():
        print(f"{name}: {value}")

finally:
    crawler.close()