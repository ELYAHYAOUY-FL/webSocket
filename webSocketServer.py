import asyncio
import websockets

async def test_connection():
    backend_server_ip = "10.130.155.35"  # Your backend server IP
    raspberry_pi_ip = "10.130.152.151"   # Raspberry Pi IP
    uri = f"ws://{backend_server_ip}:5189/videoStreamHub?raspberryPiIp={raspberry_pi_ip}"

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the backend server")

            # Send a "Ping" message to the backend
            await websocket.send("Ping from Raspberry Pi")
            print("Sent: Ping from Raspberry Pi")

            # Wait for the backend to respond with a "Pong"
            response = await websocket.recv()
            print(f"Received: {response}")

    except Exception as e:
        print(f"Connection failed: {e}")

# Run the connection test
asyncio.run(test_connection())
