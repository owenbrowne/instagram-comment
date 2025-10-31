#!/usr/bin/env python3
"""
Instagram Comment Bot
Continuously comments on a specified Instagram post
⚠️ WARNING: Use at your own risk. This may violate Instagram's ToS and lead to account suspension.
"""

import os
import sys
import time
import random
import logging
import json
from datetime import datetime
from pathlib import Path

try:
    from instagrapi import Client
    from instagrapi.exceptions import (
        LoginRequired,
        ChallengeRequired,
        FeedbackRequired,
        PleaseWaitFewMinutes,
        ClientError
    )
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class InstagramCommentBot:
    """Bot that continuously comments on an Instagram post"""
    
    def __init__(self):
        """Initialize the bot with configuration from .env file"""
        load_dotenv('config.env')
        
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.post_url = os.getenv('POST_URL')
        self.min_delay = int(os.getenv('MIN_DELAY', 300))
        self.max_delay = int(os.getenv('MAX_DELAY', 600))
        self.comments = [c.strip() for c in os.getenv('COMMENTS', '').split(',') if c.strip()]
        
        self._validate_config()
        
        self.client = Client()
        self.session_file = Path('session.json')
        self.stats_file = Path('comment_stats.json')
        self.comment_count = 0
        self.session_comment_count = 0
        self.start_time = datetime.now()
        
        # Load existing stats
        self._load_stats()
        
    def _validate_config(self):
        """Validate configuration parameters"""
        if not self.username or self.username == 'your_username_here':
            logger.error("❌ Instagram username not set in config.env")
            sys.exit(1)
            
        if not self.password or self.password == 'your_password_here':
            logger.error("❌ Instagram password not set in config.env")
            sys.exit(1)
            
        if not self.post_url or 'EXAMPLE' in self.post_url:
            logger.error("❌ Post URL not set in config.env")
            sys.exit(1)
            
        if not self.comments or self.comments == ['']:
            logger.error("❌ No comments configured in config.env")
            sys.exit(1)
            
        if self.min_delay < 60:
            logger.warning("⚠️  Delay is very short. Risk of detection is HIGH!")
    
    def _load_stats(self):
        """Load comment statistics from JSON file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    stats = json.load(f)
                    self.comment_count = stats.get('total_comments', 0)
                    logger.info(f"📊 Loaded stats: {self.comment_count} total comments posted previously")
            except Exception as e:
                logger.warning(f"⚠️  Could not load stats file: {e}")
                self.comment_count = 0
        else:
            # Initialize with 65 comments if file doesn't exist
            self.comment_count = 65
            self._save_stats()
            logger.info(f"📊 Initialized stats file with {self.comment_count} comments")
    
    def _save_stats(self):
        """Save comment statistics to JSON file"""
        try:
            stats = {
                'total_comments': self.comment_count,
                'last_updated': datetime.now().isoformat(),
                'last_post_url': self.post_url
            }
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Could not save stats: {e}")
            
    def login(self):
        """Login to Instagram with session persistence"""
        logger.info(f"🔐 Logging in as {self.username}...")
        
        # Try to load existing session
        if self.session_file.exists():
            try:
                logger.info("📂 Loading existing session...")
                self.client.load_settings(self.session_file)
                self.client.login(self.username, self.password)
                
                # Verify session is valid
                self.client.get_timeline_feed()
                logger.info("✅ Session loaded successfully")
                return
            except Exception as e:
                logger.warning(f"⚠️  Failed to load session: {e}")
                logger.info("🔄 Creating new session...")
        
        # Create new session
        try:
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)
            logger.info("✅ Logged in successfully and session saved")
        except ChallengeRequired as e:
            logger.error("❌ Challenge required. Instagram needs verification.")
            logger.error("   Please login manually through the Instagram app first.")
            sys.exit(1)
        except LoginRequired as e:
            logger.error(f"❌ Login failed: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Unexpected error during login: {e}")
            sys.exit(1)
    
    def extract_media_id(self):
        """Extract media ID from Instagram post URL"""
        try:
            logger.info(f"🔍 Extracting media ID from URL: {self.post_url}")
            media_pk = self.client.media_pk_from_url(self.post_url)
            logger.info(f"✅ Media ID: {media_pk}")
            return media_pk
        except Exception as e:
            logger.error(f"❌ Failed to extract media ID: {e}")
            logger.error("   Make sure the URL is valid and the post is public")
            sys.exit(1)
    
    def post_comment(self, media_id):
        """Post a random comment on the specified media"""
        comment_text = random.choice(self.comments)
        
        try:
            logger.info(f"💬 Posting comment: '{comment_text}'")
            self.client.media_comment(media_id, comment_text)
            self.comment_count += 1
            self.session_comment_count += 1
            self._save_stats()
            
            elapsed = datetime.now() - self.start_time
            logger.info(f"✅ Comment posted successfully")
            logger.info(f"📊 Session: {self.session_comment_count} | Total all-time: {self.comment_count}")
            return True
            
        except FeedbackRequired as e:
            logger.error(f"❌ Instagram feedback required: {e}")
            logger.error("   You may have been rate limited or flagged. Stopping bot.")
            return False
            
        except PleaseWaitFewMinutes as e:
            logger.warning(f"⚠️  Rate limited: {e}")
            logger.info("⏳ Waiting 15 minutes before retrying...")
            time.sleep(900)  # Wait 15 minutes
            return True  # Continue running
            
        except ClientError as e:
            logger.error(f"❌ Client error: {e}")
            if "challenge_required" in str(e).lower():
                logger.error("   Account needs verification. Please verify manually.")
                return False
            elif "login_required" in str(e).lower():
                logger.info("🔄 Session expired. Re-logging in...")
                self.login()
                return True
            else:
                logger.warning(f"   Unexpected error, waiting 5 minutes...")
                time.sleep(300)
                return True
                
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            logger.info("⏳ Waiting 5 minutes before continuing...")
            time.sleep(300)
            return True
    
    def run(self):
        """Main bot loop"""
        logger.info("🤖 Instagram Comment Bot Starting...")
        logger.info("=" * 60)
        logger.info(f"📋 Configuration:")
        logger.info(f"   Username: {self.username}")
        logger.info(f"   Post URL: {self.post_url}")
        logger.info(f"   Delay: {self.min_delay}-{self.max_delay} seconds")
        logger.info(f"   Comments pool: {len(self.comments)} variations")
        logger.info("=" * 60)
        logger.info("⚠️  WARNING: This bot may violate Instagram's Terms of Service")
        logger.info("⚠️  Your account may be banned. Use at your own risk!")
        logger.info("=" * 60)
        
        # Login
        self.login()
        
        # Get media ID
        media_id = self.extract_media_id()
        
        logger.info("🚀 Starting comment loop...")
        logger.info("   Press Ctrl+C to stop the bot")
        logger.info("")
        
        try:
            while True:
                # Post comment
                should_continue = self.post_comment(media_id)
                
                if not should_continue:
                    logger.error("🛑 Bot stopped due to critical error")
                    break
                
                # Random delay between comments (weighted towards minimum)
                # Using triangular distribution to favor shorter delays
                delay = int(random.triangular(self.min_delay, self.max_delay, self.min_delay + (self.max_delay - self.min_delay) * 0.3))
                
                if delay >= 60:
                    logger.info(f"⏸️  Waiting {delay} seconds ({delay/60:.1f} minutes) before next comment...")
                else:
                    logger.info(f"⏸️  Waiting {delay} seconds before next comment...")
                logger.info("")
                
                time.sleep(delay)
                
        except KeyboardInterrupt:
            logger.info("")
            logger.info("=" * 60)
            logger.info("🛑 Bot stopped by user")
            logger.info(f"📊 This session: {self.session_comment_count} comments")
            logger.info(f"📊 TOTAL COMMENTS POSTED: {self.comment_count}")
            logger.info(f"⏱️  Session runtime: {datetime.now() - self.start_time}")
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            logger.info(f"📊 This session: {self.session_comment_count} comments")
            logger.info(f"📊 TOTAL COMMENTS POSTED: {self.comment_count}")
            sys.exit(1)


def main():
    """Entry point for the bot"""
    bot = InstagramCommentBot()
    bot.run()


if __name__ == "__main__":
    main()

