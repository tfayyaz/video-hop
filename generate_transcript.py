import json
import os
from datetime import timedelta
from youtube_transcript_api import YouTubeTranscriptApi

def convert_to_hms(seconds):
    td = timedelta(seconds=float(seconds))
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

# Load the videos
with open('static/data/videos.json', 'r') as f:
    videos = json.load(f)

# Loop through each video
for video in videos:
    video_id = video["video_id"]
    video_name = video["video_name"]

    # Prepare the path to the transcript file
    transcript_file_path = f'./static/data/transcripts/{video_id}.json'
    
    # Skip if the transcript file already exists
    if os.path.isfile(transcript_file_path):
        print(f"Transcript for {video_name} already exists. Skipping...")
        continue

    # Transcript retrieval
    video_transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Add the 'time' key to each transcript entry
    for t in video_transcript:
        t['time'] = convert_to_hms(t['start'])

    # Prepare video data
    video_data = {
        "video_id": video_id,
        "video_name": video_name,
        "video_thumb_url": video["video_thumb_url"],
        "video_date": video["video_date"],
        "video_short_description": video["video_short_description"],
        "video_transcript": video_transcript
    }

    # Write the modified data back to the JSON file
    with open(transcript_file_path, 'w') as file:
        print(f"Writing transcript for {video_name} to JSON file")
        json.dump(video_data, file, indent=4)
