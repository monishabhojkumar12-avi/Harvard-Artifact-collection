Overview

The Harvard Artifact Collection Project is an end-to-end data engineering and analysis project built using the Harvard Art Museums API. The project focuses on extracting large-scale artifact data, transforming it into a structured format, storing it in a relational database, and performing analytical queries to gain insights into artworks, cultures, media usage, and color patterns.

This project is designed as a beginner-friendly yet industry-relevant implementation of API data handling, SQL database design, and data analysis.

Objectives:

1.Extract artifact data from a public museum API

2.Design a normalized relational database schema

3.Store and manage large datasets using SQL

4.Perform analytical queries using SQL

5.Enable classification-based filtering and analysis

6.Prepare data for visualization and dashboarding

🧩 Data Source

API: Harvard Art Museums API

Endpoint: /object

Data Includes:

1.Artifact metadata

2.Media information

3.Color composition details

4.Media information

5.Color composition details

Database Schema

The project uses three relational tables:

1️⃣ artifact_metadata

Stores core descriptive information about each artifact.

1.object_id (Primary Key)

2.title

3.culture

4.period

5.century

6.classification

7.department

8.accession year

9.accession method

2️⃣ artifact_media

Stores media-related information.

1.object_id (Foreign Key)

2.image count

3.media count

4.color count

5.rank

6.date begin / date end

3️⃣ artifact_color

Stores color-level details for each artifact.

1.object_id (Foreign Key)

2.color

3.hue

4.spectrum

5.coverage percentage

6.css3 color name

🛠️ Technologies Used

1.Python – Data extraction and transformation

2.Pandas – Data manipulation

3.Requests – API calls

4.SQLAlchemy – Database connectivity

5.MySQL (TiDB Cloud) – Cloud database

6.SQL – Data analysis queries

7.Streamlit – Interactive dashboard (optional)

🔄 Data Pipeline Workflow

1.Fetch artifact data using API pagination

2.Filter artifacts by classification (Paintings, Drawings, Sculptures, Jewelry, etc.)

3.Normalize JSON data into relational tables

4.Load data into MySQL database

5.Run SQL queries for analysis

Visualize insights using Streamlit

📁 Project Structure
├── data_extraction.py
├── database_load.py
├── analysis_queries.sql
├── streamlit_app.py
├── requirements.txt
└── README.md
🚀 How to Run

Clone the repository

Install dependencies

pip install -r requirements.txt

Set up your MySQL / TiDB Cloud credentials

Run data extraction script

Load data into the database

Execute SQL queries or launch Streamlit app

📌 Key Learnings

1.API pagination handling

2.Relational database design

3.SQL joins and aggregations

4.Data cleaning and normalization

5.End-to-end data pipeline development

🙌 Acknowledgements

Harvard Art Museums for providing the public API

Open-source Python and SQL communities

📬 Contact

Created as part of a learning and portfolio project.

⭐ If you found this project useful, feel free to star the repository!

 
