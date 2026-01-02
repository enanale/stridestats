# StrideStats 🏃‍♂️📊

StrideStats is a **local-first, data-sovereign** analysis tool designed for data nerds who want to dive deeper into their Strava activities. Built primarily for runners (but adaptable for all), it bypasses the high-level app summaries and gives you direct access to your raw performance data.

## Why StrideStats?

- **Data Sovereignty**: Your fitness history belongs to you. Keep a local backup in raw JSON and optimized Parquet formats.
- **Deep Insights**: Move beyond the basic charts. Use Jupyter Notebooks to perform custom analysis on pace, cadence, and splits.
- **Geographic Exploration**: Use interactive maps to explore your running routes with heatmap visualizations and polyline route decoding.
- **Privacy First**: Sensitive API tokens stay in your local `.env`, and your detailed workout data never leaves your machine.

## Quick Start

### 1. Prerequisite: Strava API Setup
To fetch your data, you'll need to register a personal application on Strava:
1. Go to [Strava API Settings](https://www.strava.com/settings/api).
2. Create an app (Website & Callback Domain can be `localhost`).
3. Note your **Client ID** and **Client Secret**.

### 2. Installation
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/stridestats.git
cd stridestats

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy the example environment file and add your Strava credentials:
```bash
cp .env.example .env
```
Open `.env` and fill in `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`.

### 4. Usage

**Step 1: Authenticate**
Run the built-in OAuth tool to secure your access tokens:
```bash
python main.py auth
```

**Step 2: Sync Data**
Download your activities to `data/raw/`:
```bash
python main.py sync --limit 200  # Sync most recent 200 runs
```

**Step 3: Process**
Flatten the raw JSON into optimized Parquet files for fast loading:
```bash
python main.py process
```

**Step 4: Analyze**
Launch Jupyter or open the included notebooks in VS Code:
- **Overview**: `notebooks/01_Activities_Overview.ipynb` (Trends, frequency, mileage).
- **Maps**: `notebooks/02_Maps_and_Locations.ipynb` (Start location heatmaps, route plotting).
- Kernel: Select **Python (StrideStats)**

## Project Structure

- `stridestats/`: Core Python library (Auth, Client, Processing).
- `data/`: Local storage for raw JSON and processed Parquet data.
- `notebooks/`: Jupyter Notebooks for analysis and visualization.
- `main.py`: Unified CLI entry point.

## License
MIT
