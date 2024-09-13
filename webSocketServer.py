from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

vlc_process = None
current_video_url = None

@app.route('/stream', methods=['POST'])
def stream_video():
    global vlc_process, current_video_url
    data = request.json
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400
    
    # Stop any existing VLC process
    if vlc_process and vlc_process.poll() is None:
        vlc_process.terminate()
        vlc_process.wait()

    # VLC command to stream the video
    vlc_command = f"cvlc --fullscreen --play-and-exit {video_url}"
    
    try:
        # Run VLC command to stream the video
        vlc_process = subprocess.Popen(vlc_command, shell=True)
        current_video_url = video_url  # Track the current video URL
        return jsonify({'message': 'Streaming started successfully'}), 200
    except Exception as e:
        current_video_url = None
        return jsonify({'error': str(e)}), 500


@app.route('/status', methods=['GET'])
def stream_status():
    global vlc_process, current_video_url
    # Check if VLC is running
    if vlc_process and vlc_process.poll() is None:
        return jsonify({'status': 'streaming', 'video_url': current_video_url}), 200
    else:
        return jsonify({'status': 'idle', 'video_url': None}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
