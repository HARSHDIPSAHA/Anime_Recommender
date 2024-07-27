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
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    
    recommendations = {
        "English name": [],
        "Abstract": [],
        "Genre": []
    }
    
    for i, (anime_index, score) in enumerate(similar_items, start=1):
        temp_df = data[data['English name'] == table.index[anime_index]]
        name = temp_df['English name'].drop_duplicates().values[0]
        abstract = temp_df['Synopsis'].drop_duplicates().values[0]
        genres = temp_df['Genres'].drop_duplicates().values[0]
        
        recommendations["English name"].append(name)
        recommendations["Abstract"].append(abstract)
        recommendations["Genre"].append(genres)
    
    return recommendations

# Streamlit app
st.title("Anime Recommendation System")

# User input
anime_input = st.text_input("Enter an anime name:")

if st.button("Recommend"):
    if anime_input:
        recommendations = recommend(anime_input)
        st.write("Here are the top 5 recommended anime:")

        for i in range(len(recommendations["English name"])):
            st.markdown(f"### {i+1}. {recommendations['English name'][i]}")
            st.write(f"**Abstract:** {recommendations['Abstract'][i]}")
            st.write(f"**Genre:** {recommendations['Genre'][i]}")
            st.write("---")
    else:
        st.write("Please enter an anime name to get recommendations.")
