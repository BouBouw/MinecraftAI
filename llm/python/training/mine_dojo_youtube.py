"""
Learn from YouTube Videos using MineDojo WebDataset

This script uses MineDojo's massive dataset of 73,000+ Minecraft YouTube videos
to generate demonstrations for imitation learning.

The dataset includes:
- 73,000+ YouTube videos
- 2.2 billion frames
- Text descriptions of what's happening
- Wiki articles linked to videos

Requirements:
    pip install minedojo

Usage:
    python mine_dojo_youtube.py --num_videos 100 --output ../data/demos/youtube_demos.pkl
"""

import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json

try:
    from minedojo.data import MineDojoWebDataset
except ImportError:
    print("❌ MineDojo not installed. Install with:")
    print("   pip install minedojo")
    print("\nOr visit: https://github.com/MineDojo/MineDojo")
    exit(1)

from utils.logger import get_logger

logger = get_logger(__name__)


class YouTubeDemoExtractor:
    """Extract demonstrations from YouTube videos using MineDojo"""

    def __init__(self, split: str = "train"):
        """
        Initialize YouTube demo extractor

        Args:
            split: Dataset split ("train", "val", or "test")
        """
        self.split = split
        self.episode_count = 0

        logger.info(f"🎬 Loading MineDojo WebDataset ({split} split)...")

        # Load MineDojo WebDataset
        self.dataset = MineDojoWebDataset(split=split)

        logger.info(f"✅ Dataset loaded: {len(self.dataset)} videos")

    def extract_from_videos(self, num_videos: int = 100) -> List[Dict]:
        """
        Extract demonstrations from YouTube videos

        Args:
            num_videos: Number of videos to process

        Returns:
            List of demonstrations extracted from videos
        """
        all_demos = []

        logger.info(f"🎬 Extracting demos from {num_videos} YouTube videos...")

        for idx, (video_frames, video_info) in enumerate(self.dataset):
            if idx >= num_videos:
                break

            try:
                # Process video
                demo = self._process_video(video_frames, video_info)
                if demo:
                    all_demos.append(demo)

                # Progress update
                if (idx + 1) % 10 == 0:
                    logger.info(f"📊 Processed {idx + 1}/{num_videos} videos")

            except Exception as e:
                logger.error(f"❌ Error processing video {idx}: {e}")
                continue

        logger.info(f"✅ Extracted {len(all_demos)} demonstrations")
        return all_demos

    def _process_video(self, video_frames, video_info: Dict) -> Dict:
        """
        Process a single YouTube video

        Args:
            video_frames: Video frames from MineDojo
            video_info: Metadata about the video

        Returns:
            Processed demonstration
        """
        # Extract information
        video_id = video_info.get('video_id', 'unknown')
        title = video_info.get('title', 'Unknown')
        description = video_info.get('description', '')

        # Extract frames as observations
        observations = []
        for frame in video_frames:
            obs = {
                'image': frame,  # RGB image
                'text_description': description,  # What's happening
            }
            observations.append(obs)

        # Get actions from video metadata
        # MineDojo provides action annotations for some videos
        actions = video_info.get('actions', None)

        # If no actions provided, we'll need to use vision model to detect them
        if actions is None:
            # Placeholder: use dummy actions
            # TODO: Use video understanding model to detect actions
            actions = [0] * len(observations)

        demonstration = {
            'observations': observations,
            'actions': actions,
            'video_id': video_id,
            'title': title,
            'description': description,
            'num_frames': len(observations),
            'timestamp': datetime.now().isoformat()
        }

        return demonstration


def extract_youtube_knowledge(num_videos: int = 100, output_path: str = None):
    """
    Extract knowledge from YouTube videos

    Args:
        num_videos: Number of videos to process
        output_path: Path to save extracted data
    """
    # Generate output path
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"../data/demos/youtube_demos_{timestamp}.pkl"

    logger.info(f"🤖 MineDojo YouTube Knowledge Extractor")
    logger.info(f"   Videos to process: {num_videos}")
    logger.info(f"   Output: {output_path}")

    # Create extractor
    try:
        extractor = YouTubeDemoExtractor(split="train")
    except Exception as e:
        logger.error(f"❌ Failed to load MineDojo dataset: {e}")
        logger.error("\n💡 Make sure MineDojo is properly installed:")
        logger.error("   pip install minedojo")
        logger.error("\n💡 The WebDataset requires downloading data first:")
        logger.error("   python -c 'from minedojo.data import MineDojoWebDataset; MineDojoWebDataset.download()'")
        return

    # Extract demonstrations
    demos = extractor.extract_from_videos(num_videos=num_videos)

    # Save
    demo_data = {
        'demonstrations': demos,
        'demo_count': len(demos),
        'source': 'youtube_videos_minedojo',
        'extracted_at': datetime.now().isoformat(),
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'wb') as f:
        pickle.dump(demo_data, f)

    logger.info(f"💾 Saved {len(demos)} demos to {output_path}")
    logger.info("✅ YouTube knowledge extraction complete!")


def main():
    import sys

    # Parse arguments
    num_videos = 100
    output_path = None

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--num-videos='):
                num_videos = int(arg.split('=', 1)[1])
            elif arg.startswith('--output='):
                output_path = arg.split('=', 1)[1]

    extract_youtube_knowledge(num_videos=num_videos, output_path=output_path)


if __name__ == "__main__":
    main()
