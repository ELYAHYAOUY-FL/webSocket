from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/start-stream', methods=['POST'])
def start_stream():
    data = request.get_json()
    video_path = data.get('videoPath')

    # Handle the video streaming logic here
    # For example, start streaming the video to a player or save it for later playback
    print(f"Received request to stream video: {video_path}")

    return jsonify({"status": "success", "message": "Streaming started"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

