import json
from datetime import timedelta

def convert_to_hms(seconds):
    td = timedelta(seconds=float(seconds))
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

# Read the JSON file
with open('./static/data/transcripts/1.json', 'r') as file:
    video = json.load(file)

# Add the 'time' key to each transcript entry
for transcript in video['video_transcript']:
    transcript['time'] = convert_to_hms(transcript['start'])

# Write the modified data back to the JSON file
with open('./static/data/transcripts/1.json', 'w') as file:
    print("modified data back to the JSON file")
    json.dump(video, file, indent=4)
