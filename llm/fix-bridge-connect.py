#!/usr/bin/env python3
"""
Fix bridge connection - make listener run in background
"""

file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if 'asyncio.create_task(self._listen_loop())' in content:
    print("✅ Bridge connection already fixed")
    exit(0)

# Fix 1: Update connect() to create background task
old_connect = '''    async def connect(self):
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

            # Don't start listening here - let the training loop control when to listen
            # The listen loop will be started when needed

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

            # Start listening for messages in background
            # This won't block - it creates a background task
            asyncio.create_task(self._listen_loop())

        except Exception as e:
            logger.error(f"❌ Failed to connect: {e}")
            raise'''

# Fix 2: Rename listen() to _listen_loop()
old_listen = '    async def listen(self):'
new_listen = '    async def _listen_loop(self):'

if old_connect in content:
    content = content.replace(old_connect, new_connect)
    content = content.replace(old_listen, new_listen)

    # Write back
    with open(file_path, 'w') as f:
        f.write(content)

    print("✅ Fixed bridge connection - listener now runs in background")
else:
    print("⚠️  Could not find the connect method to fix")
