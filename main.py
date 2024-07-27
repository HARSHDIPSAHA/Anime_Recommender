import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Load the models and data
table = pickle.load(open('models/table.pkl','rb'))
data = pickle.load(open('models/anime_data.pkl','rb'))
similarity_scores = pickle.load(open('models/similarity_scores.pkl','rb'))

def recommend(anime):
    # index fetch
    index = np.where(table.index == anime)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    recommendations = {
        "Name": [],
        "Other name": [],
        "Abstract": [],
        "Genre": [],
        "Image URL": []
    }
    
    for i, (anime_index, score) in enumerate(similar_items, start=1):
        temp_df = data[data['English name'] == table.index[anime_index]]
        name = temp_df['Name'].drop_duplicates().values[0]
        other_name = temp_df['Other name'].drop_duplicates().values[0]
        abstract = temp_df['Synopsis'].drop_duplicates().values[0]
        genres = temp_df['Genres'].drop_duplicates().values[0]
        image_url = temp_df['Image URL'].drop_duplicates().values[0]  # Assuming 'Image URL' is the column name
        
        recommendations["Name"].append(name)
        recommendations["Other name"].append(other_name)
        recommendations["Abstract"].append(abstract)
        recommendations["Genre"].append(genres)
        recommendations["Image URL"].append(image_url)
    
    return recommendations

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit app
st.title("Anime Recommendation System")

# Load CSS
load_css("styles.css")

# User input
anime_input = st.text_input("Enter an anime name:")

if st.button("Recommend"):
    if anime_input:
        recommendations = recommend(anime_input)
        st.write("Here are the top 5 recommended anime:")

        for i in range(len(recommendations["Name"])):
            st.markdown(f"""
            <div class="recommendation-card">
                <div class="image-container">
                    <img src="{recommendations['Image URL'][i]}" alt="{recommendations['Name'][i]}">
                </div>
                <div class="info-container">
                    <h3>{i+1}. {recommendations['Name'][i]}</h3>
                    <p><strong>Other name:</strong> {recommendations['Other name'][i]}</p>
                    <p><strong>Abstract:</strong> {recommendations['Abstract'][i]}</p>
                    <p><strong>Genre:</strong> {recommendations['Genre'][i]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Please enter an anime name to get recommendations.")

# About section
st.markdown("""
<div class="about-section">
    <h2>About</h2>
    <p>This Anime Recommendation System uses a dataset of anime titles, genres, and synopses to recommend similar anime based on your input.</p>
    <p>Rather than simply based on similar story and content, this system uses the data of various users and then give suggestions,<a href="https://developers.google.com/machine-learning/recommendation/collaborative/basics"> Collaborative filtering </a>
    <p><strong>Dataset Used:</strong> <a href="https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset">Kaggle Dataset</a></p>
    <p><strong>Feedback:</strong> If you have any feedback or suggestions, please feel free to <a href="mailto:harshdipsaha95@gmail.com">email me</a>.</p>
</div>
""", unsafe_allow_html=True)
