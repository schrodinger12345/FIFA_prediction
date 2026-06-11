import requests
import pandas as pd
from pathlib import Path


def fetch_fifa_rankings(gender="men"):
    base_url = "https://www.fotmob.com"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": f"{base_url}/fifaranking/{gender}",
    }

    periods_response = requests.get(
        f"{base_url}/api/data/fifarankings/period",
        params={"gender": gender},
        headers=headers,
        timeout=30,
    )
    periods_response.raise_for_status()
    periods = periods_response.json()
    if not periods:
        raise ValueError("No FIFA ranking periods were returned by FotMob")

    latest_period_id = periods[0]["periodId"]

    rankings_response = requests.get(
        f"{base_url}/api/data/fifarankings/ranking",
        params={"gender": gender, "periodId": latest_period_id},
        headers=headers,
        timeout=30,
    )
    rankings_response.raise_for_status()

    rankings = rankings_response.json()
    df = pd.DataFrame(rankings)[["name", "totalPoints"]].rename(
        columns={"name": "Team names", "totalPoints": "FIFA points"}
    )
    return df


def save_to_excel(df, filename="fifa_rankings.xlsx"):
    output_path = Path(__file__).resolve().with_name(filename)
    df.to_excel(output_path, index=False)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    df = fetch_fifa_rankings()
    print(df.head())
    save_to_excel(df)