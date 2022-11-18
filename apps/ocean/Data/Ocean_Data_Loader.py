import pandas as pd
import pathlib

#Set the path to the data we want
csv_path = pathlib.Path(__file__).parent / 'dataframe.csv'
#classify according to season
def f(row):
    if row['date'].month in range(3, 6):
        val = 'autumn'
    elif row['date'].month in range(6, 9):
        val = 'winter'
    elif row['date'].month in range(9, 12):
        val = 'spring'
    else:
        val = 'summer'
    return val

def create_df():
    #Create the DataFrame
    df= pd.read_csv(csv_path)
    #Process data to remove errors
    df['date'] = df['date'].replace('201900809', '20190809')
    df['date'] = pd.to_datetime(df.date, format='%Y%m%d').dt.date
    df['season'] = df.apply(f, axis=1)
    seasons = df['season'].unique()
    season = {}
    for i in seasons:
        subset = (df.loc[(df['season'] == i)]['date'].unique())
        season[i] = [str(x) for x in subset]
    return df,seasons