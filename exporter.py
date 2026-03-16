import pandas as pd
import json
import os
from datetime import datetime

EXPORT_DIR = "data/exports"


def export_excel(data):

    os.makedirs(EXPORT_DIR, exist_ok=True)

    filename = f"{EXPORT_DIR}/shodan_{datetime.now().timestamp()}.xlsx"

    df = pd.DataFrame(data)

    df.to_excel(filename, index=False)

    return filename


def export_json(data):

    os.makedirs(EXPORT_DIR, exist_ok=True)

    filename = f"{EXPORT_DIR}/shodan_{datetime.now().timestamp()}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return filename
