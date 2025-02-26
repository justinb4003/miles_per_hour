# A quick Streamlit app to show baby names per hour over time
import altair as alt
import streamlit as st
import pandas as pd

# This data is published by the Social Security Administration in .txt format
# with a file for each available year. I've already downloaded and processed
# them into a big parquet file that has everything. It ends up being smaller
# than the sum of the individual files, which is nice.
baby_names = pd.read_parquet('baby_names.parquet')
baby_names['name'] = baby_names['name'].str.lower()

# Now we start actually drawing the page.
st.title('Miles Per Hour')
st.subheader('Baby names per hour over time')
babyname = st.text_input('Enter a name', 'Miles')

# Once we have the baby name we can filter the data to just that name
# and then group by year to get the total count for each year.
# We can then divide by the number of hours in a year to get the count per hour.
yourname = baby_names[baby_names['name'] == babyname.lower()]
yourname = yourname.groupby(['year', 'name']).sum('count').reset_index()
yourname['name_per_hour'] = yourname['count'] / (25 * 365)

# Finally, we can use Altair to draw a line chart of the data. Streamlit has
# a built in st.line_chart() that's nice and smple but it doesn't support
# all the features of Altair.

alt_chart = alt.Chart(yourname).mark_line().encode(
    x=alt.X('year:Q', axis=alt.Axis(format='d')),
    y='name_per_hour',
).properties(
    title=f'{babyname} per hour',
)
st.altair_chart(alt_chart, use_container_width=True)