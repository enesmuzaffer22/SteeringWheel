"""
WebSocket Server Test Script
Quick test to verify the server can start and accept connections
"""
import asyncio
import websockets
import socket

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

async def handle_client(websocket, path):
    """Handle incoming WebSocket connections."""
    client_ip = websocket.remote_address[0] if websocket.remote_address else "Unknown"
    print(f"✅ Client connected from: {client_ip}")
    
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            # Echo back
            await websocket.send(f"Server received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"❌ Client disconnected: {client_ip}")

async def main():
    """Start the test WebSocket server."""
    host = '0.0.0.0'
    port = 5000
    
    print("=" * 70)
    print("🧪 WEBSOCKET SERVER TEST")
    print("=" * 70)
    print(f"🌐 Server starting on: {host}:{port}")
    print(f"📍 Your PC IP Address: {get_local_ip()}")
    print("")
    print("📱 On your phone, connect to:")
    print(f"   ws://{get_local_ip()}:{port}")
    print("")
    print("=" * 70)
    print("⏳ Waiting for connections...\n")
    
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
