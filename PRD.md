# Product Requirements Document: StrideStats

## 1. Introduction
**StrideStats** is a local-first data analysis tool that enables Strava users to download their activity data, store it locally, and perform custom analytics and visualization using Jupyter Notebooks.

## 2. Objectives
- **Data Sovereignty**: Allow users to maintain a local backup of their Strava history.
- **Flexible Analysis**: Enable custom data processing and visualization beyond Strava's built-in features.
- **Extensibility**: Provide a foundation for building diverse analytical notebooks.

## 3. Scope
### In Scope
- CLI/Script for downloading activities from Strava API.
- Selective download filtering (e.g., date range, activity count).
- Local storage of activity data.
- Jupyter Notebook templates for common analyses.
- Initial Visualization: Annual activity breakdown by type.

### Out of Scope
- Web interface (for the MVP, notebooks are the UI).
- Modifying/Uploading data back to Strava.
- Social features.

## 4. Functional Requirements

### 4.1 Data Ingestion (Importer Tool)
- **Authentication**: The tool must authenticate with Strava using OAuth2.
  - User handles obtaining Client ID/Secret from Strava settings.
  - Tool handles the OAuth flow (getting/refreshing tokens).
- **Fetch Capabilities**:
  - Fetch summary list of user activities.
  - Support pagination to retrieve full history.
  - **Filtering**: User must be able to limit download volume (e.g., date range, limit).
- **Storage**:
  - Data must be saved locally in a structured format.

### 4.2 Data Analysis (Notebooks)
- **Environment**: Project provides dependency management.
- **Core Notebook**: `01_Activities_Overview.ipynb`
  - Loads locally stored data.
  - **Visualization**: Generates a chart showing the number of activities per year, broken down by Activity Type (Run, Ride, Swim, etc.).

## 5. Non-Functional Requirements
- **Privacy**: All data remains on the user's local machine.
- **Rate Limiting**: Importer must respect Strava API rate limits:
    - **Overall**: 200 requests every 15 minutes, 2,000 daily.
    - **Read**: 100 requests every 15 minutes, 1,000 daily.
- **Usability**: Scripts should provide feedback on progress.

## 6. User Story / Workflow
1. **Setup**: User sets up Strava API credentials.
2. **Import**: User runs the import tool to sync data locally.
3. **Analyze**: User opens the notebook to view visualizations and perform analysis.
