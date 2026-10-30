import json
import csv
from pathlib import Path


class DataExporter:

    def export_json(self, data: list, file_path: Path):
        """Export crawled data to a JSON file."""

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"JSON file saved: {file_path}")

    def export_csv(self, data: list, file_path: Path):
        """Export crawled data to a CSV file."""

        if not data:
            print("No data available to export.")
            return

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "url",
                    "title",
                    "headings",
                    "paragraphs",
                    "links",
                    "images",
                    "metadata"
                ]
            )

            writer.writeheader()

            for page in data:
                row = page.copy()

                for key in [
                    "headings",
                    "paragraphs",
                    "links",
                    "images",
                    "metadata"
                ]:
                    row[key] = json.dumps(
                        row.get(key, {}),
                        ensure_ascii=False
                    )

                writer.writerow(row)

        print(f"CSV file saved: {file_path}")