import requests
import pandas as pd
from sqlalchemy import create_engine

classifications = ["Paintings", "Coins", "Drawings", "Sculptures", "Jewelry"]


api_key =  "145c1dd9-a73b-41f9-9165-e0227f4ddfd6"

for classifications in classifications:
    print(f"Processing classifications: {classifications}")
    params = {
        "apikey": api_key,
        "classifications": classifications,
        "size": 2500,
        "page": 1
    }

    all_records = []
    while len(all_records) < 2500:
        response = requests.get("https://api.harvardartmuseums.org/object", params=params)
        data = response.json()
        all_records.extend(data["records"])
        if "info" in data and data["info"]["next"]:
            params["page"] += 1
        else:
            break
------inserting into sql-------

artifact_metadata= []
artifact_media= []
artifact_color= []
for i in all_records:
     artifact_metadata.append(dict(
            object_id = i.get('id'),
            title = i.get('title'),
            culture = i.get('culture'),
            period = i.get('period'),
            century = i.get('century'),
            medium = i.get('medium'),
            dimension = i.get('dimension'),
            description = i.get('description'),
            department = i.get('department'),
            classification = i.get('classification'),
            accessionyear = i.get('accessionyear'),
            accessionmethod = i.get('accessionmethod')
        ))

     artifact_media.append(dict(
            object_id = i.get('id'),
            imagecount = i.get('imagecount'),
            mediacount = i.get('mediacount'),
            colorcount = i.get('colorcount'),
            ranks = i.get('rank'),
            datebegin = i.get('datebegin'),
            dateend = i.get('dateend')
        ))


     color_item = i.get('colors')
     if color_item:
      for j in color_item:
        artifact_color.append({
            "object_id": i.get("objectid"),
            "color": j.get("color"),
            "spectrum": j.get("spectrum"),
            "hue": j.get("hue"),
            "percent": j.get("percent"),
            "css3": j.get("css3")
        })   
        
------sql connection-------


engine = create_engine(
     "mysql+pymysql://278VnWPCuCkeWbZ.root:EOreOfSv1GliELtY@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Harvard_project",
      connect_args={
        "ssl": {
            "ca": "/content/tidb-ca.pem"
        }
    }
)


    df_metadata.to_sql("artifact_metadata", engine, if_exists="append", index=False)
    df_media.to_sql("artifact_media", engine, if_exists="append", index=False)
    df_color.to_sql("artifact_colors", engine, if_exists="append", index=False)

