import csv
from io import StringIO
from typing import List
from src.models.base import Base


def download(rows: List[Base], fieldnames: List[str]) -> StringIO:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for row in rows:
        # ! Содержит ненужные ключи, например '_sa_instance_state', поэтому решил так
        writer.writerow(
            {field: row.__dict__[field] for field in fieldnames}
        )
    output.seek(0)
    return output
