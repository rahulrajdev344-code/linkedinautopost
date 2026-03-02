"""
Main orchestrator: Generate a tech post using AI and publish it to LinkedIn.
"""

import sys
import logging
from datetime import datetime, timezone

from generate_post import generate_post, load_random_topic
from post_to_linkedin import post_to_linkedin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main(dry_run: bool = False) -> None:
    """Generate and post content to LinkedIn."""

    logger.info("=" * 60)
    logger.info("LinkedIn Auto Poster — Starting run")
    logger.info(f"Time: {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 60)

    # Step 1: Pick a topic
    topic = load_random_topic()
    logger.info(f"Selected topic: {topic}")

    # Step 2: Generate post content
    logger.info("Generating post with OpenRouter (DeepSeek R1)...")
    try:
        post_content = generate_post(topic)
    except Exception as e:
        logger.error(f"Failed to generate post: {e}")
        sys.exit(1)

    logger.info(f"Generated post ({len(post_content)} chars):")
    logger.info("-" * 40)
    logger.info(post_content)
    logger.info("-" * 40)

    # Step 3: Post to LinkedIn (or dry-run)
    if dry_run:
        logger.info("[DRY RUN] Skipping LinkedIn post. Content above would have been posted.")
        return

    logger.info("Publishing to LinkedIn...")
    try:
        result = post_to_linkedin(post_content)
    except Exception as e:
        logger.error(f"Failed to post to LinkedIn: {e}")
        sys.exit(1)

    if result["success"]:
        logger.info(f"✅ {result['details']}")
    else:
        logger.error(f"❌ Post failed: {result['details']}")
        sys.exit(1)

    logger.info("Run complete!")


if __name__ == "__main__":
    is_dry_run = "--dry-run" in sys.argv
    main(dry_run=is_dry_run)
