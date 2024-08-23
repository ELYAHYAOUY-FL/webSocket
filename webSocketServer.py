from flask import Flask, request, Response, abort
import os

app = Flask(__name__)

@app.route('/start-stream', methods=['POST'])
def start_stream():
    data = request.get_json()
    video_path = data.get('videoPath')

    if not video_path:
        return {"status": "error", "message": "Video path not provided"}, 400

    if not os.path.isfile(video_path):
        return {"status": "error", "message": "File not found"}, 404

    def generate():
        with open(video_path, 'rb') as f:
            while True:
                chunk = f.read(1024*64)  # Adjust chunk size as needed
                if not chunk:
                    break
                yield chunk

    return Response(generate(), mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
