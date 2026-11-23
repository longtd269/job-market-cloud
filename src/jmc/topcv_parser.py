from datetime import date
from bs4 import BeautifulSoup
import pandas as pd

EXPECTED_COLUMNS = [
    "created_date",
    "job_title",
    "company",
    "salary",
    "address",
    "time",
    "link_description",
]

def _clean_city(name: str) -> str:
    return name.replace("(mới)", "").strip()

def parse_job_card(card, crawl_date: date) -> dict:
    title_link = card.select_one("h3.title a")
    title = title_link.select_one("span[title]")
    company = card.select_one(".company-name")
    salary = card.select_one(".title-salary")
    posted = card.select_one("label.label-update")

    address_link = card.select_one("a.address")
    tooltip = BeautifulSoup(address_link.get("title", ""), "html.parser")
    cities = [_clean_city(li.get_text(strip=True)) for li in tooltip.select("li")]
    if not cities:
        cities = [_clean_city(address_link.get_text(strip=True))]

    return {
        "created_date": crawl_date.isoformat(),
        "job_title": title["title"].strip() if title else title_link.get_text(" ", strip=True),
        "company": company.get_text(strip=True) if company else None,
        "salary": salary.get_text(strip=True) if salary else None,
        "address": ": ".join(cities),
        "time": posted.get_text(" ", strip=True) if posted else None,
        "link_description": title_link["href"],
    }

def parse_list_page(html: str, crawl_date: date) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    rows = [parse_job_card(card, crawl_date) for card in soup.select("div.job-item-search-result")]
    return pd.DataFrame(rows, columns=EXPECTED_COLUMNS)    