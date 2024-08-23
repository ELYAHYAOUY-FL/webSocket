from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/start-stream', methods=['POST'])
def start_stream():
    data = request.get_json()
    video_path = data.get('videoPath')

    # Ensure the file exists
    if not os.path.exists(video_path):
        return {"status": "error", "message": "File not found"}, 404

    # Stream the video
    def generate():
        with open(video_path, 'rb') as f:
            while chunk := f.read(1024*64):  # Read in chunks
                yield chunk

    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
