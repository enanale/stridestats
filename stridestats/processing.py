import json
import pandas as pd
from pathlib import Path

class DataProcessor:
    """
    Transforms raw Strava JSON activities into a flattened Pandas DataFrame,
    saving to Parquet and CSV.
    """
    def __init__(self, raw_dir="data/raw", processed_dir="data/processed"):
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def flatten_activities(self, output_name="activities.parquet"):
        activities = []
        
        # Load all JSON files in raw_dir
        json_files = list(self.raw_dir.glob("*.json"))
        if not json_files:
            print("No raw activity files found to process.")
            return None

        print(f"Processing {len(json_files)} activities...")
        
        for file_path in json_files:
            with open(file_path, "r") as f:
                data = json.load(f)
                
                # Flatten the fields we care about
                # Strava API returns a lot, let's pick core ones for our goals
                start_latlng = data.get("start_latlng", [])
                end_latlng = data.get("end_latlng", [])
                
                flat_activity = {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "type": data.get("type"),
                    "sport_type": data.get("sport_type"),
                    "start_date": data.get("start_date"),
                    "start_date_local": data.get("start_date_local"),
                    "distance": data.get("distance"),
                    "moving_time": data.get("moving_time"),
                    "elapsed_time": data.get("elapsed_time"),
                    "total_elevation_gain": data.get("total_elevation_gain"),
                    "average_speed": data.get("average_speed"),
                    "max_speed": data.get("max_speed"),
                    # Location and Map Data
                    "start_lat": start_latlng[0] if len(start_latlng) == 2 else None,
                    "start_lng": start_latlng[1] if len(start_latlng) == 2 else None,
                    "end_lat": end_latlng[0] if len(end_latlng) == 2 else None,
                    "end_lng": end_latlng[1] if len(end_latlng) == 2 else None,
                    "map_polyline": data.get("map", {}).get("summary_polyline"),
                    "location_city": data.get("location_city"),
                    "location_state": data.get("location_state"),
                    "location_country": data.get("location_country"),
                }
                activities.append(flat_activity)

        df = pd.DataFrame(activities)
        
        # Basic type conversion
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['year'] = df['start_date'].dt.year
        
        # Save as Parquet
        output_path = self.processed_dir / output_name
        df.to_parquet(output_path, index=False)
        
        # Also save as CSV for easier inspection during development
        df.to_csv(self.processed_dir / "activities.csv", index=False)
        
        print(f"Successfully processed {len(activities)} activities.")
        print(f"Saved to {output_path}")
        return df
