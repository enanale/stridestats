import os
import json
import argparse
from pathlib import Path
from stridestats.auth import StravaAuth
from stridestats.client import StravaClient
from stridestats.processing import DataProcessor

def main():
    """
    Main entry point for the StrideStats CLI.
    Supports:
    - whoami: Verify API connection
    - auth: Initial OAuth2 authorization
    - sync: Download activities from Strava
    - process: Flatten raw JSON data into Parquet/CSV
    """
    parser = argparse.ArgumentParser(description="StrideStats: Strava Data Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Command: Get athlete info
    subparsers.add_parser("whoami", help="Display athlete info to verify connection")

    # Command: Initial Auth
    subparsers.add_parser("auth", help="Generate authorization URL")

    # Command: Sync activities
    sync_parser = subparsers.add_parser("sync", help="Download activities")
    sync_parser.add_argument("--limit", type=int, default=None, help="Max number of activities to download. If not set, fetches all.")
    sync_parser.add_argument("--pagesize", type=int, default=100, help="Results per page (default: 100)")

    # Command: Process data
    subparsers.add_parser("process", help="Process raw JSON into flattened Dataframe")

    args = parser.parse_args()

    auth = StravaAuth()
    client = StravaClient(auth)

    if args.command == "whoami":
        try:
            athlete = client.get_athlete()
            print(f"Connected as: {athlete.get('firstname')} {athlete.get('lastname')} (ID: {athlete.get('id')})")
        except Exception as e:
            print(f"Error: {e}")

    elif args.command == "auth":
        port = os.getenv("STRAVA_REDIRECT_PORT", "8000")
        url = auth.get_authorization_url(port=port)
        print("\n--- Strava Authorization ---")
        print("1. Visit the following URL in your browser:")
        print(f"\n{url}\n")
        print("2. Click 'Authorize'.")
        print(f"3. You will be redirected to a page that fails to load (e.g., http://localhost:{port}/?code=...)")
        print("4. Copy the 'code' parameter from the URL bar and paste it here.")
        
        code = input("\nEnter the authorization code: ").strip()
        if code:
            try:
                auth.exchange_code_for_token(code)
                print("Successfully authenticated and saved tokens!")
            except Exception as e:
                print(f"Authentication failed: {e}")

    elif args.command == "sync":
        try:
            raw_dir = Path("data/raw")
            raw_dir.mkdir(parents=True, exist_ok=True)

            print("Starting sync...")
            page = 1
            total_synced = 0
            
            while True:
                per_page = args.pagesize
                if args.limit and (total_synced + per_page > args.limit):
                    per_page = args.limit - total_synced
                
                if per_page <= 0:
                    break

                print(f"Fetching page {page} ({per_page} items)...")
                activities = client.get_activities(page=page, per_page=per_page)
                
                if not activities:
                    print("No more activities found.")
                    break

                for activity in activities:
                    activity_id = activity.get('id')
                    file_path = raw_dir / f"{activity_id}.json"
                    with open(file_path, "w") as f:
                        json.dump(activity, f, indent=2)
                
                total_synced += len(activities)
                print(f"Synced {len(activities)} activities (Total: {total_synced})")
                
                if len(activities) < per_page or (args.limit and total_synced >= args.limit):
                    break
                
                page += 1
            
            print(f"Sync complete. Total activities stored in {raw_dir}: {total_synced}")
        except Exception as e:
            print(f"Sync failed: {e}")

    elif args.command == "process":
        try:
            processor = DataProcessor()
            processor.flatten_activities()
        except Exception as e:
            print(f"Processing failed: {e}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
