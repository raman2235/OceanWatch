# OceanWatch – Ocean Hazard Monitoring & Reporting Platform

OceanWatch is an integrated platform designed for real-time monitoring and reporting of coastal hazards. It orchestrates a sophisticated data pipeline that ingests and classifies data from multiple social media platforms alongside crowdsourced user reports to provide location-based risk insights.

## 📁 Project Structure

The repository is organized into two primary independent modules:

- **`/backend`**: FastAPI (Python) server handling data ingestion, hazard classification logic, and SQLite database management.
- **`/src`**: React.js frontend built with Vite, providing dynamic dashboards and hotspot visualizations.

---

## 🚀 Getting Started

### Prerequisites
* **Python**: 3.8+
* **Node.js**: 14+
* **Package Manager**: npm

### 1. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python db_setup.py
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be running at http://127.0.0.1:8000.

### 2. Frontend Setup
1. Navigate to the root directory:
    ```bash
    cd ..
    ```
2. Install dependencies:
    ```bash
    npm install
    ```
3. Start the development server:
    ```bash
    npm run dev
    ```
The dashboard will be available at http://localhost:5173.

## Features

- **User Authentication**: Secure, role-based user management with different permissions for Citizens, Officials, and Analysts.
- **User Reporting**: Enables citizens to submit reports on coastal hazards, including a description, location, and optional file uploads.
- **Social Media Data Ingestion**: Automatically fetches and processes posts from social media platforms such as Twitter, Reddit, and YouTube to identify potential hazard events.
- **Automated Classification**: A rule-based classifier analyzes social media post content to automatically assign a hazard type (e.g., Flood, Cyclone, Tsunami) and an urgency level (High, Medium, Low).
- **Hotspot Visualization**: Aggregates data from both user reports and social media feeds to generate a dynamic heatmap of high-risk coastal areas.

## Tech Stack

**Backend**
* **Framework**: FastAPI
* **Database**: SQLite
* **Language**: Python
* **Dependencies**: Pydantic, Passlib, Jose, Tweepy, praw, google-api-python-client, requests, python-dotenv, shutil, glob

**Frontend**
* **Framework**: React.js
* **Build Tool**: Vite
* **Styling**: Tailwind CSS, PostCSS
* **Mapping**: Leaflet.js, Leaflet.heat
* **Dependencies**: react, react-dom, react-leaflet, react-router-dom
