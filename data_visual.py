import pandas as pd
import sqlite3 
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


try:
    conn = sqlite3.connect("IMDB.db")
except Exception as e:
    print("ERROR -> Database connection: ", e)

def visualizations():

    try:
        st.header("Top 10 Movies by Rating and Voting Counts")
        q = """WITH ranked_movies AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY Title ORDER BY Votes DESC, Rating DESC) AS rn
            FROM Movies)SELECT * FROM ranked_movies WHERE rn = 1 ORDER BY Votes DESC, Rating DESC LIMIT 10;"""
        a = pd.read_sql_query(q, conn)
        st.write("Highest Ratings and Significant Voting engagement")
        st.write(a[["Title", "Rating", "Votes"]].reset_index(drop=True))
    except Exception as e:
            st.warning(f"Error -> {e}")

    try:
        st.header("Genre Distribution")
        q = """SELECT Genre, COUNT(*) AS Count FROM Movies GROUP BY Genre ORDER BY Count DESC;"""
        a = pd.read_sql_query(q, conn)
        st.write("Movie Count by Genre")
        st.write(a)
    except Exception as e:
            st.warning(f"Error -> {e}")
    
    try:
        st.header("Average Duration of movies")
        q = """WITH converted_duration AS (
            SELECT Genre, (CAST(SUBSTR(Duration, 1, INSTR(Duration, '.') - 1) AS INTEGER) * 60 + 
            CAST(SUBSTR(Duration, INSTR(Duration, '.') + 1) AS INTEGER)) AS Duration_in_minutes
            FROM Movies WHERE Duration LIKE '%.%')
        SELECT Genre, ROUND(AVG(Duration_in_minutes), 2) AS "Avg Duration (min)"
        FROM converted_duration GROUP BY Genre ORDER BY "Avg Duration (min)";"""
        a = pd.read_sql_query(q, conn)
        st.write("Average Movie Duration per Genre") 
        st.write(a)
    except Exception as e:
            st.warning(f"Error -> {e}")

    try:
        st.header("Voting Trends by Genre")
        q = """SELECT Genre, ROUND(SUM(Votes) * 1.0 / COUNT(Title), 2) AS "Avg Votes Per Movie"
        FROM Movies GROUP BY Genre ORDER BY "Avg Votes Per Movie" DESC;"""
        b = pd.read_sql_query(q, conn)
        st.write("Average Voting Counts per Genre")
        st.write(b)
    except Exception as e:
            st.warning(f"Error -> {e}")

    try:
        st.header("Rating Distribution")
        q = """SELECT Rating FROM Movies WHERE Rating IS NOT NULL""" 
        ratings_data = pd.read_sql_query(q, conn)
        bin_edges = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bin_labels = [f"{bin_edges[i]} - {bin_edges[i+1]}" for i in range(len(bin_edges)-1)]
        bin_counts = pd.cut(ratings_data["Rating"], bins=bin_edges, labels=bin_labels, include_lowest=True).value_counts().sort_index()
        table_data = pd.DataFrame({"Bin Range": bin_counts.index, "Frequency": bin_counts.values})
        st.write("Histogram chart for Movie Ratings")
        st.table(table_data)
    except Exception as e:
        st.warning(f"Error -> {e}")

    try:
        st.header("Genre-Based Rating Leaders")
        q = """WITH ranked_movies AS (SELECT Genre, Title, Rating,
            RANK() OVER (PARTITION BY Genre ORDER BY Rating DESC) AS rank
            FROM Movies WHERE Rating IS NOT NULL )
        SELECT Genre, Title, Rating FROM ranked_movies
        WHERE rank = 1 ORDER BY Genre;"""
        a = pd.read_sql_query(q, conn)
        st.write("Top-Rated movie for each Genre")
        st.write(a.reset_index(drop=True))
    except Exception as e:
            st.warning(f"Error -> {e}")

    try:
        st.header("Most Popular Genres by Voting")
        st.subheader("Highest Total Voting counts in a Pie-Chart")
        q = """WITH genre_votes AS (SELECT Genre, SUM(Votes) AS total_votes
        FROM Movies WHERE Votes IS NOT NULL GROUP BY Genre),
        total AS (SELECT SUM(total_votes) AS grand_total FROM genre_votes)
        SELECT gv.Genre, gv.total_votes AS "Total Votes", 
        ROUND((gv.total_votes * 100.0) / t.grand_total, 1) AS "Percentage (%)"
        FROM genre_votes gv, total t ORDER BY gv.total_votes DESC; """
        d = pd.read_sql_query(q, conn)
        st.write("Highest Total Voting counts in a Pie-Chart")
        st.write(d)
    except Exception as e:
            st.warning(f"Error: {e}")
    
    try:
        st.header("Duration Extremes")
        q = """WITH Converted_Duration AS (SELECT Title, Genre, 
            CAST(Duration AS INTEGER) * 60 + ROUND((Duration - CAST(Duration AS INTEGER)) * 100, 0) AS Duration_Minutes 
            FROM Movies),
            Shortest AS (SELECT 'Shortest Movie' AS Label, Title, Genre, Duration_Minutes
            FROM Converted_Duration WHERE Duration_Minutes = (SELECT MIN(Duration_Minutes) FROM Converted_Duration)),
            Longest AS (SELECT 'Longest Movie' AS Label, Title, Genre, Duration_Minutes
            FROM Converted_Duration WHERE Duration_Minutes = (SELECT MAX(Duration_Minutes) FROM Converted_Duration))
            SELECT Label, Title, Genre, 
            CAST(Duration_Minutes / 60 AS INTEGER) || ' hr ' || CAST(Duration_Minutes % 60 AS INTEGER) || ' min' AS Duration 
            FROM Shortest UNION ALL SELECT Label, Title, Genre, 
            CAST(Duration_Minutes / 60 AS INTEGER) || ' hr ' || CAST(Duration_Minutes % 60 AS INTEGER) || ' min' AS Duration 
            FROM Longest;"""
        table_data = pd.read_sql_query(q, conn)
        st.write("Shortest and Longest Movies in Table view")
        st.table(table_data)
    except Exception as e:
            st.warning(f"Error: {e}")

    try:
        st.header("Ratings by Genre")
        q = """SELECT Genre, ROUND(AVG(Rating), 2) AS "Avg Rating" FROM Movies GROUP BY Genre
        ORDER BY "Avg Rating" DESC;"""
        a = pd.read_sql_query(q, conn)
        st.write("Heatmap to compare Average Ratings across Genres")
        st.table(a)
    except Exception as e:
            st.warning(f"Error: {e}")

    try:
        st.header("Correlation Analysis")
        q = """SELECT Rating, Votes FROM Movies ORDER BY Rating DESC, Votes DESC;"""
        a = pd.read_sql_query(q, conn)
        fig, ax = plt.subplots(figsize=(15, 10))
        sns.scatterplot(x=a["Rating"], y=a["Votes"], alpha=0.6, color="royalblue", edgecolor="black")
        ax.set_xlabel("Movie Ratings", fontsize=12)
        ax.set_ylabel("Total Votes", fontsize=12)
        ax.set_title("Relationship Between Ratings and Voting Counts")
        ax.grid(True, linestyle="--", alpha=0.6)
        st.write("Relationship between Ratings and Voting Counts ")
        st.pyplot(fig)
    except Exception as e:
            st.warning(f"Error: {e}")


def filtering():
    if conn:
        st.title("Filtering Page")
        st.header("Select Filters")
        d_o = ["click here to select range", "< 2 hrs", "2 - 3 hrs", "> 3 hrs"]
        r_o = [round(x * 0.1, 1) for x in range(0, 101)]
        v_o = ["click here to select range", "<= 1000", "1001 to 10,000 hrs", "> 10,000 hrs"]
        g_o = ["Action", "Adventure", "Animation", "Comedy", "Crime"]
        d = st.selectbox("Select a Duration Range (Hours)", options=d_o)
        r = st.select_slider("Select a minimum IMDb Rating", options=r_o, value=5.0)
        v = st.selectbox("Select a Votes Range", options=v_o)
        g = st.radio("Select a Genre", options=g_o, index=None)
        if (d == d_o[0]) or (v == v_o[0]) or (g == None):
            pass
        else:
            try:
                q = """SELECT Title, Genre, Rating, Votes, Duration FROM Movies
                WHERE Genre = :selected_genre AND Rating >= :min_rating AND (
                    (:duration_range = '< 2 hrs' AND Duration <= 2.0) 
                    OR (:duration_range = '2 - 3 hrs' AND Duration > 2.0 AND Duration <= 3.0) 
                    OR (:duration_range = '> 3 hrs' AND Duration > 3.0))
                AND ((:votes_range = '<= 1000' AND Votes <= 1000)
                    OR (:votes_range = '1001 to 10,000 hrs' AND Votes > 1000 AND Votes <= 10000)
                    OR (:votes_range = '> 10,000 hrs' AND Votes > 10000));"""
                f = pd.read_sql_query(q, conn, params={"selected_genre": g,"min_rating": r,"duration_range": d,"votes_range": v})
            except Exception as e:
                st.warning(f"Error -> query part {e}")
            if not f.empty:
                st.write(f"Gener-{g},Rating-{r} : 10.0, Duration - {d}, Votes: {v} -> count - {f.shape[0]}")
                st.dataframe(f)
            elif f.empty:
                st.write("# No Result Found")
            else:
                st.warning("Something wrong Re-run the code")
    else:
        st.warning("Database Connection is stopped")

st.sidebar.title("Page")
page = st.sidebar.radio("Go to", ["Data Visualizations", "Data Filter"])
if page == "Data Visualizations":
    visualizations()
elif page == "Data Filter":
    filtering()
