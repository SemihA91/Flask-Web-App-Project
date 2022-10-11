# Run this app with `python dash_app.py` and visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import html
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import csv

geo = Nominatim(user_agent="test_app",  timeout=1000000)
# rgeocode = RateLimiter(geo.reverse, min_delay_seconds=0.01)
f = open('countries.csv','w',newline='')
writer = csv.writer(f)

df = pd.read_csv("newMet2.csv")

#df = df.head(10)
# print(df)
# df.drop(0, inplace = True)
# print(df)


countries = []



for i in range(len(df['reclat'])):
    lat = str(df['reclat'][i])
    long = str(df['reclong'][i])

    lat_long = lat + ',' + long
    loc = geo.reverse(lat_long,language='en')
    print("Processing number {}".format(i))
    try:
        countries.append(loc.raw['address'].get('country',''))
        writer.writerow([loc.raw['address'].get('country','')+','])
    except:
        print("DROPPING LINE {}".format(i))
        df.drop(i, inplace = True)
        
   
df['countries'] = countries
df.to_csv('meteor_countries.csv')
f.close()








# app = dash.Dash(__name__)

# app.layout = html.Div(children=[
#     html.H1(children='Countries with the Largest Number of Meteorite Landings'),

# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)