import heapq
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import NamedTuple
from uuid import UUID


class Record(NamedTuple):
    day: date
    company: str
    region: int
    shows: int
    clicks: int


class Top(NamedTuple):
    company: UUID
    value: int


def get_records(tsv_file: Path):
    with tsv_file.open("r") as fp:
        for i, line in enumerate(fp):
            if i == 0:
                continue
            day, company, region, shows, clicks = line.split("\t")
            yield Record(
                date.fromisoformat(day),
                company,
                int(region),
                int(shows),
                int(clicks),
            )


def calculate_top(
    tsv_file_path: Path,
    start_date: date,
    end_date: date,
    stats_by: str,
    top_size: int,
):
    companies = defaultdict(int)
    for record in get_records(tsv_file_path):
        if start_date <= record.day <= end_date:
            companies[record.company] -= getattr(record, stats_by)

    companies_queue = [(value, id_) for id_, value in companies.items()]
    heapq.heapify(companies_queue)

    top_companies = []
    for _ in range(min(top_size, len(companies_queue))):
        value, company = heapq.heappop(companies_queue)
        top_companies.append(Top(UUID(company), -value))

    return top_companies
