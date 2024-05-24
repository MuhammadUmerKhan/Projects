import emoji
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df =  df[df['user'] == selected_user]

    new_messages = df.shape[0]
    words = []
    for messages in df['message']:
        words.extend(messages.split())
    
    num_media_messages = df[df['message'] == "<Media omitted>\n"].shape[0]
    
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
        
    return new_messages, len(words), num_media_messages, len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head()
    
    if 'group_notification' in x:
        x = x.drop('group_notification')
        
    active_user_data = round(((df['user'].value_counts()/df.shape[0]) * 100), 2).reset_index().rename(columns={'index':'Names', 'user':"Percentage"})
    
    return x, active_user_data

def create_wordcloud(selected_user, df):
    f = open('./stop_hinglish.txt', 'r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500, height=500, max_font_size=110, background_color='black')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_used_words(selected_user, df):
    
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(7))
    most_common_df = most_common_df.rename(columns={0:'Words', 1:'Repeated'})
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df = emoji_df.rename(columns={0:'Emoji', 1:'Repitition'})
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_name', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " " + str(timeline['year'][i]))
    timeline['time'] = time
    
    return timeline