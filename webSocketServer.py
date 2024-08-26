from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Store the process ID (PID) of the VLC instance
vlc_process = None

@app.route('/stream', methods=['POST'])
def stream_video():
    global vlc_process
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
        return jsonify({'message': 'Streaming started successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_video():
    global vlc_process

    if vlc_process and vlc_process.poll() is None:
        vlc_process.terminate()
        vlc_process.wait()
        return jsonify({'message': 'Streaming stopped successfully'}), 200
    else:
        return jsonify({'error': 'No streaming process to stop'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
