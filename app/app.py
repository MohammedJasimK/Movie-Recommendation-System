import streamlit as st
import pandas as pd
import requests
import pickle

# Load Data
with open(r"C:\Users\jasim\Data Science\My Project\Movie Recommendation System\model\movies recommender.pkl", 'rb') as file:
    df, similarity = pickle.load(file)


# Function to fetch poster and overview from TMDb API
def fetch_poster(movie_id):
    api_key = "034eda191f36fbb7d8b945ac57a47f81"    #use your api_key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    overview = data.get('overview', 'No description available.')
    rating = data.get('vote_average', 'N/A')
    release_date = data.get('release_date', 'Unknown')

    if poster_path:
        poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
    else:
        poster_url = "https://via.placeholder.com/500x750?text=No+Image"

    return poster_url, overview, rating, release_date

# Function to recommend movies
def recommend(movie, top_n=10):
    if movie not in df['title'].values:
        st.warning("Movie not found in the dataset.")
        return []

    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n + 1]

    recommendations = []
    for i in movies_list:
        recommendations.append({
            "title": df.iloc[i[0]]['title'],
            "movie_id": df.iloc[i[0]]['movie_id']
        })
    return recommendations

# Streamlit Page Configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Background and CSS Styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1524985069026-dd778a71c7b4");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: rgba(0,0,0,0);
}
h1, h2, h3, h4, h5, h6, p, span, div {
    color: #F5F5F5 !important;
}
img {
    border-radius: 12px;
    transition: transform 0.3s;
}
img:hover {
    transform: scale(1.05);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("About the App")
st.sidebar.info("""
This Movie Recommendation System suggests similar movies using a **content-based filtering** approach powered by 
cosine similarity.

Built by using Streamlit + TMDb API""")

st.sidebar.markdown("---")
st.sidebar.header("Settings")
st.sidebar.info("Adjust the slider to control how many similar movies you get.")
top_n = st.sidebar.slider("Number of recommendations", 5, 20, 10)

# Main Title and Movie Selector
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Movie Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Pick a movie and discover similar titles instantly!</p>", unsafe_allow_html=True)

selected_movie = st.selectbox('Select a movie', df['title'].values)

# Recommend Button
if st.button('Recommend'):
    with st.spinner('Fetching recommendations...'):
        recommendations = recommend(selected_movie, top_n)

    if not recommendations:
        st.error("No recommendations found. Try another movie.")

    else:
        st.subheader(f"Top {top_n} Movies similar to **{selected_movie}**")
        for i in range(0, len(recommendations), 5):
            cols = st.columns(5)
            for col, rec in zip(cols, recommendations[i:i + 5]):
                poster_url, overview, rating, release_date = fetch_poster(rec['movie_id'])
                with col:
                    st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                    st.image(poster_url, width=150)
                    st.markdown(f"**{rec['title']}**")
                    st.markdown(f"**Rating:** {rating}  \n**Release:** {release_date}")
                    with st.expander("Overview"):
                        st.write(overview)
                    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<hr>
<center>Developed by Mohammed Jasim | Powered by Streamlit & TMDb API</center>
""", unsafe_allow_html=True)
