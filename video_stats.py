#Importing requests liberary 
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
#Adding URL to make requests 
#Setting URL VARiables
#os command gets the env variables 
API_Key= os.getenv("API_Key")
CHANNEL_Handle="MrBeast"
part="contentDetails"
part_two = "snippet"
part_three ="statistics"
playListID ='UUX6OQ3DkcsbYNE6H8uQQuVA'
maxResults = 50

#Defining a coherent function to structure code and reuse in the future
def get_playlist_id(): 
    
    try: 

        url=f"https://youtube.googleapis.com/youtube/v3/channels?part={part}&forHandle={CHANNEL_Handle}&key={API_Key}"
        response = requests.get(url)
        #print(response)
        response.raise_for_status
        #Parsing response using JSON
        data = response.json()
        #json.dumps() converts a Python object into a JSON formatted string
        #print(json.dumps(data,indent=4))

        #Changing the path and parsing data 
        #data.items[0].contentDetails.relatedPlaylists.uploads
        channel_Items=data["items"][0]
        channel_Kind=channel_Items["kind"]
        channel_ID=channel_Items["id"]
        channel_playListID=channel_Items["contentDetails"]["relatedPlaylists"]["uploads"]
        channel_playList_Likes=channel_Items["contentDetails"]["relatedPlaylists"]["likes"]

        print("channel items are :", channel_Items)
        print("channel kind is :",channel_Kind)
        print("channel id is : ",channel_ID)
        print("PlayList id is : ", channel_playListID)
        print("PlayList likes are : ", channel_playList_Likes)
        return channel_Items,channel_Kind,channel_ID,channel_playListID,channel_playList_Likes

    except requests.exceptions.RequestException as ERR:
        raise ERR


def get_video_id(playList_id):
    video_ids=[]
    pageToken=None
    url_base=f"https://youtube.googleapis.com/youtube/v3/playlistItems?part={part}&maxResults={maxResults}&playlistId={playListID}&key={API_Key}"
    try:
        while True:
            url=url_base

            #If pageToke!=None then append the URL with the token got in the response which is the next page token because each page returns a maximum of 50 results           
            if pageToken: 
                url += f"&pageToken={pageToken}" 
            response = requests.get(url)
            #print(response)
            response.raise_for_status
            #Parsing response using JSON
            data = response.json()
            #json.dumps() converts a Python object into a JSON formatted string
            #print(json.dumps(data,indent=4))
            #We will Loop through items and get every video id from the lists and stock it in the ideo_ids[] List that is initially empty
            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                #print("this is the video id: ", video_id)
                video_ids.append(video_id)

            pageToken=data.get("nextPageToken")
            if not pageToken: 
                break        
        print("the list of video ids in this playList is :" , video_ids)
        return(video_ids)        
    except requests.exceptions.RequestException as ERR:
        raise ERR



def extract_video_data(video_ids): 
    extracted_data=[]


    ##Now we need a function that will use the video_ids to return video details 
    #First we need to split video_ids list to wideo ideas 

    def batch_list(video_id_list, batch_size): 
        for video_id in range(0,len(video_id_list),batch_size):
            #Yield is a function that returns a value pauses the func remembers its state and then resumes where it left off
            yield video_id_list[video_id : video_id + batch_size]


    try: 
        #Look through the batch values 
        for batch in batch_list(video_ids,maxResults): 
            video_ids_str=",".join(batch)
            url =f'https://youtube.googleapis.com/youtube/v3/videos?part={part}&part={part_two}&part={part_three}&id={video_ids_str}&key={API_Key}'
            response = requests.get(url)
            #print(response)
            response.raise_for_status
            #Parsing response using JSON
            data = response.json()
            #json.dumps() converts a Python object into a JSON formatted string
            #print(json.dumps(data,indent=4))
            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails'] 
                statistics=item['statistics']
            #Defining a dictionnary that will contain all the variables we're looking for 
                video_data = {
                    "video_id" : video_id,
                    "title" : snippet['title'], 
                    "publishedAT" : snippet['publishedAt'],
                    "duration" : contentDetails['duration'], 
                    "viewCount" : statistics.get('viewCount', None), 
                    "likeCount" : statistics.get('likeCount', None), 
                    "commentCount" : statistics.get('commentCount', None)
                }
                    
                    
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as ERR:
            raise ERR

#Script is run directly and not imported as a module 
#If we will run this script from another script => Not run directly so name will not be equals main but equals the name of the file.py
if __name__=="__main__": 
    print ("The function get playlist id will be excecuted")
    playList_id=get_playlist_id()
    #print(playList_id)
    video_ids=get_video_id(playList_id)
    print(extract_video_data(video_ids))
else:
    print ("The function get playlist id will not be excecuted")