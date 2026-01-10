#!/usr/bin/env python3
"""
Episode Splitter - Splits long stories into 2-minute episodes
"""
from utils.logger import setup_logger
import re

logger = setup_logger()

class EpisodeSplitter:
    def __init__(self, target_words_per_episode=350):
        """
        Initialize episode splitter
        
        Args:
            target_words_per_episode: Target words per episode (350 words ≈ 2 minutes)
        """
        self.target_words_per_episode = target_words_per_episode
        logger.info(f"Episode Splitter initialized: ~{target_words_per_episode} words per episode")
    
    def split_story(self, story: str, title: str):
        """
        Split story into episodes of approximately 2 minutes each
        
        Args:
            story: Full story text
            title: Story title
            
        Returns:
            List of episode dictionaries with story text and metadata
        """
        # Split story into paragraphs
        paragraphs = [p.strip() for p in story.split('\n\n') if p.strip()]
        
        logger.info(f"Story has {len(paragraphs)} paragraphs")
        
        # Group paragraphs into episodes
        episodes = []
        current_episode = []
        current_word_count = 0
        
        for para in paragraphs:
            para_words = len(para.split())
            
            # If adding this paragraph exceeds target significantly, start new episode
            if current_word_count > 0 and (current_word_count + para_words) > (self.target_words_per_episode * 1.3):
                # Save current episode
                episode_text = '\n\n'.join(current_episode)
                episodes.append({
                    'text': episode_text,
                    'word_count': current_word_count
                })
                
                # Start new episode with this paragraph
                current_episode = [para]
                current_word_count = para_words
            else:
                # Add to current episode
                current_episode.append(para)
                current_word_count += para_words
        
        # Don't forget the last episode
        if current_episode:
            episode_text = '\n\n'.join(current_episode)
            episodes.append({
                'text': episode_text,
                'word_count': current_word_count
            })
        
        # Add metadata to each episode
        total_episodes = len(episodes)
        for i, episode in enumerate(episodes, 1):
            episode['episode_number'] = i
            episode['total_episodes'] = total_episodes
            episode['title'] = f"{title} - Part {i}/{total_episodes}"
            episode['base_title'] = title
        
        logger.info(f"✓ Story split into {total_episodes} episodes")
        for i, ep in enumerate(episodes, 1):
            logger.info(f"  Episode {i}: {ep['word_count']} words (~{ep['word_count']//150} min)")
        
        return episodes
    
    def get_episode_caption(self, episode: dict, category: str):
        """
        Generate caption for an episode
        
        Args:
            episode: Episode dictionary
            category: Story category
            
        Returns:
            Caption parts (title_line, part_indicator, next_info)
        """
        ep_num = episode['episode_number']
        total = episode['total_episodes']
        base_title = episode['base_title']
        
        # Episode 1: "🔥 NEW STORY!"
        if ep_num == 1:
            title_line = f"🔥 NEW STORY: {base_title}"
            part_indicator = f"Part {ep_num}/{total}"
            if total > 1:
                next_info = f"▶️ Next episode in 15 mins!"
            else:
                next_info = ""
        
        # Last episode: "FINALE"
        elif ep_num == total:
            title_line = f"✨ FINALE: {base_title}"
            part_indicator = f"Part {ep_num}/{total}"
            next_info = f"🔄 New story in 3 hours!"
        
        # Middle episodes
        else:
            title_line = base_title
            part_indicator = f"Part {ep_num}/{total}"
            next_info = f"▶️ Next in 15 mins!"
        
        return {
            'title_line': title_line,
            'part_indicator': part_indicator,
            'next_info': next_info
        }
