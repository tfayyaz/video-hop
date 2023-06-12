from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
import json

app = Flask(__name__)

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

@app.route('/')
def home():
    with open('./static/data/videos.json', 'r') as file:
        videos = json.load(file)
    return render_template('home.html', videos=videos)

# @app.route("/")
# def homepage():
#     return render_template("index.html")

@app.route('/video')
def video():
    video_id = request.args.get('vid', '')
    # Load the corresponding video transcript file
    with open(f'./static/data/transcripts/{video_id}.json', 'r') as file:
        video = json.load(file)
    return render_template('video.html', video=video)

def search_prev_next(data, search_term):
    search_results = []
    for i, entry in enumerate(data):
        if search_term.lower() in entry['text'].lower():

            modified_entry = {}
            modified_entry["start"] = entry["start"]
            modified_entry["time"] = entry["time"]
            modified_entry["text_list"] = []
            modified_entry["text_list"].append(entry["text"])

            # Add previous entry if it exists
            if i > 0:
                previous_text = data[i-1]['text']
                previous_start = data[i-1]['start']
                previous_time = data[i-1]['time']
                modified_entry["start"] = previous_start
                modified_entry["time"] = previous_time
                modified_entry["text_list"].insert(0, previous_text)

            # Add next entry if it exists
            if i < len(data) - 1:
                next_text = data[i+1]['text']
                modified_entry["text_list"].append(next_text)

            modified_entry["text"] = " ".join(modified_entry["text_list"])

            # Add the modified entry
            search_results.append(modified_entry)
    return search_results
    

@app.route('/search', methods=['POST'])
def search():
    video_id = request.args.get('vid', '')
    search_term = request.form.get('search')
    print(search_term)
 
    with open(f'./static/data/transcripts/{video_id}.json', 'r') as file:
        video = json.load(file)
        data = video['video_transcript']

    # search the data
    search_results = [entry for entry in data if search_term.lower() in entry['text'].lower()]
    
    # prepare the initial and empty HTML string
    html_string = """<tr class="hover:bg-slate-50">
          <td class="border text-slate-500 text-sm px-2 py-2 hover:bg-slate-50">Search above or hop to the start of the video...</td>
          <td class="border px-2 py-2 min-w-128 hover:bg-slate-50">
            <button 
            class="whitespace-nowrap min-w-128 bg-teal-500 hover:bg-teal-700 text-xs text-white py-2 px-2 rounded"
            hx-get="/video-hop?vid={{ video.video_id }}&start=0" hx-target="#video-player" hx-swap="outerHTML">Hop to 00:00:00
            </button>
          </td>
          </tr>"""
    
    # prepare the search result HTML string
    if(search_term != ''):
        html_string = ""
        for result in search_results:

            # convert transcript start time into human readable time
            readable_time = result['time']

            # trim start time to remove decimal places
            start_time_float = float(result['start']) 
            seconds_trimmed = int(start_time_float) 

            # highlight search_term in result text
            highlighted_text = result['text'].lower().replace(search_term, f'<span class="bg-teal-500 text-white">{search_term}</span>')

            html_string += f"""<tr>
            <tr class="hover:bg-slate-50">
            <td class="border text-slate-500 text-sm px-2 py-2">{result['text']}</td>
            <td class="border px-2 py-2">
              <button 
              class="whitespace-nowrap overflow-hidden bg-teal-500 hover:bg-teal-700 text-xs text-white py-2 px-2 rounded"
              hx-get="/video-hop?vid={video_id}&start={seconds_trimmed}" hx-target="#video-player" hx-swap="outerHTML">Hop to {readable_time}
              </button>
            </td>
            </tr>
            """

    return html_string

@app.route('/video-hop', methods=['GET'])
def video_hop():
    video_id = request.args.get('vid')
    start_time = request.args.get('start')
    start_time_float = float(start_time) 
    start_time_trimmed = int(start_time_float) 
    
    # html_string = f"""<iframe width="720" height="405" src="https://www.youtube.com/embed/1o_QDFq6gzE?start={start_time_trimmed}&autoplay=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>"""
    
    html_string = f'<iframe id="video-player" class="w-full aspect-video rounded-lg shadow-lg" src="https://www.youtube.com/embed/{video_id}?start={start_time_trimmed}&autoplay=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    return html_string



if __name__ == "__main__":
    app.run(debug=True)