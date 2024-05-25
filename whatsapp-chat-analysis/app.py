import plotly.graph_objects as go
import plotly.express as px
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
    
    # st.dataframe(df)
    
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt ", user_list)
    
    if st.sidebar.button('Show Analysis'):
        num_messages, words, num_media_shared, links_shared = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)
        st.title("Top Statistics")
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
        # timeline
        st.title("Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig = go.Figure(data=go.Scatter(x=timeline['time'], y=timeline['message'], mode='lines'))
        fig.update_layout(title='Timeline Plot',
                        xaxis_title='Time',
                        yaxis_title='Message')

        st.plotly_chart(fig)
                
        # Daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        # st.title("Daily Timeline")
        fig = go.Figure(data=go.Scatter(x=daily_timeline['only_date'], y=daily_timeline['message'], mode='lines'))
        fig.update_layout(title='Daily Timeline Plot',
                        xaxis_title='Date',
                        yaxis_title='Message')

        st.plotly_chart(fig)
        # weekly activity timeline
        
        st.title("Activity Map")
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=busy_day.index, y=busy_day.values
        ))
        fig.update_layout(
            title='Busy day in Week Day',
            xaxis=dict(tickangle=90),
            autosize=False,
            width=600,  # Adjust the width
            height=400,  # Adjust the height
            margin=dict(l=50, r=50, b=100, t=100, pad=4)
        ); st.plotly_chart(fig)
        
        st.header("Most Busy Month")
        busy_month = helper.month_activity_map(selected_user, df)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=busy_month.index, y=busy_month.values
        ))
        fig.update_layout(
            title='Busy Month',
            xaxis=dict(tickangle=90),
            autosize=False,
            width=600, 
            height=400,
            margin=dict(l=50, r=50, b=100, t=100, pad=4)
        ); st.plotly_chart(fig) 
        
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        
        
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, active_user_data = helper.most_busy_user(df)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=x.index, y=x.values
            ))
            fig.update_layout(
                title='Most Busy User',
                xaxis=dict(tickangle=90),
                autosize=False,
                width=600,  # Adjust the width
                height=400,  # Adjust the height
                margin=dict(l=50, r=50, b=100, t=100, pad=4)
            )
                            
            # st.dataframe(active_user_data)
            st.plotly_chart(fig)
            
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        most_common_df = helper.most_common_used_words(selected_user, df)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=most_common_df['Repeated'], 
            y=most_common_df['Words'], 
            orientation='h'
        ))

        fig.update_layout(
            title='Most Used Words',
            xaxis=dict(
                tickangle=90,
                showgrid=True 
            ),
            yaxis=dict(
                showgrid=True 
            ),
            autosize=False,
            width=600,
            height=400,
            margin=dict(l=50, r=50, b=100, t=100, pad=4)
        )

        st.plotly_chart(fig)
        
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = px.pie(
                emoji_df.head(), 
                values=emoji_df['Repitition'][:5],
                names=emoji_df['Emoji'][:5], 
                title='Emoji Usage',
                # hole=0.1, 
            )
            fig.update_traces(textinfo='label+percent', textposition='inside')
            fig.update_layout(
                autosize=False,
                width=400,  # Adjust the width
                height=400,  # Adjust the height
                margin=dict(l=50, r=50, b=50, t=50, pad=4)
            )
            st.plotly_chart(fig)
