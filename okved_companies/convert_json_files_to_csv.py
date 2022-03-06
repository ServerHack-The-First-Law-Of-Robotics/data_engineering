from typing import List, Dict
from csv import DictWriter
from glob import glob

from okved_companies.data_saving import read_results_from_json


def preproc_json_to_csv(json_pth: str) -> List[Dict]:
    results = read_results_from_json(json_pth)

    rows = []
    for page_data in results.values():
        okved = page_data.okved
        if page_data.is_error:
            continue
        for company in page_data.companies_list:
            row = {
                "okved": okved,
                "inn": company.inn,
                "ogrn": company.ogrn
            }
            rows.append(row)
    return rows


if __name__ == "__main__":
    json_files = glob("../data/okved_companies/*.json")
    fields = ["okved", "inn", "ogrn"]

    preprocessed_rows = []

    for pth in json_files:
        preprocessed_file_rows = preproc_json_to_csv(pth)
        preprocessed_rows += preprocessed_file_rows

    with open("../data/okved_companies/okved_companies_data.csv", "w", newline="") as f:
        csv_writer = DictWriter(f, fields)
        csv_writer.writeheader()

        for row in preprocessed_rows:
            csv_writer.writerow(row)
