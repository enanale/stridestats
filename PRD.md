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

### 4.3 Advanced Analysis Modules (Proposed)
These modules extend the basic analysis to provide deeper insights into performance, behavior, and geography.

#### 4.3.1 Performance & Physiology
- **Cumulative Progress Comparison**:
  - Interactive chart comparing cumulative distance and elevation gain for the current year vs. previous years.
  - Helps answer: "Am I ahead or behind my mileage from last year?"
- **Intensity Distribution**:
  - Histograms showing the distribution of Average Heart Rate and Average Speed across activities.
  - **Zone Analysis**: Classification of activities into low/medium/high intensity buckets based on user-defined thresholds.
- **Taper & Load Tracking**:
  - Rolling 7-day and 30-day average distance/duration to visualize training volume and rest weeks.

#### 4.3.2 Geospatial Intelligence
- **Global Activity Heatmap**:
  - A single interactive map overlaying all activity poly-lines.
  - **Metric Coloring**: Option to color paths by Speed, Heart Rate, or Grade (e.g., fast sections in red, slow in blue).
- **Route "Small Multiples" (Implemented)**:
  - A faceted grid display showing the geometry of every individual run/ride as a standalone shape, sorted by date or distance.
  - Useful for visualizing the variety of routes taken.
  - Located in: `notebooks/04_Route_Gallery.ipynb`
- **Territory Explorer**:
  - Analysis of unique "tiles" or grid squares visited (similar to VeloViewer).

#### 4.3.3 Fun & Gamification
- **The "Epic" Leaderboard**:
  - Automatic ranking of top 10 "toughest" activities based on a custom score (Distance * Elevation Gain).
- **Eddington Number**:
  - Calculation of the Eddington Number for Cycling and Running (e.g., "I have run E miles at least E times").
- **Consistency Calendar**:
  - A "GitHub-style" contribution heatmap showing daily activity frequency and streak analysis.
  - **Day-of-Week Split**: Pie chart showing "Weekend Warrior" vs. "Weekday Worker" volume distribution.

#### 4.3.4 Artistic & Generative Visualizations (New)
For athletes with large datasets (1000+ activities), these views transform raw data into "Data Art."

- **The "Route Bloom" (Composite Overlay)**:
  - All ~2,000 routes are centered at a single origin (0,0) and plotted with very high transparency (1-2%).
  - Result: A ghostly, glowing "nebulous" shape that reveals the statistical center and extreme reaches of the athlete's exploration.
- **The "DNA Strand" (Chronological Strip)**:
  - A very long, thin high-resolution image where all 2,000 routes are plotted side-by-side as minimal sparklines.
  - Sorting by date creates a vertical or horizontal "fingerprint" of your athletic life.
- **The "Time Spiral"**:
  - Routes are arranged along a mathematical spiral (Archimedean) based on their timestamp.
  - Helps visualize the density of activity over years in a single circular composition.
- **Route "Similarity Clusters" (The Galaxy Map)**:
  - Using basic features (distance, elevation, aspect ratio), routes are positioned in a 2D space.
  - Cluster "islands" emerge: one for "short lunch runs," another for "mountain loop rides," etc.
- **The "Pace Heat" Mosaic**:
  - A massive grid of every route shape, color-coded by relative intensity or average speed.
  - Result: A colorful tapestry showing "blocks" of peak performance seasons.

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
