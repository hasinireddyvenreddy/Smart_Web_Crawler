
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class HTMLParser:

    def extract_data(self, html: str, page_url: str) -> dict:
        """
        Extract useful information from webpage HTML.
        """

        soup = BeautifulSoup(html, "lxml")

        # Extract website title
        title = (
            soup.title.get_text(strip=True)
            if soup.title else ""
        )

        # Extract headings
        headings = [
            heading.get_text(" ", strip=True)
            for heading in soup.find_all(
                ["h1", "h2", "h3", "h4", "h5", "h6"]
            )
        ]

        # Extract paragraphs
        paragraphs = [
            paragraph.get_text(" ", strip=True)
            for paragraph in soup.find_all("p")
            if paragraph.get_text(strip=True)
        ]

        # Extract hyperlinks
        links = [
            urljoin(page_url, link["href"])
            for link in soup.find_all("a", href=True)
        ]

        # Extract images
        images = [
            urljoin(page_url, image["src"])
            for image in soup.find_all("img", src=True)
        ]

        # Extract metadata
        metadata = {}

        for meta in soup.find_all("meta"):
            name = (
                meta.get("name")
                or meta.get("property")
                or meta.get("http-equiv")
            )

            content = meta.get("content")

            if name and content:
                metadata[name] = content

        return {
            "url": page_url,
            "title": title,
            "headings": headings,
            "paragraphs": paragraphs,
            "links": links,
            "images": images,
            "metadata": metadata
        }
    
    def search_keyword(self, data: list, keyword: str) -> list:
        """Search for a keyword in extracted webpage content."""

        results = []

        keyword = keyword.lower()

        for page in data:
            content = (
                page.get("title", "") + " " +
                " ".join(page.get("headings", [])) + " " +
                " ".join(page.get("paragraphs", []))
            )

            if keyword in content.lower():
                results.append({
                    "url": page["url"],
                    "title": page["title"]
                })

        return results

