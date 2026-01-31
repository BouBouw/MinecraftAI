# 🎮 How to Run the Minecraft RL AI

**The AI can now actually play Minecraft!** 🎉

This guide shows you how to start the complete system and watch the AI learn.

---

## 📋 Prerequisites

### 1. Minecraft Server
You need a Minecraft server running (local or remote):
- Vanilla or Fabric server
- Survival mode (recommended for learning)
- Server accessible from where you run the AI

### 2. Environment File
Create a `.env` file in the project root:

```bash
# Minecraft Server Connection
MC_HOST=localhost
MC_PORT=25565
MC_USERNAME=RLAgent
```

**For local server:**
```bash
MC_HOST=localhost
MC_PORT=25565
```

**For remote server (OVH):**
```bash
MC_HOST=your-ovh-server-ip
MC_PORT=25565
```

### 3. Python & Node.js
- Python 3.10+
- Node.js 18+
- npm

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Minecraft Server
Start your Minecraft server (local or remote).

### Step 2: Start the RL System
```bash
cd /path/to/MinecraftAI
./llm/start-rl-minecraft.sh
```

**What happens:**
1. ✅ Connects bot to Minecraft server
2. ✅ Starts bridge server (WebSocket communication)
3. ✅ Starts TensorBoard (monitoring)
4. ✅ Starts RL training (AI begins learning!)

### Step 3: Watch the AI Learn!
```bash
# Terminal 1: Live monitoring
./llm/monitor.sh --live

# Terminal 2: Training logs
tail -f llm/data/logs/training.log

# Browser: TensorBoard
http://localhost:6006
```

---

## 📊 What You'll See

### In Minecraft:
- A bot named `RLAgent` will join the server
- It will start moving, mining, and exploring
- It will die often at first (that's how it learns!)
- Over time, it will get smarter

### In Terminal:
```
🚀 Starting Minecraft RL AI System...
   MC Server: localhost:25565
   Username: RLAgent

🎮 Connecting to Minecraft server...
✅ Bot spawned in world!
   Position: Vec3(x=100, y=64, z=-200)
   Health: 20/20
   Food: 20/20

🌉 Starting bridge server...
✅ Bridge is ready!

🤖 Starting RL training...
Episode 1
   Step 100 | Reward: -5.20 | Total: -45.30
   Step 200 | Reward: 2.10 | Total: -12.50
✅ Episode 1 complete
   Length: 342 steps
   Total reward: -15.20

Episode 2
🏆 New best reward: 8.50
💾 Checkpoint saved
...
```

### In TensorBoard:
- Training rewards over time
- Episode lengths
- Loss curves
- Exploration metrics

---

## 🎯 Learning Progression

### First 24 Hours (Steps 0-1M)
- AI learns to move without falling
- Starts mining basic blocks (dirt, stone, wood)
- Discovers 1-5 crafts
- Dies frequently (this is normal!)

### Days 2-3 (Steps 1M-10M)
- Movement becomes smooth
- Mines efficiently
- Discovers 10-20 crafts
- Starts surviving longer

### Days 5-7 (Steps 10M-25M)
- 30+ crafts discovered
- Builds basic shelters
- Survives nights sometimes
- Develops strategies

### 2-4 Weeks (Steps 100M+)
- AI is quasi-autonomous
- 50+ crafts discovered
- Builds complex structures
- Survives consistently
- **Can actually play Minecraft!**

---

## 🛑 Stopping the System

```bash
./llm/start-rl-minecraft.sh stop
```

This stops:
- RL training
- Bridge server
- Minecraft bot
- TensorBoard

---

## 📁 Important Files

### Logs
- `llm/data/logs/training.log` - Training progress
- `llm/data/logs/bridge.log` - Bridge communication
- `llm/data/logs/tensorboard.log` - TensorBoard output

### Models (Saved Checkpoints)
- `llm/data/models/checkpoint_ep*.pt` - Model checkpoints
- `llm/data/models/model_step_*.pt` - Step-based checkpoints

### Database
- `llm/data/memories/minecraft_rl.db` - All memories
  - Long-term knowledge
  - Episode history
  - Discovered recipes
  - Semantic concepts

---

## 🔧 Troubleshooting

### Bot can't connect to server
**Problem:** "Failed to connect to Minecraft server"

**Solutions:**
1. Check server is running: `ping $MC_HOST`
2. Check port: `telnet $MC_HOST $MC_PORT`
3. Verify `.env` file has correct values
4. Check firewall settings

### Bot connects but doesn't move
**Problem:** Bot spawns but stands still

**Solutions:**
1. Check bot is in survival mode (not spectator)
2. Give it time to initialize (5-10 seconds)
3. Check `bridge.log` for errors
4. Try restarting: `./llm/start-rl-minecraft.sh stop && ./llm/start-rl-minecraft.sh`

### High RAM usage
**Problem:** System using too much memory

**Solutions:**
1. Reduce batch size in `llm/config/rl_config.yaml`
2. Reduce memory capacity:
   ```yaml
   memory:
     short_term:
       capacity: 5000  # instead of 10000
   ```

### Training is slow
**Problem:** Not enough steps per second

**Solutions:**
1. Use OVH server with more cores
2. Increase batch size in config
3. Reduce observation complexity
4. Use curriculum mode (starts simple)

---

## 🎮 Customizing Training

### Change Training Duration
```bash
# 10M steps instead of 100M
./llm/start-rl-minecraft.sh 10000000
```

### Change Server Connection
Edit `.env`:
```bash
MC_HOST=mc.hypixel.net
MC_PORT=25565
MC_USERNAME=MyRLBot
```

### Skip TensorBoard
Edit `start-rl-minecraft.sh`, comment out TensorBoard section

### Start from Checkpoint
```bash
python llm/python/training/real_minecraft_trainer.py \
    --checkpoint llm/data/models/checkpoint_ep50.pt \
    --steps 20000000
```

---

## 📊 Monitoring Commands

### Quick Status
```bash
./llm/monitor.sh
```

Shows:
- Process status (running/stopped)
- Current episode
- Recent rewards
- Model checkpoints
- Memory database stats

### Live Monitoring
```bash
./llm/monitor.sh --live
```
Updates every 5 seconds with:
- System resources (CPU, RAM, disk)
- Training progress
- Recent rewards
- Current curriculum stage

### View Training Logs
```bash
tail -f llm/data/logs/training.log
```

### Check Bot Position
```bash
sqlite3 llm/data/memories/minecraft_rl.db \
    "SELECT * FROM long_term_memory ORDER BY timestamp DESC LIMIT 10;"
```

---

## 🎉 Success Indicators

### Your AI is learning if:
- ✅ Total reward increases over episodes
- ✅ Episode lengths get longer
- ✅ New crafts appear in database
- ✅ Bot survives longer before dying
- ✅ Checkpoint files are created

### Expected timeline:
- **Day 1**: Negative rewards, lots of deaths (normal!)
- **Day 2-3**: First positive rewards, basic crafts
- **Day 7**: Consistently positive rewards
- **Day 14**: AI can survive independently

---

## 🚀 Advanced: OVH Deployment

For 24/7 training on OVH server:

1. **Upload project to OVH:**
   ```bash
   scp -r MinecraftAI root@ovh-server:/opt/
   ```

2. **SSH to OVH:**
   ```bash
   ssh root@ovh-server
   cd /opt/MinecraftAI
   ```

3. **Run deployment script:**
   ```bash
   ./llm/deploy_ovh.sh
   ```

4. **Start training:**
   ```bash
   ./llm/start-rl-minecraft.sh
   ```

5. **Monitor remotely:**
   ```bash
   # Local machine
   ssh -L 6006:localhost:6006 root@ovh-server
   # Open: http://localhost:6006
   ```

See [DEPLOYMENT_OVH.md](DEPLOYMENT_OVH.md) for full details.

---

## 🆘 Getting Help

### Check system status
```bash
./llm/monitor.sh
```

### View errors
```bash
./llm/monitor.sh --errors
```

### Check logs
```bash
# Training errors
grep -i error llm/data/logs/training.log | tail -20

# Bridge errors
grep -i error llm/data/logs/bridge.log | tail -20

# Recent deaths
grep "died" llm/data/logs/training.log | tail -10
```

---

## 🎊 What's Next?

Once training is running:

1. **Watch it play** - The most fun part!
2. **Monitor progress** - TensorBoard graphs
3. **Check discoveries** - What crafts has it learned?
4. **Share results** - Show off your AI!

### Exporting the trained model:
```bash
# The best model is saved at:
llm/data/models/checkpoint_epXXX.pt
```

You can use this model to:
- Continue training
- Run inference (let it play without learning)
- Share with others
- Analyze what it learned

---

## 📝 Summary

**You now have a complete AI system that:**
- ✅ Connects to real Minecraft server
- ✅ Plays survival mode
- ✅ Learns from experience
- ✅ Discovers crafts autonomously
- ✅ Improves over time
- ✅ Remembers everything

**Just run:**
```bash
./llm/start-rl-minecraft.sh
```

**And watch it learn!** 🤖✨

---

**Enjoy your autonomous Minecraft AI!** 🎮🚀
