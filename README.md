##OceanWatch - Ocean Hazard Reporting Platform

This is a web-based platform for monitoring and reporting coastal hazards. It combines user-submitted reports with data from social media feeds to provide a comprehensive view of potential threats. This project was developed as part of a group effort.

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

## Project Structure

```
├── backend/
│   ├── .env                       # Environment variables
│   ├── coastal.db                 # SQLite database file
│   ├── db_setup.py                # Database setup script
│   ├── main.py                    # FastAPI application core
│   ├── social_fetcher.py          # Social media data fetching logic
│   ├── rule_classifier.py         # Hazard classification logic
│   ├── heatmap.html               # Frontend-specific map visualization
│   └── ...
├── src/
│   ├── assets/
│   ├── components/
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── .gitignore
├── index.html
├── package.json
├── postcss.config.cjs
├── README.md
├── tailwind.config.js
└── vite.config.js
```

## Getting Started

### Prerequisites

* Python 3.8+
* Node.js 14+
* npm

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/raman2235/oceanwatch.git
    cd oceanwatch
    ```

2.  Set up the backend:
    ```bash
    cd backend
    pip install -r requirements.txt  # You may need to create this file
    python db_setup.py
    ```

3.  Run the backend server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

4.  Set up the frontend:
    ```bash
    cd ..
    npm install
    ```

5.  Run the frontend development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.
