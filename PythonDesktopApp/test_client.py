"""
Test client for the Gyroscope to Keyboard Bridge
Simulates a mobile device sending gyroscope data
"""

import asyncio
import websockets
import json
import random
import time


async def test_client():
    """Connect to the server and send test gyroscope data."""
    uri = "ws://localhost:5000"
    
    print("=" * 60)
    print("🧪 Test Client for Gyroscope Bridge")
    print("=" * 60)
    print(f"Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to server!")
            print("📤 Sending test gyroscope data...")
            print("=" * 60)
            
            # Test sequence
            test_data = [
                # Turn LEFT
                {"x": -0.4, "y": 0.05, "z": 0.8, "label": "LEFT"},
                {"x": -0.35, "y": 0.03, "z": 0.82, "label": "LEFT"},
                {"x": -0.3, "y": 0.02, "z": 0.79, "label": "LEFT"},
                
                # Return to CENTER
                {"x": -0.15, "y": 0.01, "z": 0.81, "label": "CENTER"},
                {"x": 0.0, "y": 0.0, "z": 0.8, "label": "CENTER"},
                
                # Turn RIGHT
                {"x": 0.3, "y": -0.02, "z": 0.78, "label": "RIGHT"},
                {"x": 0.4, "y": -0.03, "z": 0.76, "label": "RIGHT"},
                {"x": 0.45, "y": -0.04, "z": 0.75, "label": "RIGHT"},
                
                # Return to CENTER
                {"x": 0.15, "y": 0.01, "z": 0.79, "label": "CENTER"},
                {"x": 0.0, "y": 0.0, "z": 0.8, "label": "CENTER"},
                
                # Slight left (below threshold)
                {"x": -0.1, "y": 0.01, "z": 0.81, "label": "CENTER (below threshold)"},
                
                # Random steering simulation
                {"x": -0.25, "y": 0.02, "z": 0.80, "label": "LEFT"},
                {"x": 0.28, "y": -0.01, "z": 0.79, "label": "RIGHT"},
                {"x": 0.05, "y": 0.00, "z": 0.80, "label": "CENTER"},
            ]
            
            for i, data in enumerate(test_data, 1):
                # Extract label and remove it from the data
                label = data.pop("label")
                
                # Send data to server
                message = json.dumps(data)
                await websocket.send(message)
                
                print(f"{i:2d}. Sent: x={data['x']:+.2f} y={data['y']:+.2f} z={data['z']:+.2f} [{label}]")
                
                # Wait a bit between messages (simulate real sensor data rate)
                await asyncio.sleep(0.05)  # 50ms = 20 updates per second
            
            print("=" * 60)
            print("✅ Test sequence completed!")
            print("Waiting 2 seconds before disconnect...")
            await asyncio.sleep(2)
            
    except ConnectionRefusedError:
        print("❌ ERROR: Could not connect to server!")
        print("   Make sure the server is running on localhost:5000")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    print("\n⚠️  NOTE: Make sure the server (main.py) is running first!\n")
    time.sleep(1)
    asyncio.run(test_client())
