# import pandas as pd
# import streamlit as st
# import pickle
# import requests
#
# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?language=en-US&api_key=a94af0e349928f2dac998f893b268860'.format(movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500" + data['poster_path']
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#
#         #fetch poster from API
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_posters
#
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl','rb'))
#
# st.title('Movie Recommendation System')
#
# selected_movie_name = st.selectbox(
#     'How would you like to be contacted?',
#     movies['title'].values)
#
# if st.button('Recommend'):
#     names,posters = recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 = st.columns(5)
#
#     with col1:
#         st.header(names[0])
#         st.image(posters[0])
#
#     with col2:
#         st.header(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.header(names[2])
#         st.image(posters[2])
#
#     with col4:
#         st.header(names[3])
#         st.image(posters[3])
#
#     with col5:
#         st.header(names[4])
#         st.image(posters[4])


















# import pandas as pd
# import streamlit as st
# import pickle
# import requests
# import time  # ✅ Import time for adding sleep
#
# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?language=en-US&api_key=a94af0e349928f2dac998f893b268860'.format(movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500" + data['poster_path']
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#
#         # fetch poster from API
#         recommended_movies_posters.append(fetch_poster(movie_id))
#         time.sleep(0.2)  # ✅ Add delay after each API request to avoid being blocked
#
#     return recommended_movies, recommended_movies_posters
#
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('Movie Recommendation System')
#
# selected_movie_name = st.selectbox(
#     'How would you like to be contacted?',
#     movies['title'].values)
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 = st.columns(5)
#
#     with col1:
#         st.header(names[0])
#         st.image(posters[0])
#
#     with col2:
#         st.header(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.header(names[2])
#         st.image(posters[2])
#
#     with col4:
#         st.header(names[3])
#         st.image(posters[3])
#
#     with col5:
#         st.header(names[4])
#         st.image(posters[4])


import pandas as pd
import streamlit as st
import pickle
import requests
import time


# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&api_key=a94af0e349928f2dac998f893b268860'

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"


# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster and respect API rate limits
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)
        time.sleep(0.3)

    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.header(names[i])
            st.image(posters[i])

