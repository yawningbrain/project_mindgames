"""Main entry point for Emotiv LSL server."""

import sys
import argparse
from emotiv_lsl.emotiv_epoc_x import EmotivEpocX
from emotiv_lsl.logger import setup_logger
from config import LOG_LEVEL, LOG_FILE


def main():
    """Run the Emotiv LSL server."""
    parser = argparse.ArgumentParser(
        description='Emotiv EPOC X LSL Server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                    # Run with default settings
  python main.py --log-level DEBUG  # Run with debug logging
        '''
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default=LOG_LEVEL,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set logging level (default: %(default)s)'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        default=LOG_FILE if LOG_FILE else None,
        help='Path to log file (default: console only)'
    )
    
    args = parser.parse_args()
    
    # Setup logger
    logger = setup_logger(
        name='main',
        level=args.log_level,
        log_file=args.log_file
    )
    
    logger.info("="*60)
    logger.info("Emotiv EPOC X LSL Server")
    logger.info("="*60)
    
    try:
        emotiv_epoc_x = EmotivEpocX()
        emotiv_epoc_x.main_loop()
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
