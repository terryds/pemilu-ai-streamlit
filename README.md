# Pemilu 2024 Data Visualizer

An interactive Streamlit application for visualizing the 2024 Indonesian Presidential Election (Pemilu) data.

## Overview

This application provides comprehensive visualizations and analysis tools for exploring the results of Indonesia's 2024 Presidential Election. Users can interact with the data through various charts, maps, and tables to gain insights into voting patterns across the country.

## Features

- Data visualization of presidential election results
- Regional breakdown of voting data
- Interactive charts and maps
- AI-powered data analysis capabilities

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pemilu2024-visualizer.git
   cd pemilu2024-visualizer
   ```

2. Download the required database file:
   - Get the `pemilu2024-kpu.duckdb` file from: https://github.com/terryds/pemilu-2024-scraper/releases
   - Place the file in the root directory of the project

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Launch the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your default web browser, typically at http://localhost:8501

## Project Structure

- `app.py` - Main application entry point
- `visualization.py` - Data visualization components
- `ask_ai.py` - AI analysis functionality
- `about.py` - About page content
- `pemilu2024-kpu.duckdb` - Database containing election data (needs to be downloaded separately)

## Technology Stack

- [Streamlit](https://streamlit.io/) - Web application framework
- [DuckDB](https://duckdb.org/) - Embedded analytics database
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [LangChain](https://python.langchain.com/) - AI/LLM integration


## Acknowledgements

- Data source: Komisi Pemilihan Umum (KPU) Indonesia
- Original data scraper: [pemilu-2024-scraper](https://github.com/terryds/pemilu-2024-scraper)
