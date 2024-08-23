import asyncio
import websockets
import subprocess

async def handle_stream_request(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        if message.startswith("stream:"):
            video_path = message.split(":", 1)[1]
            # Construct the VLC command to stream the video
            command = [
                'cvlc',  # Command for VLC
                video_path,  # Path to the video file
                '--sout', '#rtp{sdp=rtsp://:8554/stream}',  # Streaming options
                '--no-sout-all', '--sout-keep'
            ]
            # Run the VLC command
            subprocess.Popen(command)
            print(f"Started streaming {video_path}")

async def main():
    server = await websockets.serve(handle_stream_request, '0.0.0.0', 8765)
    print("WebSocket server started on port 8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
