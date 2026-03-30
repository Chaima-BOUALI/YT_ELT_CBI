#THIS CODE DOESNT USE A FUNCTION IT WILL BE CREATED BASED ON THIS CODE IN video_stats.py
# Importing requests liberary 
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
#Adding URL to make requests 
#Setting URL VARiables
API_Key= os.getenv("API_Key")
CHANNEL_Handle="MrBeast"
part="contentDetails"

url=f"https://youtube.googleapis.com/youtube/v3/channels?part={part}&forHandle={CHANNEL_Handle}&key={API_Key}"
response = requests.get(url)
print(response)

#Parsing response using JSON
data = response.json()
#json.dumps() converts a Python object into a JSON formatted string
print(json.dumps(data,indent=4))

#Changing the path and parsing data 
#data.items[0].contentDetails.relatedPlaylists.uploads
channel_Items=data["items"][0]
channel_Kind=channel_Items["kind"]
channel_ID=channel_Items["id"]
channel_playListID=channel_Items["contentDetails"]["relatedPlaylists"]["uploads"]
channel_playList_Likes=channel_Items["contentDetails"]["relatedPlaylists"]["likes"]

print("channel items are :", channel_Items)
print("channel kinf is :",channel_Kind)
print("channel id is : ",channel_ID)
print("PlayList id is : ", channel_playListID)
print("PlayList likes are : ", channel_playList_Likes)