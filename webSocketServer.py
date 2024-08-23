import asyncio
import websockets
import subprocess
import socket

async def handle_stream_request():
    # Get the Raspberry Pi's IP address
    raspberry_pi_ip = socket.gethostbyname(socket.gethostname())
    uri = f"ws://localhost:5189/videoStreamHub?raspberryPiIp={raspberry_pi_ip}"

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            if message.startswith("ReceiveStream:"):
                video_path = message.split(":", 1)[1]
                command = [
                    'cvlc',
                    video_path,
                    '--sout', '#rtp{sdp=rtsp://:8554/stream}',
                    '--no-sout-all', '--sout-keep'
                ]
                subprocess.Popen(command)
                print(f"Started streaming {video_path}")

async def main():
    await handle_stream_request()

if __name__ == "__main__":
    asyncio.run(main())
