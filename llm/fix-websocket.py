#!/usr/bin/env python3
"""
Fix WebSocket connection in minecraft_bot_bridge.py on server
Changes from websockets.serve() to websockets.connect()
"""

file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'websockets.connect' in content:
    print("✅ WebSocket connection already fixed")
    exit(0)

# Fix the connect method
old_connect = '''    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            logger.info(f"🔌 Connecting to WebSocket server at {self.host}:{self.port}...")

            self.ws = await websockets.serve(
                f"ws://{self.host}:{self.port}",
                ping_interval=30
            )

            logger.info("✅ Connected to Minecraft bot via WebSocket")
            self.connected = True

            # Start listening for messages
            await self.listen()

        except Exception as e:
            logger.error(f"❌ Failed to connect: {e}")
            raise'''

new_connect = '''    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            logger.info(f"🔌 Connecting to WebSocket server at {self.host}:{self.port}...")

            # Connect as client to the Node.js WebSocket server
            self.ws = await websockets.connect(
                f"ws://{self.host}:{self.port}",
                ping_interval=30,
                ping_timeout=20,
                close_timeout=10
            )

            logger.info("✅ Connected to Minecraft bot via WebSocket")
            self.connected = True

            # Start listening for messages
            await self.listen()

        except Exception as e:
            logger.error(f"❌ Failed to connect: {e}")
            raise'''

if old_connect in content:
    content = content.replace(old_connect, new_connect)

    # Write back
    with open(file_path, 'w') as f:
        f.write(content)

    print("✅ Fixed WebSocket connection in minecraft_bot_bridge.py")
    print("   Changed from websockets.serve() to websockets.connect()")
else:
    print("⚠️  Could not find the connect method to fix")
    print("   It may already be fixed or have a different format")
