import datetime
import glob
import json
from pathlib import Path
from pprint import pprint

EXPORT_DIRECTORY = "export-servicing"
PULL_DIRECTORY = f"{EXPORT_DIRECTORY}/pulls"
REVIEW_DIRECTORY = f"{EXPORT_DIRECTORY}/reviews"


# export/xxxx/pullsで探索できるようにする
# reportも分離するようにする
def main():
    report = {
        "count": 0,
        "approves": {},
        "reviewers": {},
    }

    td = 0
    md = 0
    mds = []

    target_pulls = {}
    for f in glob.glob(f"{PULL_DIRECTORY}/*.json"):
        with open(f) as ff:
            data = json.load(ff)
            for d in data:
                created_at = d["created_at"]
                merged_at = d["merged_at"]
                if merged_at:
                    c = created_at.split("T")[0].split("-")
                    m = merged_at.split("T")[0].split("-")
                    d = datetime.date(int(m[0]), int(m[1]), int(m[2])) - datetime.date(int(c[0]), int(c[1]), int(c[2]))
                    print(d.days)
                    td += 1
                    md += d.days
                    mds.append(d)
                continue
                # print(f'{created_at} {merged_at}')
                # This logic is not best...
                date_list = created_at.split("T")[0].split("-")
                if datetime.date(
                    int(date_list[0]), int(date_list[1]), int(date_list[2])
                ) >= datetime.date(2021, 11, 1):
                    target_pulls[d["number"]] = [
                        r["login"] for r in d["requested_reviewers"]
                    ]

    mds.sort(reverse=True)
    print(mds)
    print(td)

    return

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
                    report["reviewers"].setdefault(user, 0)
                    report["reviewers"][user] += 1
                    report["approves"].setdefault(user, 0)
                    report["approves"][user] += 1
                    caches.append(user)

            for u in target_pulls[file_number]:
                if u in caches:
                    continue
                report["reviewers"].setdefault(u, 0)
                report["reviewers"][u] += 1

    pprint(report)


if __name__ == "__main__":
    main()
