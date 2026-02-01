#!/usr/bin/env python3
"""
Update minecraft_bot_bridge.py on server to add create() method
"""

import re

file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if create method already exists
if 'async def create(cls' in content:
    print("✅ create() method already exists")
    exit(0)

# Find the __init__ method and add imports first
if 'from gym_env.observations import create_observation_space' not in content:
    # Add imports
    content = content.replace(
        'from utils.logger import get_logger',
        '''from utils.logger import get_logger
from gym_env.observations import create_observation_space
from gym_env.actions import create_action_space'''
    )

# Update __init__ to add observation_space and action_space
old_init = '''    def __init__(self, bridge_host: str = 'localhost', bridge_port: int = 8765):
        """
        Initialize Minecraft environment

        Args:
            bridge_host: Bridge server host
            bridge_port: Bridge port
        """
        self.bridge = MinecraftBotBridge(bridge_host, bridge_port)

        # Action mapping'''

new_init = '''    def __init__(self, bridge_host: str = 'localhost', bridge_port: int = 8765):
        """
        Initialize Minecraft environment

        Args:
            bridge_host: Bridge server host
            bridge_port: Bridge port
        """
        self.bridge = MinecraftBotBridge(bridge_host, bridge_port)

        # Get config for spaces
        from utils.config import get_config
        config = get_config()

        # Create observation and action spaces
        self.observation_space = create_observation_space(config)
        self.action_space = create_action_space(config)

        # Action mapping'''

content = content.replace(old_init, new_init)

# Add create() method after __init__ and before action_names
create_method = '''
    @classmethod
    async def create(cls, host: str = 'localhost', port: int = 8765):
        """
        Create and connect a Minecraft environment asynchronously

        Args:
            host: Bridge server host
            port: Bridge port

        Returns:
            Connected MinecraftEnvironment instance
        """
        logger.info(f"🌉 Creating Minecraft environment connected to {host}:{port}...")

        # Create instance
        env = cls(bridge_host=host, bridge_port=port)

        # Connect to the bridge
        await env.bridge.connect()

        logger.info("✅ Minecraft environment connected and ready!")

        return env

'''

# Insert create method before action_names
marker = '        # Action mapping\n        self.action_names = {'
content = content.replace(marker, create_method + marker)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Updated minecraft_bot_bridge.py with create() method")
print("✅ Added observation_space and action_space to __init__")
