
# MobileWeatherDevice

A weather dashboard that retrieves weather forecasts from Malaysia's MET API, translates Malay weather descriptions into English, and presents daily forecasts through an interactive interface.

## Overview

MobileWeatherDevice is a Python-based weather application designed to make Malaysian weather forecasts easier to understand and access.

The application retrieves weather forecast data from the Malaysian government's public weather API (data.gov.my), stores the retrieved information locally using SQLite, and displays it through a web-based dashboard.

Malay weather descriptions are translated into English using a custom rule-based translation module. The dashboard also provides weather icons, temperature information, rain intensity indicators, and animated visual effects.

## Features

- **Weather Forecasts:** View current-day and upcoming weather forecasts.
- **Location Selection:** Search and select available locations, including states, districts, towns, divisions, and recreation centres.
- **English Translation:** Automatically translate Malay weather descriptions into English.
- **Temperature Information:** View daily minimum and maximum temperatures.
- **Weather Conditions:** Display weather icons for sunny, rainy, overcast, hazy, and thunderstorm conditions.
- **Rain Intensity:** Categorise rainfall descriptions into four intensity levels.
- **Temperature Range:** Visualise daily temperature ranges through graphical indicators.
- **Weather Animations:** Display animated weather icons, rainfall effects, and lightning effects.
- **Local Data Storage:** Store retrieved forecasts and location information using SQLite.
- **Responsive Interface:** Adapt the dashboard layout to desktop and mobile screen sizes.

## Technologies Used

| Category | Technology |
| --- | --- |
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Template Engine | Jinja2 |
| Database | SQLite |
| Animation Library | anime.js |
| HTTP Client | HTTPX |
| Testing Framework | pytest |
| Weather Data Source | [Malaysia Public Weather API](https://api.data.gov.my/weather/forecast/) |

## Project Structure

```text
MobileWeatherDevice/
│
├── app/
│   ├── main.py                 # FastAPI application and routes
│   │
│   ├── static/
│   │   ├── ambient.js          # Rain and lightning effects
│   │   ├── anime.umd.min.js    # Animation library
│   │   ├── app.js              # Dashboard animations
│   │   ├── picker.js           # Location search and selection
│   │   └── style.css           # Dashboard styling
│   │
│   └── templates/
│       ├── _icons.html         # Weather icon components
│       └── index.html          # Main dashboard template
│
├── collector/
│   ├── check_db.py             # Database inspection utility
│   ├── explore_api.py          # Weather API exploration
│   ├── explore_phrases.py      # Forecast phrase analysis
│   └── run_daily.py            # Forecast collection process
│
├── core/
│   ├── db.py                   # SQLite database configuration
│   └── translate.py            # Malay-to-English translation
│
├── tests/
│   └── test_translate.py       # Translation unit tests
│
├── requirements.txt            # Python dependencies
├── run_collector.bat           # Windows collector launcher
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10 or newer
- pip (Python package manager)
- Git
- Internet connection for retrieving weather forecasts

### 1. Clone the Repository

```bash
git clone https://github.com/Jacqueson1/MobileWeatherDevice.git

cd MobileWeatherDevice
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv .venv

.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Collect Weather Data

Run the weather collector to retrieve forecasts and initialise the SQLite database.

```bash
python -m collector.run_daily
```

The collector retrieves forecasts from the MET Malaysia API and stores them in:

```text
data/weather.db
```

The database is created automatically when the collector runs for the first time.

### 5. Start the Application

Run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Open your browser and navigate to:

```text
http://127.0.0.1:8000
```

## Weather Data Source

This application retrieves weather forecast information from the MET Malaysia public API.

**API Endpoint:**

https://api.data.gov.my/weather/forecast/

The collector retrieves forecast information, including:

- Location information
- Forecast dates
- Morning forecasts
- Afternoon forecasts
- Night forecasts
- General weather summaries
- Minimum temperatures
- Maximum temperatures

Retrieved forecasts are stored as dated snapshots in the local SQLite database.

## Translation System

The application uses a custom rule-based translation module located in `core/translate.py`.

It recognises common Malay weather descriptions and converts them into English.

Examples:

| Malay Description | English Translation |
| --- | --- |
| Tiada hujan | No rain |
| Hujan di beberapa tempat | Scattered rain |
| Ribut petir di beberapa tempat | Scattered thunderstorms |
| Hujan di kebanyakan tempat | Rain in most places |
| Jerebu | Haze |
| Mendung | Overcast |

The translation module also identifies rainfall intensity and geographical descriptions, such as coastal and inland areas.

Unknown descriptions are preserved in their original form rather than discarded.

## Running Tests

The project uses pytest to test the translation module.

Run the test suite using:

```bash
pytest
```

To run only the translation tests:

```bash
pytest tests/test_translate.py -v
```

## Database

The application uses SQLite for local data persistence.

The database contains two main tables:

**locations**
- Location ID
- Location name
- Location type
- Latitude
- Longitude

**forecast_snapshots**
- Forecast date
- Retrieval date and timestamp
- Forecast lead time
- Morning, afternoon, and night descriptions
- General weather summary
- Minimum and maximum temperatures

Forecast snapshots are stored separately by retrieval date, allowing the application to retain previously collected forecast records.

## Notes

- An active internet connection is required to retrieve new forecasts.
- The dashboard displays previously stored forecasts.
- Forecast collection is performed separately from the dashboard application.
- The default location is Langkawi (`Ds001`).
- Weather description translations are rule-based and depend on the phrases recognised by the translation module.
- The project currently provides a web-based interface.

## License

No license file is currently provided in this repository.
