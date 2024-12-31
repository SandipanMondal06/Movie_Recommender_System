import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch poster using API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f1ae16bb96d9f07469840b5bae1e5dd5')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Add background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://t3.ftcdn.net/jpg/08/99/71/24/240_F_899712407_OJjnKJD049hvsc7xXPnH9k72hQfyiqdY.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    h1 {{
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        color: #FFD700;
    }}
    .css-18e3th9 {{
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title('🎥 Movie Recommender System 🎬')

# Movie selection
Selected_movie_name = st.selectbox('Search your favourite movie:', movies['title'].values)

# Recommendation button
if st.button('Search'):
    names, posters = recommend(Selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(names[idx])
            st.image(posters[idx])

# Add footer with your name
st.markdown(
    """
    <style>
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        text-align: center;
        padding: 10px 0;
        font-size: 16px;
        color: white;
        font-family: 'Arial', sans-serif;
    }}
    </style>
    <div class="footer">
        Made with ❤️ by <strong>Sandipan Mondal</strong> using Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
