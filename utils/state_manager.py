import json
import os
from typing import Dict, Any
from utils.logger import setup_logger

logger = setup_logger()


class StateManager:
    """Manages persistent state between bot runs"""

    def __init__(self, state_file: str):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Load state from JSON file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    logger.info(f"State loaded: {state}")
                    return state
            except Exception as e:
                logger.error(f"Error loading state: {e}")
                return self._get_default_state()
        else:
            return self._get_default_state()

    def _get_default_state(self) -> Dict[str, Any]:
        """Return default state"""
        return {
            'category_index': 0,
            'video_index': 0,
            'total_runs': 0,
            'last_run': None
        }

    def save_state(self):
        """Save state to JSON file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.info(f"State saved: {self.state}")
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def get_next_category(self, categories: list) -> str:
        """Get next category in rotation"""
        index = self.state['category_index']
        category = categories[index]

        # Update index for next run
        self.state['category_index'] = (index + 1) % len(categories)

        return category

    def get_next_video_index(self, total_videos: int) -> int:
        """Get next video index in rotation"""
        index = self.state['video_index']

        # Update index for next run
        self.state['video_index'] = (index + 1) % total_videos

        return index

    def increment_run_count(self):
        """Increment total run counter"""
        self.state['total_runs'] += 1

    def update_last_run(self, timestamp: str):
        """Update last run timestamp"""
        self.state['last_run'] = timestamp