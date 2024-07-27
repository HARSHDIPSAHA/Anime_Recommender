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
        "Genre": []
    }
    
    for i, (anime_index, score) in enumerate(similar_items, start=1):
        temp_df = data[data['English name'] == table.index[anime_index]]
        name = temp_df['Name'].drop_duplicates().values[0]
        other_name = temp_df['Other name'].drop_duplicates().values[0]
        abstract = temp_df['Synopsis'].drop_duplicates().values[0]
        genres = temp_df['Genres'].drop_duplicates().values[0]
        
        recommendations["Name"].append(name)
        recommendations["Other name"].append(other_name)
        recommendations["Abstract"].append(abstract)
        recommendations["Genre"].append(genres)
    
    return recommendations

# Streamlit app
st.title("Anime Recommendation System")

# User input
anime_input = st.text_input("Enter an anime name:")

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if st.button("Recommend"):
    st.session_state.current_index = 0  # Reset to the first recommendation
    if anime_input:
        st.session_state.recommendations = recommend(anime_input)
        st.write("Here is your recommended anime:")

        recommendation = st.session_state.recommendations
        idx = st.session_state.current_index

        st.markdown(f"### {idx+1}. {recommendation['Name'][idx]}")
        st.write(f"**Other name:** {recommendation['Other name'][idx]}")
        st.write(f"**Abstract:** {recommendation['Abstract'][idx]}")
        st.write(f"**Genre:** {recommendation['Genre'][idx]}")
        st.write("---")
        
        if idx < len(recommendation["Name"]) - 1:
            if st.button("Next"):
                st.session_state.current_index += 1
                st.experimental_rerun()
    else:
        st.write("Please enter an anime name to get recommendations.")

if 'recommendations' in st.session_state:
    recommendation = st.session_state.recommendations
    idx = st.session_state.current_index
    if idx < len(recommendation["Name"]) and idx >= 0:
        st.markdown(f"### {idx+1}. {recommendation['Name'][idx]}")
        st.write(f"**Other name:** {recommendation['Other name'][idx]}")
        st.write(f"**Abstract:** {recommendation['Abstract'][idx]}")
        st.write(f"**Genre:** {recommendation['Genre'][idx]}")
        st.write("---")
        
        if idx < len(recommendation["Name"]) - 1:
            if st.button("Next"):
                st.session_state.current_index += 1
                st.experimental_rerun()
    elif idx >= len(recommendation["Name"]):
        st.write("No more recommendations.")
