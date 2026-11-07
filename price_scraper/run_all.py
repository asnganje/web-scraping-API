import subprocess
import sys
from pathlib import Path

SCRAPY_PROJECT_DIR = Path(__file__).resolve().parent
print(f"Director is....{SCRAPY_PROJECT_DIR}")

SPIDERS = [
    "lappyworld",
    "digitonia",
    "fahavi"
]

spider_results = []
for spider in SPIDERS:
    print(f"\nStarting spider: {spider}")
    result = subprocess.run([
        sys.executable,
        "-m",
        "scrapy",
        "crawl",
        spider
        ],
        cwd=SCRAPY_PROJECT_DIR
    )

    status = "Success" if result.returncode == 0 else "Failed"
    spider_results.append({
        "spider":spider,
        "status":status
    })

print("\n=================SPIDERS SUMMARY=============")
for result in spider_results:
    print(f"{result["spider"]}: {result["status"]}")
print("=================================================")
