# WebSocket Server for Testing

This folder contains example WebSocket servers you can run on your PC to test the mobile app.

## Python Server (Recommended)

### Prerequisites

```bash
pip install websockets
```

### Run the server

```bash
python server.py
```

The server will start on `ws://0.0.0.0:5000`

### Find your PC's IP address

**Windows (PowerShell)**:

```powershell
ipconfig
```

Look for "IPv4 Address" under your active network adapter (usually starts with 192.168.x.x)

**macOS/Linux**:

```bash
ifconfig
```

or

```bash
ip addr show
```

Then use this IP in your mobile app, e.g., `ws://192.168.1.42:5000`
