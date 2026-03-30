#Importing requests liberary 
import requests
import json
#Adding URL to make requests 
#Setting URL VARiables
API_Key="AIzaSyC7iq85pKbLp3_jjvb68JJkuCZPbxNtTo4"
CHANNEL_Handle="MrBeast"
part="contentDetails"

#Defining a coherent function to structure code and reuse in the future
def get_playlist_information(): 
    
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

    except requests.Exception.RequestException as ERR:
        raise ERR


#Script is run directly and not imported as a module 
#If we will run this script from another script => Not run directly so name will not be equals main but equals the name of the file.py
if __name__=="__main__": 
    print ("The function get playlist information will be excecuted")
    get_playlist_information()
else:
    print ("The function get playlist information will not be excecuted")