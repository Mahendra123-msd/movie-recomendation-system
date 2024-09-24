import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the similarity matrix
similarity = pickle.load(open('similarity_file.pkl', 'rb'))

# Function to load data
@st.cache_data
def load_data(movies_file, credits_file, new_file):
    movies = pd.read_csv(movies_file)
    credits = pd.read_csv(credits_file)
    new = pd.read_csv(new_file)
    return movies, credits, new

# Function to generate movie recommendations
def recommend(movie, new_df):
    movie = movie.capitalize()
    try:
        index = new_df[new_df['title'] == movie].index[0]
    except IndexError:
        return ["Movie not found in dataset"]
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    # Get the top 5 recommendations
    recommended_movies = [new_df.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies  # Correctly return the list of recommended movies

# Streamlit App
def main():
    st.title("Movie Recommendation System")

    # Upload movie, credit, and new file
    movies_file = st.file_uploader("Upload Movies CSV", type="csv")
    credits_file = st.file_uploader("Upload Credits CSV", type="csv")
    new_file = st.file_uploader("Upload new file CSV", type="csv")

    if movies_file and credits_file and new_file:
        # Load data
        movies, credits, new_df = load_data(movies_file, credits_file, new_file)

        # Display a dropdown for selecting a movie
        movie_list = new_df['title'].values
        selected_movie = st.selectbox("Select a Movie", movie_list)

        # Show recommendations when a movie is selected
        if st.button("Show Recommendations"):
            recommendations = recommend(selected_movie, new_df)
            st.write("Recommended Movies:")
            for movie in recommendations:
                st.write(movie)

if __name__ == "__main__":
    main()
