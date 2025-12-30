%%writefile app.py
import sqlite3
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
conn = sqlite3.connect("Hardvard.db", check_same_thread=False)
cursor = conn.cursor()

# --------------------------------------------------
# API CONFIG
# --------------------------------------------------
API_KEY = "145c1dd9-a73b-41f9-9165-e0227f4ddfd6"
OBJECT_URL = "https://api.harvardartmuseums.org/object"

CLASSIFICATIONS = ("Paintings", "Drawings", "Sculpture", "Jewelry")

# --------------------------------------------------
# CREATE TABLES
# --------------------------------------------------
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_metadata(
        id INTEGER PRIMARY KEY,
        title TEXT,
        culture TEXT,
        period TEXT,
        century TEXT,
        medium TEXT,
        dimensions TEXT,
        description TEXT,
        department TEXT,
        classification TEXT,
        accessionyear INTEGER,
        accessionmethod TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_media(
        objectid INTEGER,
        imagecount INTEGER,
        mediacount INTEGER,
        colorcount INTEGER,
        rank INTEGER,
        datebegin INTEGER,
        dateend INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artifact_colors(
        objectid INTEGER,
        color TEXT,
        spectrum TEXT,
        hue TEXT,
        percent REAL,
        css3 TEXT
    )
    """)
    conn.commit()

create_tables()

# --------------------------------------------------
# FETCH DATA FROM API
# --------------------------------------------------
def fetch_artifacts(classification, limit=2500):
    meta, media, colors = [], [], []
    page = 1

    while len(meta) < limit:
        params = {
            "apikey": API_KEY,
            "classification": classification,
            "size": 100,
            "page": page
        }

        response = requests.get(OBJECT_URL, params=params).json()
        records = response.get("records", [])

        if not records:
            break

        for item in records:
            objectid = item.get("objectid")

            meta.append({
                "id": objectid,
                "title": item.get("title"),
                "culture": item.get("culture"),
                "period": item.get("period"),
                "century": item.get("century"),
                "medium": item.get("medium"),
                "dimensions": item.get("dimensions"),
                "description": item.get("description"),
                "department": item.get("department"),
                "classification": item.get("classification"),
                "accessionyear": item.get("accessionyear"),
                "accessionmethod": item.get("accessionmethod")
            })

            media.append({
                "objectid": objectid,
                "imagecount": item.get("imagecount"),
                "mediacount": item.get("mediacount"),
                "colorcount": item.get("colorcount"),
                "rank": item.get("rank"),
                "datebegin": item.get("datebegin"),
                "dateend": item.get("dateend")
            })

            for c in item.get("colors", []):
                colors.append({
                    "objectid": objectid,
                    "color": c.get("color"),
                    "spectrum": c.get("spectrum"),
                    "hue": c.get("hue"),
                    "percent": c.get("percent"),
                    "css3": c.get("css3")
                })

        page += 1

    return pd.DataFrame(meta), pd.DataFrame(media), pd.DataFrame(colors)

# --------------------------------------------------
# STREAMLIT PAGE SETUP
# --------------------------------------------------
st.set_page_config(page_title="Harvard Artifacts ETL", layout="wide")

st.title("🏛️ Harvard’s Artifacts Collection")
st.caption("Explore the data of Harvard's Museum")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "meta" not in st.session_state:
    st.session_state.meta = None
    st.session_state.media = None
    st.session_state.colors = None

if "step" not in st.session_state:
    st.session_state.step = "select"

# --------------------------------------------------
# STEP 1: SELECT CLASSIFICATION + COLLECT DATA
# --------------------------------------------------
classification = st.selectbox("Enter a classification:", CLASSIFICATIONS)

if st.button("📥 Collect Data"):
    with st.spinner("Collecting data from Harvard Art Museums API..."):
        meta, media, colors = fetch_artifacts(classification)
        st.session_state.meta = meta
        st.session_state.media = media
        st.session_state.colors = colors
    st.success(f"Collected {len(meta)} records")

# --------------------------------------------------
# SINGLE LINE NAVIGATION (BUTTON BAR)
# --------------------------------------------------
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Select Your Data", use_container_width=True):
        st.session_state.step = "select"

with col2:
    if st.button("🗄️ Migrate to SQL", use_container_width=True):
        st.session_state.step = "migrate"

with col3:
    if st.button("🔍 SQL Queries", use_container_width=True):
        st.session_state.step = "query"

st.divider()

# --------------------------------------------------
# SECTION 1: SELECT YOUR DATA
# --------------------------------------------------
if st.session_state.step == "select":

    st.subheader("📊 Preview Collected Data")

    option = st.selectbox("Select your choice", ["Metadata", "Media", "Colors"])

    if st.session_state.meta is not None:
        if option == "Metadata":
            st.dataframe(st.session_state.meta.head(50))
        elif option == "Media":
            st.dataframe(st.session_state.media.head(50))
        else:
            st.dataframe(st.session_state.colors.head(50))
    else:
        st.warning("Please collect data first")

# --------------------------------------------------
# SECTION 2: MIGRATE TO SQL
# --------------------------------------------------
elif st.session_state.step == "migrate":

    st.subheader("🗄️ Insert the Collected Data")

    if st.button("💾 Insert into SQL"):

        if st.session_state.meta is not None:

            cursor.execute(
                "SELECT COUNT(*) FROM artifact_metadata WHERE classification = ?",
                (classification,)
            )
            exists = cursor.fetchone()[0]

            if exists > 0:
                st.error("❌ This classification already exists in SQL")
            else:
                st.session_state.meta.to_sql("artifact_metadata", conn, if_exists="append", index=False)
                st.session_state.media.to_sql("artifact_media", conn, if_exists="append", index=False)
                st.session_state.colors.to_sql("artifact_colors", conn, if_exists="append", index=False)
                conn.commit()
                st.success("✅ Data inserted successfully")

        else:
            st.warning("Collect data before inserting")

# --------------------------------------------------
# SECTION 3: SQL QUERIES
# --------------------------------------------------
elif st.session_state.step == "query":

    st.subheader("🔍 SQL Queries")

    QUERY_OPTIONS = {
        "Artifacts by Department":
            "SELECT department, COUNT(*) AS count FROM artifact_metadata GROUP BY department",

        "Artifacts with Multiple Images":
            """SELECT m.title, me.imagecount
               FROM artifact_metadata m
               JOIN artifact_media me ON m.id = me.objectid
               WHERE me.imagecount > 1
               LIMIT 50""",

        "Top 10 Grey Artifacts":
            """SELECT DISTINCT m.title
               FROM artifact_metadata m
               JOIN artifact_colors c ON m.id = c.objectid
               WHERE c.hue = 'Grey'
               LIMIT 10""",

        "Byzantine Artifacts with Hues":
           """SELECT m.title, c.hue
              FROM artifact_metadata m
              JOIN artifact_colors c
                ON m.id = c.objectid
              WHERE m.culture = 'Byzantine'""",

       "All Artifact Titles with Hues":
          """SELECT m.title, c.hue
             FROM artifact_metadata m
             JOIN artifact_colors c
                ON m.id = c.objectid""",

       "Artifacts with Period and Media Rank":
          """SELECT m.title,
              m.culture,
              me.imagecount AS media_rank
             FROM artifact_metadata m
             JOIN artifact_media me
               ON m.id = me.objectid
             WHERE m.period IS NOT NULL""",

       "Top 10 Grey Artifacts (Ranked)":
          """SELECT DISTINCT m.title, me.imagecount
             FROM artifact_metadata m
             JOIN artifact_media me
               ON m.id = me.objectid
             JOIN artifact_colors c
               ON m.id = c.objectid
             WHERE c.hue LIKE '%Grey%'
             ORDER BY me.imagecount DESC
             LIMIT 10"""
      }
    

    query_choice = st.selectbox("Select SQL Query", list(QUERY_OPTIONS.keys()))

    if st.button("▶️ Run Query"):
        df = pd.read_sql(QUERY_OPTIONS[query_choice], conn)
        st.dataframe(df)

        
