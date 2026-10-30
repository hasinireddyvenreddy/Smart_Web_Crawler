
from html import parser
import time
import logging
import requests

from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException
from urllib.robotparser import RobotFileParser
from time import perf_counter


from config import (
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    MAX_RETRIES,
    USER_AGENT,
    MAX_DEPTH,
    MAX_PAGES
)


class WebCrawler:

    def __init__(self):
        self.failed_urls = []
        self.start_time = None
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": USER_AGENT
        })

        self.logger = logging.getLogger(__name__)

        self.visited_urls = set()
        self.pages_crawled = []
    def can_fetch(self, url: str) -> bool:
        """Check whether robots.txt allows crawling."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            parser.read()

            return parser.can_fetch(
                USER_AGENT,
                url
            )

        except Exception as error:
            self.logger.warning(
                "Could not read robots.txt: %s",
                error
            )

            return False    

    def download_page(self, url: str):

        for attempt in range(1, MAX_RETRIES + 1):

            try:
                self.logger.info("Downloading: %s", url)

                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT
                )

                response.raise_for_status()

                time.sleep(REQUEST_DELAY)

                return response.text

            except RequestException as error:

                self.logger.warning(
                    "Attempt %s failed: %s",
                    attempt,
                    error
                )

                if attempt < MAX_RETRIES:
                    time.sleep(2)

        self.logger.error("Failed to download: %s", url)

        return None

    def get_internal_links(self, html: str, base_url: str):

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "lxml")

        internal_links = set()

        base_domain = urlparse(base_url).netloc

        for link in soup.find_all("a", href=True):

            full_url = urljoin(base_url, link["href"])

            parsed_url = urlparse(full_url)

            if (
                parsed_url.scheme in ("http", "https")
                and parsed_url.netloc == base_domain
            ):

                clean_url = parsed_url._replace(
                    fragment=""
                ).geturl()

                internal_links.add(clean_url)

        return internal_links

    def crawl(self, start_url: str, depth: int = 0):

        if depth == 0 and self.start_time is None:
            self.start_time = perf_counter()

        if depth > MAX_DEPTH:
            return
        if len(self.visited_urls) >= MAX_PAGES:
            return
        if start_url in self.visited_urls:
            return

        self.visited_urls.add(start_url)
        if not self.can_fetch(start_url):
            self.logger.warning(
             "Crawling not allowed: %s",
                start_url
            )
            return

        html = self.download_page(start_url)

        if not html:
            self.failed_urls.append(start_url)
            return

        self.pages_crawled.append({
            "url": start_url,
            "html": html,
            "depth": depth
        })

        print(
            f"Crawled: {start_url} | Depth: {depth}"
        )

        if depth < MAX_DEPTH:

            links = self.get_internal_links(
                html,
                start_url
            )

            for link in links:

                if link not in self.visited_urls:

                    self.crawl(link, depth + 1)
    
    def get_statistics(self):
        """Return crawling statistics."""

        execution_time = 0

        if self.start_time is not None:
            execution_time = round(
                perf_counter() - self.start_time, 2
            )

        return {
            "Pages Visited": len(self.visited_urls),
            "Pages Successfully Crawled": len(self.pages_crawled),
            "Failed Downloads": len(self.failed_urls),
            "Execution Time (seconds)": execution_time
        }
                

    def close(self):
        self.session.close()
