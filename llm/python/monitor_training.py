#!/usr/bin/env python3
"""
Quick training stats monitor - Shows current learning progress
"""
import sys
import json
import sqlite3
from pathlib import Path

def get_training_stats(log_file="training.log"):
    """Parse training log and show stats"""
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

def show_db_stats(db_path="./data/memories/minecraft_rl.db"):
    """Show database stats"""
    try:
        conn = sqlite3.connect(db_path)
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
    except FileNotFoundError:
        print(f"❌ Database not found: {db_path}")

if __name__ == "__main__":
    print("🔍 Minecraft RL Training Monitor\n")
    get_training_stats()
    show_db_stats()
    print("\n💡 Run this periodically to check progress")
