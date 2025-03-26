# Import necessary libraries for the app
import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Database connection details (you should replace these with your actual credentials)
connection = {
    'host': '',
    'user': 'root',
    'password': '',
    'database': 'imdb',
}

# Function to display top 10 movies by rating and voting counts
def display_top_movies_from_db():
    st.subheader("1. Top 10 Movies by Rating and Voting Counts")

    # Connect to the MySQL database
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # Query to get top 10 movies sorted by rating and voting counts
    query = """
        SELECT title, rating, votings
        FROM movies
        ORDER BY rating DESC, votings DESC
        LIMIT 10;
    """

    # Execute query and fetch the result
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert result into a pandas DataFrame for better formatting
    df = pd.DataFrame(results, columns=['Title', 'Rating', 'Votes'])
    df.index = df.index + 1  # Adjust the index to start from 1

    # Close the database connection
    cursor.close()
    conn.close()

    # Check if the DataFrame is empty, then display a warning message
    if df.empty:
        st.warning("No movie data found.")
        return

    # Display the DataFrame in the Streamlit app
    st.dataframe(df)

# Function to plot the distribution of movies by genre
def plot_genre_counts():
    # Connect to the database
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # Query to count movies by genre
    query = """
        SELECT genres, COUNT(*) as gcount
        FROM movies
        GROUP BY genres
        ORDER BY gcount DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert results into a pandas DataFrame
    df = pd.DataFrame(results, columns=['Genre', 'Movie Count'])

    # Close the connection
    cursor.close()
    conn.close()

    # Check if the DataFrame is empty
    if df.empty:
        st.warning("No movie data found.")
        return

    # Display subheader for the genre distribution plot
    st.subheader("2. Genre Distribution")

    # Create a bar plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['Genre'], df['Movie Count'], color='skyblue')
    ax.set_xlabel('Genres')
    ax.set_ylabel('Movie Count')
    ax.set_title('Genre Distribution')
    st.pyplot(fig)  # Display the plot in Streamlit

# Function to plot average duration by genre
def plot_genre_durationavg():
    # Connect to the database
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # Query to get the average movie duration by genre
    query = """
        SELECT genres, AVG(duration) as avg_duration
        FROM movies
        GROUP BY genres
        ORDER BY avg_duration DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert results into a pandas DataFrame
    df = pd.DataFrame(results, columns=['Genre', 'Movie Duration(MINS)'])

    # Close the connection
    cursor.close()
    conn.close()

    # Check if the DataFrame is empty
    if df.empty:
        st.warning("No movie data found.")
        return

    # Display subheader for the average duration plot
    st.subheader("3. Average Duration by Genre")

    # Create a horizontal bar plot using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['Genre'], df['Movie Duration(MINS)'], color='salmon')
    ax.set_xlabel('Movie Duration (MINS)')
    ax.set_ylabel('Genres')
    ax.set_title('Average Duration by Genre')
    st.pyplot(fig)  # Display the plot

# Function to plot voting trends by genre
def plot_voting_trends():
    st.subheader("4. Voting Trends by Genre")

    # Connect to the database
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # SQL query to calculate average voting counts per genre
    query = """
        SELECT genres, AVG(votings) as avg_votes
        FROM movies
        GROUP BY genres
        ORDER BY avg_votes DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['Genre', 'Average Votes'])

    # Close the connection
    cursor.close()
    conn.close()

    # Check if the DataFrame is empty
    if df.empty:
        st.warning("No genre data found.")
        return

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))  
    ax.bar(df['Genre'], df['Average Votes'], color='wheat')

    # Add titles and labels
    ax.set_title("Average Voting Counts by Genre", fontsize=16)
    ax.set_xlabel("Genres", fontsize=12)
    ax.set_ylabel("Average Votes", fontsize=12)

    # Display the plot
    st.pyplot(fig)

# Function to plot rating distribution
def rating_distribution():
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    st.subheader("5. Rating Distribution")

    # Query to fetch all movie ratings
    query = """
    SELECT rating
    FROM movies;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Check if there is data to process
    if not results:
        st.warning("No rating data found.")
        cursor.close()
        conn.close()
        return

    # Extract ratings into a list
    ratings = [result[0] for result in results]
    df_ratings = pd.DataFrame({'Rating': ratings})

    # Create a histogram of ratings
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_ratings['Rating'], bins=15, color='lightgreen')
    ax.set_title('Movie Rating Distribution (Histogram)')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    cursor.close()
    conn.close()

# Function to display the highest-rated movies by genre
def high_rank_genre():
    st.subheader("6. Genre-Based Rating Leaders")

    # Connect to the database
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # SQL query to get the highest-rated movie in each genre
    query = """
        SELECT title,genres,rating
        FROM movies
        WHERE (genres,rating) 
        IN (SELECT genres, MAX(rating) FROM movies GROUP BY genres);
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the results into a pandas DataFrame
    df = pd.DataFrame(results, columns=['Title', 'Genres', 'Rating'])
    df.index = df.index + 1

    # Close the connection
    cursor.close()
    conn.close()

    # Check if the DataFrame is empty
    if df.empty:
        st.warning("No movie data found.")
    else:
        st.dataframe(df)


def popular_genre(): 
    st.subheader("7. Most Popular Genres by Voting")

    # Establish the database connection
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # SQL query to find popular genre by summing votes
    query = """
        SELECT genres, SUM(votings) as total_vote
        FROM movies
        GROUP BY genres
        ORDER BY total_vote DESC;
    """

    # Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()

    # Read the data directly into a pandas DataFrame
    df = pd.read_sql(query, conn)  
    if not df.empty:
        # Create a list of light colors for the pie chart
        colors = sns.color_palette('pastel') 
        
        # Create pie chart directly from DataFrame
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#f0f0f0')  # Set background color of the figure
        ax.set_facecolor('#ffffff')  # Set background color of the pie chart area

        # Create pie chart with light colors and display percentage
        ax.pie(df['total_vote'], autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
        ax.axis('equal')  # Ensure the pie chart is circular
        ax.legend(df['genres'], title="Genres", loc="upper left", bbox_to_anchor=(1, 1))  # Add a legend for genres
        
        # Display the pie chart
        st.pyplot(fig)   
    else:
        st.write("No results found.")
    
    cursor.close()  # Close the cursor after use

def duration_split():
    st.subheader("8. Duration Extremes")

    # Establish the database connection
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # SQL query to find the shortest and longest movie durations
    query = """(
            SELECT title, duration
            FROM movies
            ORDER BY duration ASC
            LIMIT 1)
        UNION(
            SELECT title, duration
            FROM movies
            ORDER BY duration DESC
            LIMIT 1);
    """

    cursor.execute(query)
    results = cursor.fetchall()

    # Extract the shortest and longest movie
    shortest_movie = results[0]  # The shortest movie (first row)
    longest_movie = results[1]   # The longest movie (second row)

    # Display the results using styled cards
    st.markdown("<h5 style='color: coral; font-weight: bold;'>Shortest Movie:</h3>", unsafe_allow_html=True)
    with st.container():
        st.write(f"**Title:** {shortest_movie[0]}")
        st.write(f"**Duration:** {shortest_movie[1]} minutes")

    st.markdown("<h5 style='color: coral; font-weight: bold;'>Longest Movie:</h3>", unsafe_allow_html=True)
    with st.container():
        st.write(f"**Title:** {longest_movie[0]}")
        st.write(f"**Duration:** {longest_movie[1]} minutes")
    
    cursor.close()  # Close cursor after fetching the data
    conn.close()    # Close the connection after use

def rating_genre():
    st.subheader("9. Ratings by Genre")

    # Establish the database connection
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # SQL query to calculate average ratings per genre
    query = """
            SELECT genres, AVG(rating) AS avg_rating
            FROM movies
            GROUP BY genres
            ORDER BY avg_rating DESC;
        """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()  # Close the cursor after fetching the data
    conn.close()    # Close the connection

    # Check if any results exist
    if results:
        # Convert results into a pandas DataFrame
        df = pd.DataFrame(results, columns=["Genre", "Average Rating"])

        # Pivot the data for heatmap visualization
        genre_pivot = df.pivot_table(index="Genre", values="Average Rating", aggfunc="mean")

        # Plot the heatmap using seaborn
        plt.figure(figsize=(10, 6))
        sns.heatmap(genre_pivot.T, annot=True, cmap="Set2", cbar=True, fmt='.2f')

        # Display the plot
        st.pyplot(plt)

    else:
        st.write("No data found for ratings by genre.")

def correlation_analysis():
    st.subheader("10. Correlation Analysis")

    # Establish the database connection
    conn = mysql.connector.connect(**connection)
    cursor = conn.cursor()

    # SQL query to select ratings and voting counts for correlation analysis
    query = """
            SELECT rating, votings
            FROM movies
        """
    cursor.execute(query)
    results = cursor.fetchall()

    # Convert the results into a pandas DataFrame
    df = pd.DataFrame(results, columns=["rating", "voting_count"])

    # Plotting a scatter plot for correlation between voting count and rating
    plt.figure(figsize=(10, 6))
    plt.scatter(df['voting_count'], df['rating'], alpha=0.6, color='b')

    # Adding titles and labels
    plt.title("Scatter Plot: Ratings vs Voting Counts", fontsize=14)
    plt.xlabel("Voting Count", fontsize=12)
    plt.ylabel("Rating", fontsize=12)

    # Display the plot
    st.pyplot(plt)

    # Close the connection
    cursor.close()
    conn.close()

def animated_header(text, color="#f01e2c"):
    # CSS animation for header text fade-in effect
    animation_css = f"""
    <style>
    .animated-header {{
        text-align: center;
        color: {color};
        animation: fadeIn 4s ease-in-out;
    }}
    @keyframes fadeIn {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}
    </style>
    """
    st.markdown(animation_css, unsafe_allow_html=True)  # Apply the animation CSS
    st.markdown(f"<h1 class='animated-header'>{text}</h1>", unsafe_allow_html=True)  # Display animated header

# Define the pages
def visual():
    # Visualizations page content
    animated_header("IMDB Interactive Visualizations")
    display_top_movies_from_db()  # Top movies display function
    plot_genre_counts()  # Genre count display function
    plot_genre_durationavg()  # Genre duration (average) display
    plot_voting_trends()  # Voting trends visualization
    rating_distribution()  # Rating distribution display
    high_rank_genre()  # High rank genre display
    popular_genre()  # Most popular genre by voting
    duration_split()  # Duration extremes display
    rating_genre()  # Ratings by genre heatmap
    correlation_analysis()  # Correlation between ratings and voting counts

def filter():
    # Filtering page content
    animated_header("IMDB Interactive Filtering")
    try:
        conn = mysql.connector.connect(**connection)
        cursor = conn.cursor()
        query = "SELECT * FROM movies"  # Query to fetch all movies
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    # Check if data is loaded correctly
    if df.empty:
        st.error("No data loaded from the database.")
        return

    st.sidebar.header("Filter Options")

    # Sidebar filtering options
    duration_options = ["< 2 hrs", "2-3 hrs", "> 3 hrs"]
    selected_duration = st.sidebar.multiselect("Duration (Hrs)", duration_options)

    # Set the rating and voting range for the sliders
    min_rating = float(df["rating"].min())
    max_rating = float(df["rating"].max())
    selected_rating = st.sidebar.slider("IMDb Rating", min_value=min_rating, max_value=max_rating, value=(min_rating, max_rating))

    min_votes = int(df["votings"].min())
    max_votes = int(df["votings"].max())
    selected_votes = st.sidebar.slider("Voting Counts", min_value=min_votes, max_value=max_votes, value=(min_votes, max_votes))

    # Extract genres from the dataframe for the genre filter
    all_genres = df["genres"].str.split(", ").explode().str.strip().unique()
    selected_genres = st.sidebar.multiselect("Genre", all_genres)

    # Apply filters to the dataframe
    filtered_df = df.copy()

    # Filter by duration
    duration_filters = []
    if "< 2 hrs" in selected_duration:
        duration_filters.append(filtered_df["duration"] < 120)
    if "2-3 hrs" in selected_duration:
        duration_filters.append((filtered_df["duration"] >= 120) & (filtered_df["duration"] <= 180))
    if "> 3 hrs" in selected_duration:
        duration_filters.append(filtered_df["duration"] > 180)

    if duration_filters:
        filtered_df = filtered_df[pd.concat(duration_filters, axis=1).any(axis=1)]

    # Filter by rating and voting count
    filtered_df = filtered_df[(filtered_df["rating"] >= selected_rating[0]) & (filtered_df["rating"] <= selected_rating[1])]
    filtered_df = filtered_df[(filtered_df["votings"] >= selected_votes[0]) & (filtered_df["votings"] <= selected_votes[1])]
    filtered_df = filtered_df[filtered_df["genres"].apply(lambda x: any(genre in x for genre in selected_genres))]

    # Display the filtered dataframe
    st.subheader("Filtered Movie Data")
    st.dataframe(filtered_df)

# Sidebar navigation
page = st.sidebar.selectbox("Data Scraping and Visualizations", ["Interactive Visualizations", "Interactive Filtering"])

# Display the appropriate page based on the sidebar selection
if page == "Interactive Visualizations":
    visual()
elif page == "Interactive Filtering":
    filter()