#!/usr/bin/env python3
"""Convert the registration CSV into XML. No third-party packages required."""
import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

FIELDS = [
    "id", "username", "email", "firstname", "lastname",
    "idnumber", "password", "city", "country"
]

def main():
    if len(sys.argv) != 3:
        print("Usage: csv_to_xml.py <input.csv> <output.xml>", file=sys.stderr)
        return 2

    input_csv, output_xml = map(Path, sys.argv[1:])

    root = ET.Element("users")

    with input_csv.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [f for f in FIELDS if f not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

        for line_no, row in enumerate(reader, start=2):
            user = ET.SubElement(root, "user")
            for field in FIELDS:
                value = (row.get(field) or "").strip()
                child = ET.SubElement(user, field)
                child.text = value

    ET.indent(root, space="  ")
    output_xml.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output_xml, encoding="utf-8", xml_declaration=True)
    print(f"Created {output_xml} from {input_csv}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
