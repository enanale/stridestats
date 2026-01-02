# Technical Design Document: StrideStats

## 1. Technical Stack
- **Language**: Python 3.10+ (using 3.10.0 for stability)
- **Environment**: Virtual Environment (`venv`)
- **Data Handling**: `pandas`
- **API Interaction**: `requests` (for direct control over Strava's OAuth and pagination)
- **Local Storage**: 
    - Raw data: JSON files in `data/raw/` (maintains API fidelity)
    - Processed data: Parquet or CSV for efficient loading into Pandas
- **Visualization**: `matplotlib` or `seaborn`
- **Notebook Interface**: `jupyterlab` or VS Code Jupyter Extension (Recommended for beginners)
- **Kernel Management**: `ipykernel` (to ensure the notebook uses the project venv)
- **Environment Management**: Virtual Environment (`venv`)

## 2. System Architecture

### 2.1 Importer Module (`stridestats/importer.py`)
- **OAuth Manager**: Handles token acquisition and refresh logic. Uses a local `.env` or `credentials.json` to store secrets.
- **Strava Client**: Wraps Strava API calls for fetching listing and detailed activities.
- **Sync Logic**: 
    - Checks for existing data to implement incremental sync.
    - Limits downloads based on user-provided flags (e.g., `--since`, `--limit`).

### 2.2 Storage Layer
- `/data/raw/activities/*.json`: Store raw activity responses.
- `/data/processed/activities.parquet`: A single flattened table of all activities for fast notebook loading.

### 2.3 Analysis Layer
- `/notebooks/`: Directory containing Jupyter `.ipynb` files.
- `notebooks/01_Activities_Overview.ipynb`: Primary visualization entry point.

## 3. Implementation Details

### 3.1 Authentication Flow
1. User provides `CLIENT_ID` and `CLIENT_SECRET`.
2. One-time authorization via browser to get `AUTHORIZATION_CODE`.
3. Exchange `AUTHORIZATION_CODE` for `ACCESS_TOKEN` and `REFRESH_TOKEN`.
4. Store tokens locally.
5. On subsequent runs, use `REFRESH_TOKEN` to get a fresh `ACCESS_TOKEN` if expired.

### 3.2 Data Processing Pipeline
1. **Fetch**: GET `/athlete/activities` with pagination.
2. **Save**: Write each activity summary to a JSON file.
3. **Process**: A script/method reads all JSONs, flattens relevant fields (type, date, distance, etc.), and saves to a compressed format (Parquet) for the notebook.

## 4. Proposed Directory Structure
```text
stridestats/
├── data/
│   ├── raw/           # Raw JSON from API
│   └── processed/     # Optimized files for Pandas
├── notebooks/         # Jupyter Notebooks
├── stridestats/       # Source code for importer
│   ├── __init__.py
│   ├── auth.py
│   ├── client.py
│   └── processing.py
├── .env.example
├── PRD.md
├── TDD.md
├── requirements.txt
└── main.py            # Entry point for CLI
```

## 5. Risk Assessment
- **API Rate Limits**:
    - Limits: 100 read requests / 15 min, 1,000 / day.
    - Strategy: Use large page sizes (100+) to minimize requests. Implement back-off or sleep if `X-RateLimit-Usage` headers indicate threshold proximity.
- **Schema Changes**: Strava API is stable, but raw JSON storage allows for re-processing if fields change.
