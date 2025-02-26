import altair as alt
import streamlit as st
import pandas as pd

baby_names = pd.read_parquet('baby_names.parquet')
baby_names['name'] = baby_names['name'].str.lower()

st.title('Miles Per Hour')
st.subheader('Baby names per hour over time')
babyname = st.text_input('Enter a name', 'Miles')

yourname = baby_names[baby_names['name'] == babyname.lower()]
yourname = yourname.groupby(['year', 'name']).sum('count').reset_index()# .drop(columns='gender')
HOURS_IN_YEAR = 24 * 365
yourname['name_per_hour'] = yourname['count'] / HOURS_IN_YEAR
alt_chart = alt.Chart(yourname).mark_line().encode(
    x=alt.X('year:Q', axis=alt.Axis(format='d')),
    y='name_per_hour',
).properties(
    title=f'{babyname} per hour',
)
st.altair_chart(alt_chart, use_container_width=True)