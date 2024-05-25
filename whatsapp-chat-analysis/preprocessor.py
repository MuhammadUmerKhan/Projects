import re
import pandas as pd
def preprocess_data(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\u202f?[APMapm]{2} - '

    split_content = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    df = pd.DataFrame({'user_message':split_content, 'message_date':dates})
    
    date_format = '%m/%d/%y, %I:%M\u202f%p - '
    df['message_date'] = pd.to_datetime(df['message_date'], format=date_format)
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    user = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]: # user name
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('group_notification')
            messages.append(entry[0])
            
    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_name'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['only_data'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df.rename(columns={'only_data':'only_date'}, inplace=True)
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    period = []
    for hr in df[['day_name', 'hour']]['hour']:
        if hr == 23:
            period.append(str(hr) + '-' + str('00'))
        elif hr == 0:
            period.append(str('00') + '-' + str(hr+1))
        else:
            period.append(str(hr) + '-' + str(hr+1))
    df['period'] = period
    return df