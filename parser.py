import datetime
import glob
import json
from pathlib import Path

EXPORT_DIRECTORY = "export"
PULL_DIRECTORY = f"{EXPORT_DIRECTORY}/pulls"
REVIEW_DIRECTORY = f"{EXPORT_DIRECTORY}/reviews"


def main():
    report = {
        "count": 0,
        "approves": {},
    }

    target_pulls = []
    for f in glob.glob(f"{PULL_DIRECTORY}/*.json"):
        with open(f) as ff:
            data = json.load(ff)
            for d in data:
                created_at = d["created_at"]
                # This logic is not best...
                date_list = created_at.split("T")[0].split("-")
                if datetime.date(
                    int(date_list[0]), int(date_list[1]), int(date_list[2])
                ) >= datetime.date(2021, 10, 10):
                    target_pulls.append(d["number"])

    for f in glob.glob(f"{REVIEW_DIRECTORY}/*.json"):
        file_number = int(Path(f).stem)
        if file_number not in target_pulls:
            continue

        report["count"] += 1
        with open(f) as ff:
            data = json.load(ff)
            caches = []
            for d in data:
                user = d["user"]["login"]
                if user in caches:
                    continue
                elif d["state"] == "APPROVED":
                    report["approves"].setdefault(user, 0)
                    report["approves"][user] += 1
                    caches.append(user)
    print(report)


if __name__ == "__main__":
    main()
