from googleapiclient.discovery import build
import config

api_key = config.YOUTUBE_API_KEY

youtube = build('youtube', 'v3', developerKey=api_key)

# Example: Search for videos related to a certain query
search_query = "EAZ - Juicy"  # Replace with your search query, should be in a parsable format
songName = search_query.split('-')[-1].strip().lower()
resultLimit = 5
popSum = 0


### got this stuff from chatGPT
# Example: Search for videos related to a certain query
search_response = youtube.search().list(q=search_query, part='id', type='video', order='viewCount', maxResults=resultLimit).execute()

# Extract video IDs from the search results
video_ids = [item['id']['videoId'] for item in search_response['items']]

# Retrieve statistics for each video
for video_id in video_ids:
    video_response = youtube.videos().list(part='snippet,statistics', id=video_id).execute()
    
    # Process the response
    snippet = video_response['items'][0]['snippet']
    statistics = video_response['items'][0]['statistics']

    title = snippet['title']
    ### print(f"Description: {snippet['description']}")

    if songName in title.lower():
        print(f"Title: {title}")
        print(f"View Count: {statistics['viewCount']}")
        popSum += int(statistics['viewCount'])

print("TOTAL")
print(popSum)
