import json
import pymongo
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langdetect import detect, LangDetectException

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize the YouTube API
api_key = ['AIzaSyDIHWn7fCzFSU9xlSjpVJi6Gf6dj5J-qX4']
youtube = build('youtube', 'v3', developerKey=api_key)

# MongoDB connection setup
client = pymongo.MongoClient(config['MONGO_URI'])
db = client[config['DB_NAME']]
collection = db[config['COLLECTION']]

# Load stop words from files
def load_stop_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(word.strip() for word in file.readlines())

english_stop_words = load_stop_words('stopwordsang.txt')
french_stop_words = load_stop_words('stopwordsfr.txt')
arabic_stop_words = load_stop_words('stopwordsarab.txt')
darija_stop_words = load_stop_words('stopwords.txt')

# Function to get popular videos from a channel
def get_popular_videos(channel_id):
    response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='viewCount',
        maxResults=11
    ).execute()
    
    return [item['id']['videoId'] for item in response['items']]

# Function to get comments for a specific video
def get_comments(video_id):
    comments = []
    total_comments = 0
    page_token = None
    
    try:
        while total_comments < 250:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(100, 250 - total_comments),
                pageToken=page_token
            ).execute()
            
            for item in response.get('items', []):
                try:
                    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                    
                    if is_arabic(comment):
                        comments.append({
                            "video_id": video_id,
                            "comment": comment,
                            "author": author_name,
                            "language": "arabic"
                        })
                        total_comments += 1
                    elif is_darija(comment):
                        comments.append({
                            "video_id": video_id,
                            "comment": comment,
                            "author": author_name,
                            "language": "darija"
                        })
                        total_comments += 1
                    elif is_french(comment):
                        comments.append({
                            "video_id": video_id,
                            "comment": comment,
                            "author": author_name,
                            "language": "french"
                        })
                        total_comments += 1
                    elif is_english(comment):
                        comments.append({
                            "video_id": video_id,
                            "comment": comment,
                            "author": author_name,
                            "language": "english"
                        })
                        total_comments += 1
                    else:
                        pass
                
                except KeyError:
                    print(f"Skipping malformed comment for video ID {video_id}")
            
            if 'nextPageToken' in response:
                page_token = response['nextPageToken']
            else:
                break
        
        return comments[:250]
    
    except HttpError as e:
        print(f"HttpError occurred: {e}")
        return []

# Function to remove stop words
def remove_stop_words(text, stop_words):
    words = text.split()
    return ' '.join([word for word in words if word.lower() not in stop_words])

# Function to check if a comment is in Arabic
def is_arabic(comment):
    try:
        filtered_comment = remove_stop_words(comment, arabic_stop_words)
        lang = detect(filtered_comment)
        return lang == 'ar'
    except LangDetectException:
        return False

# Function to check if a comment is in Darija
def is_darija(comment):
    try:
        filtered_comment = remove_stop_words(comment, darija_stop_words)
        lang = detect(filtered_comment)
        return lang == 'ar'  # Assuming Darija is detected as 'ar'
    except LangDetectException:
        return False

# Function to check if a comment is in French
def is_french(comment):
    try:
        filtered_comment = remove_stop_words(comment, french_stop_words)
        lang = detect(filtered_comment)
        return lang == 'fr'
    except LangDetectException:
        return False

# Function to check if a comment is in English
def is_english(comment):
    try:
        filtered_comment = remove_stop_words(comment, english_stop_words)
        lang = detect(filtered_comment)
        return lang == 'en'
    except LangDetectException:
        return False

# Function to store comments in MongoDB
def store_comments(comments, video_id):
    for comment in comments:
        collection.insert_one({
            "video_id": video_id,
            "comment": comment["comment"],
            "author": comment["author"],
            "language": comment["language"]
        })

# Main function to fetch comments for popular videos and store in MongoDB
def main():
    video_ids = get_popular_videos(config['CHANNEL_ID'])
    all_comments = []
    
    for video_id in video_ids:
        print(f"Fetching comments for video ID: {video_id}")
        comments = get_comments(video_id)
        all_comments.extend(comments)
        store_comments(comments, video_id)
    
    # Save all comments to extracted_comments.json
    filename = "extracted_comments.json"
    with open(filename, 'w+', encoding='utf-8') as json_file:
        json.dump(all_comments, json_file, ensure_ascii=False, indent=2)
    
    print(f"All comments have been saved to {filename}")

if __name__ == "__main__":
    main()
