📌 Project Statement:
As an app developer, you are tasked with building an interactive, end-to-end ETL and data exploration platform using the Harvard Art Museums public API. This platform will empower users to dynamically explore, collect, store, and query rich art collections from Harvard’s digital archive — all through a simple, intuitive Streamlit web application.

🎯 Business Use Cases:
Museum Collection Strategy:
 Enable curators and acquisition teams to analyze classification trends (e.g., sculptures, manuscripts) to guide future acquisitions or exhibitions.


Educational Portals:
 Provide universities or online platforms with an interactive tool for students to explore historical artifacts by classification, era, or culture.


Audience Interest Tracking:
 Use SQL analytics to track which types of artifacts receive the most user queries or views, informing digital marketing and content strategies.


Cultural Research & Journalism:
 Support writers, historians, or researchers in filtering and retrieving targeted artifact data for storytelling or analysis.


Grant Reporting & Documentation:
 Help museum management export visual and data-driven summaries of digital engagement and collection diversity for funding reports.


Project Approach:
📝1: Getting the Harvard Art Museums API Key
Go to: https://www.harvardartmuseums.org/collections/api
Scroll down and click on “Send a request”.
In the google form, fill in your name, email address, and a brief description of your project or intended use.
Submit the form — your API key will be displayed instantly and also sent to your email.
The key will look like: “1a7ae53e-......”
Use your key to format the following API URLs using params: 
Classification: “https://api.harvardartmuseums.org/classification”
Details of every classification:
“https://api.harvardartmuseums.org/object”

📂 Available Classifications & Data Collection Targets
The Harvard Art Museums API offers a rich collection of artifacts categorized under 116 unique classifications — ranging from Paintings, Sculptures, and Coins to Jewelry, Furniture, Drawings, and many more. These classifications represent different types of artworks and historical objects preserved in the museum's digital archive.
To-Dos:
Collect a minimum of 2500 records for each chosen classification(via streamlit) using the API.


Store these records in 3 separate SQL tables for further querying and analysis.


This ensures broad, diverse data coverage and provides a rich base for meaningful data exploration 

. SQL Table creation:
🗄️ Table 1: artifact_metadata
This table stores general metadata about each artifact.
Field
Description
Data Type
id
Unique ID for the artifact(PRIMARY KEY)
INTEGER
title
Title or name of the artifact
TEXT
culture
Cultural origin of the artifact
TEXT
period
Specific historical period
TEXT
century
Century the object belongs to
TEXT
medium
Material/technique used (e.g., ink, silk,silver)
TEXT
dimensions
Physical dimensions (height, width, etc.)
TEXT
description
Description of the object
TEXT
department
Department at the museum responsible for the object
TEXT
classification
Classification/category (e.g., Painting, Sculpture)
TEXT
accessionyear
Year the object was acquired
INTEGER
accessionmethod
How the object was acquired (purchase, gift, etc.)
TEXT


🖼️ Table 2: artifact_media
This table handles visual and interactive media + additional metadata.
Field
Description
Data Type
objectid
Foreign key linking to artifact_metadata
INT
imagecount
Number of associated images
INT
mediacount
Number of media files (images, videos)
INTEGER
colorcount
Count of detected colors
INTEGER
rank
Importance or order value for display
INTEGER
datebegin
Starting year of creation
INTEGER
dateend
Ending year of creation
INTEGER


🎨 Table 3: artifact_colors:
Color details extracted from the JSON structure.
Column
Description
Data Type
objectid
Foreign key that links this color record to its corresponding artifact.
INTEGER
color
Hexadecimal color code (e.g., #afafaf) detected in the artifact's image.
TEXT
spectrum
A representative color on the visible spectrum (also a hex code, e.g., #8c5fa8).
TEXT
hue
General name of the color tone (e.g., Grey, Red, Blue).
TEXT
percent
Percentage of the artifact's image area occupied by this color (0.0–100.0).
REAL
css3
Closest matching CSS3 standard color code (e.g., #a9a9a9).
TEXT


🔍 3 : SQL Queries (Display the output in streamlit)
🏺 artifact_metadata Table:
List all artifacts from the 11th century belonging to Byzantine culture.


What are the unique cultures represented in the artifacts?


List all artifacts from the Archaic Period.


List artifact titles ordered by accession year in descending order.


How many artifacts are there per department?





🖼️ artifact_media Table:
Which artifacts have more than 1 image?


What is the average rank of all artifacts?


Which artifacts have a higher colorcount than mediacount?


List all artifacts created between 1500 and 1600.


How many artifacts have no media files?



🎨 artifact_colors Table:
What are all the distinct hues used in the dataset?


What are the top 5 most used colors by frequency?


What is the average coverage percentage for each hue?


List all colors used for a given artifact ID.


What is the total number of color entries in the dataset?



🔗 Join-Based Queries:
List artifact titles and hues for all artifacts belonging to the Byzantine culture.


List each artifact title with its associated hues.


Get artifact titles, cultures, and media ranks where the period is not null.


Find artifact titles ranked in the top 10 that include the color hue "Grey".


How many artifacts exist per classification, and what is the average media count for each?

Along with answering the 20 given questions, learners are encouraged to frame and execute their own SQL queries(5 to 10) to derive additional insights.

📌 📊 Streamlit Application Breakdown
🖥️  App Interface Layout
Title + Instructions


Dropdown to select a classification(Ex: Coins, paintings, scriptures, jewellery,Drawings etc..)


Collect a minimum of 2500 records for every classification.


Buttons


Collect Data → fetch from API


Show Data → display fetched records


Insert into SQL → store data into SQL table


Query & Visualization Section


Pre-written query options in a selectbox


Button to Run Query


Display results in a table(mandatory) or chart(optional)

