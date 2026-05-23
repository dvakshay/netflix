import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #141414;
    color: white;
}

h1, h2, h3 {
    color: #E50914;
}

[data-testid="stSidebar"] {
    background-color: #000000;
}

[data-testid="metric-container"] {
    background-color: #1f1f1f;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("netflix_titles.csv")

# ---------------- CLEAN DATA ----------------
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Unknown")
df['director'] = df['director'].fillna("Unknown")
df['cast'] = df['cast'].fillna("Unknown")

# ---------------- TITLE ----------------
st.title("🎬 Netflix Analytics Dashboard V3")

st.markdown("### Interactive Netflix Data Analysis Dashboard")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🎯 Filter Options")

# Search box
search_title = st.sidebar.text_input("🔍 Search Title")

# Type filter
type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df['type'].unique(),
    default=df['type'].unique()
)

# Country filter
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

# Search filter
if search_title:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_title, case=False)
    ]

# ---------------- KPI CARDS ----------------
movies_count = filtered_df[filtered_df['type'] == 'Movie'].shape[0]
tv_count = filtered_df[filtered_df['type'] == 'TV Show'].shape[0]
country_count = filtered_df['country'].nunique()
director_count = filtered_df['director'].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎬 Movies", movies_count)
col2.metric("📺 TV Shows", tv_count)
col3.metric("🌍 Countries", country_count)
col4.metric("🎥 Directors", director_count)

st.divider()

# ---------------- DATA PREVIEW ----------------
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head())

# ---------------- MOVIES VS TV SHOWS ----------------
st.subheader("🎭 Movies vs TV Shows")

type_counts = filtered_df['type'].value_counts()

fig1 = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title="Content Distribution",
    color_discrete_sequence=['#E50914', '#B81D24']
)

st.plotly_chart(fig1, width='stretch')

# ---------------- RATINGS CHART ----------------
st.subheader("⭐ Ratings Distribution")

rating_counts = filtered_df['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']

fig2 = px.bar(
    rating_counts,
    x='Rating',
    y='Count',
    color='Count',
    title='Ratings Distribution',
    color_continuous_scale='Reds'
)

st.plotly_chart(fig2, width='stretch')

# ---------------- TOP COUNTRIES ----------------
st.subheader("🌍 Top Countries")

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
    title='Top 10 Countries',
    color_continuous_scale='Reds'
)

st.plotly_chart(fig3, width='stretch')

# ---------------- RELEASE YEAR TREND ----------------
st.subheader("📈 Content Release Trend")

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

# ---------------- TOP DIRECTORS ----------------
st.subheader("🎥 Top Directors")

director_counts = (
    filtered_df['director']
    .value_counts()
    .head(10)
    .reset_index()
)

director_counts.columns = ['Director', 'Count']

fig5 = px.bar(
    director_counts,
    x='Director',
    y='Count',
    color='Count',
    title='Top Directors',
    color_continuous_scale='Reds'
)

st.plotly_chart(fig5, width='stretch')