#!/usr/bin/env python3
"""
Fix action wait to properly wait for action_complete message
"""

file_path = 'llm/python/bridge/minecraft_bot_bridge.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Check if it needs fixing
if '_action_complete_event' in content:
    print("✅ Action wait fix already applied")
    exit(0)

# 1. Add asyncio import if not present
if 'import asyncio' not in content:
    # Add asyncio to imports
    old_imports = "import json"
    new_imports = """import asyncio
import json"""
    content = content.replace(old_imports, new_imports)
    print("✅ Added asyncio import")

# 2. Add event flag in __init__
old_init = """        self.host = host
        self.port = port
        self.ws = None
        self.connected = False
        self.current_state = None
        self.logger = logger"""

new_init = """        self.host = host
        self.port = port
        self.ws = None
        self.connected = False
        self.current_state = None
        self.logger = logger
        self._action_complete_event = asyncio.Event()
        self._last_action_result = None"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("✅ Added event flag to __init__")
else:
    print("⚠️  Could not find __init__ section")
    exit(1)

# 3. Update _handle_action_complete to set the event
old_handler = """    async def _handle_action_complete(self, data: Dict[str, Any]):
        \"\"\"Handle action completion result\"\"\"
        success = data.get('success', False)
        action = data.get('action', {})

        logger.debug(f"Action completed: success={success}")"""

new_handler = """    async def _handle_action_complete(self, data: Dict[str, Any]):
        \"\"\"Handle action completion result\"\"\"
        success = data.get('success', False)
        action = data.get('action', {})

        # Store result and set event
        self._last_action_result = data
        self._action_complete_event.set()

        logger.debug(f"Action completed: success={success}")"""

if old_handler in content:
    content = content.replace(old_handler, new_handler)
    print("✅ Updated _handle_action_complete")
else:
    print("⚠️  Could not find _handle_action_complete")
    exit(1)

# 4. Update _wait_for_action_result to wait for the event
old_wait = """    async def _wait_for_action_result(self, timeout: float = 30.0) -> Dict[str, Any]:
        \"\"\"
        Wait for action completion result

        Args:
            timeout: Timeout in seconds

        Returns:
            Action result
        \"\"\"
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Will receive action_complete message
            await asyncio.sleep(0.1)
        else:
            logger.warning(f"Action timeout after {timeout}s")
            return {'success': False, 'timeout': True}"""

new_wait = """    async def _wait_for_action_result(self, timeout: float = 30.0) -> Dict[str, Any]:
        \"\"\"
        Wait for action completion result

        Args:
            timeout: Timeout in seconds

        Returns:
            Action result
        \"\"\"
        # Clear the event before waiting
        self._action_complete_event.clear()
        self._last_action_result = None

        # Wait for the event to be set by _handle_action_complete
        try:
            await asyncio.wait_for(self._action_complete_event.wait(), timeout=timeout)
            return self._last_action_result or {'success': True}
        except asyncio.TimeoutError:
            logger.warning(f"Action timeout after {timeout}s")
            return {'success': False, 'timeout': True}"""

if old_wait in content:
    content = content.replace(old_wait, new_wait)
    print("✅ Updated _wait_for_action_result")
else:
    print("⚠️  Could not find _wait_for_action_result")
    exit(1)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Action wait fix applied!")
