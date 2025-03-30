# IMDB

This project focuses on scraping IMDb's 2024 Movies page to extract movie details and store the data in CSV and SQL formats. The data is scraped using Selenium, processed, and stored for future analysis. The extracted data includes movie names, genres, ratings, voting counts, and durations. The project also provides a mechanism to save the data in individual CSV files by genre and combine them into a single dataset for SQL storage.

# Project Deliverables

This project aims to scrape, store, and visualize IMDb 2024 movie data. It includes several components:

1. **Data Scraping:** The data is scraped using Selenium from IMDb's 2024 movies page, extracting movie names, genres, ratings, voting counts, and durations.

2. **Data Storage:** The data is stored both in genre-wise CSV files and in an SQL database for easy querying.

3. **Python Scripts:** Used for data scraping, cleaning, merging, and database interaction.

4. **Streamlit Application:** A real-time interactive dashboard that allows users to explore and visualize the movie data.

# Jupyter Notebook: IMBD_DataScrap.ipynb

* **Data Scraping:**
The notebook scrapes movie data from IMDb using Selenium. The movie details (name, genre, ratings, voting counts, and duration) are extracted and saved in separate CSV files for each genre.
*   **Data Cleaning:**
The data is cleaned by ensuring that any missing values or inconsistencies are handled properly.
*  **Combining CSVs:**
Once the CSV files for each genre are created, they are merged into a single DataFrame that contains the complete movie dataset.
*   **Storing Data in SQL Database:**
After cleaning and merging the data, the final dataset is stored in an SQL database (MySQL). This step involves setting up a MySQL connection and inserting the cleaned data into the database, making it ready for querying and analysis.

**To run the notebook, execute the following steps:**

  * Open IMBD_DataScrap.ipynb in Jupyter Notebook.
  * Run the cells in the notebook sequentially to scrape, clean, and store the data.

**Prerequisites for Running the Notebook:**

* Selenium: This is for scraping the IMDb website.
* Pandas: For data cleaning and manipulation.
* MySQL Connector: For connecting and interacting with the MySQL database.

# Python file: prosimdb.py

This code provides interactive visualizations and filtering options for IMDb movie data stored in a MySQL database. Users can explore various aspects of the data, such as top-rated movies, genre distributions, movie durations, voting trends, and more.

**Features: Interactive Visualizations:**

  1. Top 10 Movies by Rating and Voting Counts.
  2. Genre Distribution.
  3. Average Duration by Genre.
  4. Voting Trends by Genre.
  5. Movie Rating Distribution.
  6. Genre-based Rating Leaders.
  7. Popular Genres by Voting.
  8. Duration Extremes (Shortest and Longest Movies).
  9. Ratings by Genre (Heatmap).
  10. Correlation Analysis between Ratings and Voting Counts.

**Interactive Filtering:**

  1. Filter movies based on IMDb ratings, voting counts, genres, and duration.
  2. Use sliders and dropdowns for easy data filtering.

**Requirements**

  * Python 3.x
  * MySQL database containing movie data

**Required Python libraries:**

  * streamlit
  * pandas
  * mysql-connector-python
  * matplotlib
  * seaborn

**Note: Please ensure to save all the required files in a same folder to avoid any path related issues.**
