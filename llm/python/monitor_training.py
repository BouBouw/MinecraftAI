#!/usr/bin/env python3
"""
Quick training stats monitor - Shows current learning progress
"""
import sys
import json
import sqlite3
from pathlib import Path

# Get script directory for absolute paths
SCRIPT_DIR = Path(__file__).parent

def find_log_file():
    """Find training.log in common locations"""
    possible_paths = [
        SCRIPT_DIR / "training.log",
        SCRIPT_DIR / "logs" / "training.log",
        Path.home() / "MinecraftAI" / "llm" / "python" / "training.log",
        Path.cwd() / "training.log",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None

def find_db_file():
    """Find minecraft_rl.db in common locations"""
    possible_paths = [
        SCRIPT_DIR / "data" / "memories" / "minecraft_rl.db",
        SCRIPT_DIR / "data" / "minecraft_rl.db",
        Path.home() / "MinecraftAI" / "llm" / "python" / "data" / "memories" / "minecraft_rl.db",
        Path.cwd() / "data" / "memories" / "minecraft_rl.db",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None

def get_training_stats(log_file=None):
    """Parse training log and show stats"""
    if log_file is None:
        log_file = find_log_file()

    if log_file is None or not log_file.exists():
        print("❌ No log file found")
        print("💡 Searched in:")
        print("   -", SCRIPT_DIR / "training.log")
        print("   -", SCRIPT_DIR / "logs" / "training.log")
        print("   -", Path.cwd() / "training.log")
        return

    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()

        # Extract episodes
        episodes = []
        for line in lines:
            try:
                data = json.loads(line)
                if 'episode' in data and 'reward' in data:
                    episodes.append(data)
            except:
                pass

        if not episodes:
            print("❌ No episode data found yet")
            return

        # Show recent episodes
        print(f"\n📊 {len(episodes)} episodes completed")
        print("="*60)

        # Last 10 episodes
        recent = episodes[-10:] if len(episodes) >= 10 else episodes
        for ep in recent:
            stage = ep.get('curriculum_stage', 'unknown')
            reward = ep.get('reward', 0)
            length = ep.get('length', 0)
            print(f"Episode {ep.get('episode', '?'):3d}: reward={reward:8.1f}, length={length:4d}, stage={stage}")

        # Calculate average
        if len(episodes) >= 10:
            recent_avg = sum(e['reward'] for e in episodes[-10:]) / 10
            print(f"\n📈 Avg reward (last 10): {recent_avg:.1f}")

        # Show best
        best = max(episodes, key=lambda x: x['reward'])
        print(f"🏆 Best reward: {best['reward']:.1f} (Episode {best['episode']})")

    except FileNotFoundError:
        print(f"❌ Log file not found: {log_file}")
    except Exception as e:
        print(f"❌ Error reading log file: {e}")

def show_db_stats(db_path=None):
    """Show database stats"""
    if db_path is None:
        db_path = find_db_file()

    if db_path is None or not db_path.exists():
        print("❌ No database found")
        print("💡 Searched in:")
        print("   -", SCRIPT_DIR / "data" / "memories" / "minecraft_rl.db")
        print("   -", SCRIPT_DIR / "data" / "minecraft_rl.db")
        return

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get episode count
        cursor.execute("SELECT COUNT(*) FROM episodes")
        count = cursor.fetchone()[0]
        print(f"\n💾 Database: {count} episodes stored")

        # Recent episodes
        cursor.execute("""
            SELECT episode_id, stage, total_reward, death_cause
            FROM episodes
            ORDER BY id DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
        if rows:
            print("\n📜 Recent DB entries:")
            for row in rows:
                print(f"  ID {row[0]}: Stage {row[1]}, Reward {row[2]:.1f}, Died: {row[3] or 'No'}")

        conn.close()
    except sqlite3.OperationalError as e:
        print(f"❌ Database error: {e}")
        print(f"💡 Tried: {db_path}")
    except Exception as e:
        print(f"❌ Error accessing database: {e}")

if __name__ == "__main__":
    print("🔍 Minecraft RL Training Monitor\n")
    get_training_stats()
    show_db_stats()
    print("\n💡 Run this periodically to check progress")
