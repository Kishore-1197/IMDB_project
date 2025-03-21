IMDb 2024 Data Scraping and Visualization

Project Overview

This project focuses on extracting and analyzing movie data from IMDb for the year 2024. It involves web scraping IMDb's latest movies, storing the collected data in an SQLite database, and building interactive visualizations using Streamlit. The goal is to explore trends in ratings, genres, voting patterns, and movie durations while providing a user-friendly filtering mechanism for detailed insights.

File Structure

data_scrape.ipynb – Jupyter Notebook for scraping IMDb 2024 movie data using Selenium.

data_visual.py – Streamlit-based application for interactive visualizations and data filtering.

Setup and Installation

Clone the repository:

git clone https://github.com/your-username/imdb-2024-analysis.git
cd imdb-2024-analysis

Install dependencies:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run data_visual.py

Features

IMDb Data Scraping

Uses Selenium to extract movie information such as:

Movie Title

IMDb Rating

Number of Votes

Genre

Duration

Stores the scraped data into an SQLite database (IMDB.db).

Interactive Visualizations (Streamlit App)

Top 10 movies by rating and votes

Genre distribution and popularity

Average movie duration per genre

Voting trends by genre

Rating distribution histogram

Top-rated movies for each genre

Most popular genres by voting (Pie Chart)

Longest and shortest movies

Heatmap for average ratings across genres

Correlation analysis between votes and ratings

Movie Filtering System

Users can filter movies based on:

Duration: <2 hrs, 2-3 hrs, >3 hrs

Rating Range: Select a minimum rating threshold

Number of Votes: Low, Medium, High engagement

Genre Selection: Choose a specific genre to explore

Technologies Used

Python 

Selenium (for web scraping)

SQLite (for database storage)

Pandas & Seaborn (for data analysis)

Matplotlib (for charts)

Streamlit (for interactive visualizations)

Next Steps

Implement real-time data updates

Add more advanced filtering options

Improve visualization aesthetics and interactivity

License

This project is open-source and available under the MIT License.

