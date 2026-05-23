import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("netflix_titles.csv")

# ---------------- CLEAN DATA ----------------
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Unknown")
df['director'] = df['director'].fillna("Unknown")

# ---------------- TITLE ----------------
st.title("🎬 Netflix Analytics Dashboard V2")

st.markdown("Interactive Data Analytics Dashboard using Streamlit")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filter Options")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].unique(),
    default=df['country'].unique()[:10]
)

# ---------------- FILTER DATA ----------------
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['country'].isin(country_filter))
]

# ---------------- KPI CARDS ----------------
movies_count = filtered_df[filtered_df['type'] == 'Movie'].shape[0]
tv_count = filtered_df[filtered_df['type'] == 'TV Show'].shape[0]
country_count = filtered_df['country'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("🎬 Movies", movies_count)
col2.metric("📺 TV Shows", tv_count)
col3.metric("🌍 Countries", country_count)

st.divider()

# ---------------- DATA PREVIEW ----------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

# ---------------- PIE CHART ----------------
st.subheader("Movies vs TV Shows")

type_counts = filtered_df['type'].value_counts()

fig1 = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title="Content Distribution"
)

st.plotly_chart(fig1, width='stretch')

# ---------------- RATINGS CHART ----------------
st.subheader("Ratings Distribution")

rating_counts = filtered_df['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']

fig2 = px.bar(
    rating_counts,
    x='Rating',
    y='Count',
    color='Count',
    title='Ratings Distribution'
)

st.plotly_chart(fig2, width='stretch')

# ---------------- TOP COUNTRIES ----------------
st.subheader("Top Countries")

country_counts = (
    filtered_df['country']
    .value_counts()
    .head(10)
    .reset_index()
)

country_counts.columns = ['Country', 'Count']

fig3 = px.bar(
    country_counts,
    x='Country',
    y='Count',
    color='Count',
    title='Top 10 Countries'
)

st.plotly_chart(fig3, width='stretch')

# ---------------- RELEASE YEAR TREND ----------------
st.subheader("Content Release Trend")

year_counts = (
    filtered_df['release_year']
    .value_counts()
    .sort_index()
    .reset_index()
)

year_counts.columns = ['Year', 'Count']

fig4 = px.line(
    year_counts,
    x='Year',
    y='Count',
    title='Content Released Over Years'
)

st.plotly_chart(fig4, width='stretch')