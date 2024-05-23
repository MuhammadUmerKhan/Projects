import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess_data(data)
    
    st.dataframe(df)
    
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall" )
    selected_user = st.sidebar.selectbox("Show Analysis wrt ", user_list)
    
    if st.sidebar.button('Show Analysis'):
        num_messages, words, num_media_shared, links_shared = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_shared)
        with col4:
            st.header("Links Shared")
            st.title(links_shared)
            
        
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x = helper.most_busy_user(df)
            col1, col2 = st.columns(2)
            