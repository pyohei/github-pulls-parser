import json
import os
import time

import click
import requests

EXPORT_DIRECTORY = "export"
PULL_DIRECTORY = f"{EXPORT_DIRECTORY}/pulls"
REVIEW_DIRECTORY = f"{EXPORT_DIRECTORY}/reviews"


@click.command()
@click.option("--token", required=True, help="GitHub Personal token")
@click.option("--owner", required=True, help="GitHub owner.")
@click.option("--repo", required=True, help="GitHub repository.")
@click.option("--start-page", required=False, default=1, help="Start page.")
@click.option("--end-page", required=False, default=1, help="End page.")
def main(token, owner, repo, start_page, end_page):
    os.makedirs(PULL_DIRECTORY, exist_ok=True)
    os.makedirs(REVIEW_DIRECTORY, exist_ok=True)

    pull_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }
    params = {
        "state": "closed",
        "per_page": "100",
        "page": 0,  # this value change the below code.
    }
    # fetch pulls
    for n in range(start_page, end_page + 1):
        params["page"] = n
        response = requests.get(pull_url, params=params, headers=headers)
        pulls = response.json()
        with open(f"{PULL_DIRECTORY}/{str(n)}.json", "w") as f:
            f.write(json.dumps(pulls, indent=2))
        print(pull_url)
        time.sleep(1)

        # fetch reviews
        for pull in pulls:
            # basically review comment count is less 100, and I only fetch page 1.
            review_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pull["number"]}/reviews?per_page=100&page=1'
            response = requests.get(review_url, headers=headers)
            reviews = response.json()
            with open(f'{REVIEW_DIRECTORY}/{str(pull["number"])}.json', "w") as f:
                f.write(json.dumps(reviews, indent=2))
            print(review_url.split("?")[0])
            time.sleep(3)


if __name__ == "__main__":
    main()
