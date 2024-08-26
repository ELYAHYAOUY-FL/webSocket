from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/stream', methods=['POST'])
def stream_video():
    data = request.json
    video_url = data.get('video_url')

    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400

    # VLC command to stream the video
    vlc_command = f"cvlc --fullscreen --play-and-exit {video_url}"

    try:
        # Run VLC command to stream the video
        subprocess.Popen(vlc_command, shell=True)
        return jsonify({'message': 'Streaming started successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

