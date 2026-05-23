import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# PAGE CONFIG
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
.main {
    background-color: #141414;
    color: white;
}

.stApp {
    background-color: #141414;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #000000;
}

.metric-card {
    background-color: #1f1f1f;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# LOAD DATA
df = pd.read_csv("netflix_titles.csv")

# CLEANING
df.fillna("Unknown", inplace=True)

# SIDEBAR
st.sidebar.title("🎯 Netflix Filters")

search = st.sidebar.text_input("Search Title")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].unique(),
    default=df["country"].unique()[:10]
)

rating_filter = st.sidebar.multiselect(
    "Select Rating",
    options=df["rating"].unique(),
    default=df["rating"].unique()
)

# FILTER DATA
filtered_df = df[
    (df["type"].isin(type_filter)) &
    (df["country"].isin(country_filter)) &
    (df["rating"].isin(rating_filter))
]

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False)
    ]

# TITLE
st.title("🎬 Netflix Analytics Dashboard V4")

st.markdown("---")

# KPI SECTION
movies = filtered_df[filtered_df["type"] == "Movie"].shape[0]
tvshows = filtered_df[filtered_df["type"] == "TV Show"].shape[0]
countries = filtered_df["country"].nunique()
directors = filtered_df["director"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎥 Movies", movies)
col2.metric("📺 TV Shows", tvshows)
col3.metric("🌍 Countries", countries)
col4.metric("🎬 Directors", directors)

st.markdown("---")

# DATASET PREVIEW
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df.head())

# CHARTS
col1, col2 = st.columns(2)

# PIE CHART
with col1:
    type_counts = filtered_df["type"].value_counts()

    fig1 = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        title="Movies vs TV Shows",
        color_discrete_sequence=px.colors.sequential.Reds
    )

    st.plotly_chart(fig1, width='stretch')

# BAR CHART
with col2:
    rating_counts = filtered_df["rating"].value_counts().reset_index()
    rating_counts.columns = ["Rating", "Count"]

    fig2 = px.bar(
        rating_counts,
        x="Rating",
        y="Count",
        color="Count",
        title="Ratings Distribution",
        color_continuous_scale="reds"
    )

    st.plotly_chart(fig2, width='stretch')

# TOP COUNTRIES
st.subheader("🌍 Top Countries")

top_countries = (
    filtered_df["country"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_countries.columns = ["Country", "Count"]

fig3 = px.bar(
    top_countries,
    x="Country",
    y="Count",
    color="Count",
    color_continuous_scale="reds"
)

st.plotly_chart(fig3, width='stretch')

# =========================
# RECOMMENDATION SYSTEM
# =========================

st.markdown("---")
st.header("🎯 Netflix Recommendation System")

# CREATE TAGS
df["tags"] = (
    df["listed_in"].astype(str) + " " +
    df["description"].astype(str)
)

# TF-IDF VECTORIZE
tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(df["tags"])

# COSINE SIMILARITY
cosine_sim = cosine_similarity(tfidf_matrix)

# TITLE LIST
titles = df["title"].drop_duplicates().tolist()

selected_movie = st.selectbox(
    "Choose a Movie or TV Show",
    titles
)

# RECOMMEND FUNCTION
def recommend(title):

    try:
        idx = df[df["title"] == title].index[0]

        sim_scores = list(enumerate(cosine_sim[idx]))

        sim_scores = sorted(
            sim_scores,
            key=lambda x: x[1],
            reverse=True
        )

        sim_scores = sim_scores[1:6]

        movie_indices = [i[0] for i in sim_scores]

        return df["title"].iloc[movie_indices]

    except:
        return []

# SHOW RECOMMENDATIONS
if st.button("Recommend"):

    recommendations = recommend(selected_movie)

    st.subheader("🎬 Recommended Titles")

    for movie in recommendations:
        st.write("✅", movie)