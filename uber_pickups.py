import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure

st.title('Uber pickups in NYC')

# Fetch some data
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
#data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache_data)")

# Inspect the raw data
#st.subheader('Raw data')
#st.write(data)
# Use a button to toggle data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Draw a histogram
st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

# # bokeh
# from bokeh.plotting import figure, show
#
# rng = np.random.default_rng()
# x = rng.normal(loc=0, scale=1, size=1000)
#
# p = figure(width=670, height=400, toolbar_location=None,
#            title="Normal (Gaussian) Distribution")
#
# # Histogram
# bins = np.linspace(-3, 3, 40)
# hist, edges = np.histogram(x, density=True, bins=bins)
# p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
#          fill_color="skyblue", line_color="white",
#          legend_label="1000 random samples")
#
# # Probability density function
# x = np.linspace(-3.0, 3.0, 100)
# pdf = np.exp(-0.5*x**2) / np.sqrt(2.0*np.pi)
# p.line(x, pdf, line_width=2, line_color="navy",
#        legend_label="Probability Density Function")
#
# p.y_range.start = 0
# p.xaxis.axis_label = "x"
# p.yaxis.axis_label = "PDF(x)"
#
# #show(p)
# st.bokeh_chart(p, use_container_width=True)

# Plot data on a map
st.subheader('Map of all pickups')

#st.map(data)

#hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)




