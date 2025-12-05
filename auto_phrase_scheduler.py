#!/usr/bin/env python3
"""
Auto Phrase Scheduler
Automatically monitors word supply and generates new phrases when running low.
"""

import os
import sys
import time
import schedule
import logging
from datetime import datetime, timedelta
from phrase_generator import PhraseGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phrase_scheduler.log'),
        logging.StreamHandler()
    ]
)

class AutoPhraseScheduler:
    def __init__(self, words_file='words.txt', min_days_ahead=7, generate_count=30):
        self.words_file = words_file
        self.min_days_ahead = min_days_ahead  # Generate phrases when less than this many days ahead
        self.generate_count = generate_count
        self.generator = PhraseGenerator()
        
    def get_future_phrases_count(self):
        """Count how many phrases are scheduled for future dates"""
        try:
            future_count = 0
            today = datetime.now().date()
            
            with open(self.words_file, 'r') as file:
                for line in file:
                    if ',' in line:
                        date_str, phrase = line.strip().split(', ')
                        try:
                            phrase_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                            if phrase_date > today:
                                future_count += 1
                        except ValueError:
                            continue
            
            return future_count
        except FileNotFoundError:
            logging.error(f"Words file {self.words_file} not found")
            return 0
    
    def get_next_available_date(self):
        """Find the next available date for a new phrase"""
        try:
            used_dates = set()
            with open(self.words_file, 'r') as file:
                for line in file:
                    if ',' in line:
                        date_str, phrase = line.strip().split(', ')
                        used_dates.add(date_str)
            
            # Start from tomorrow
            current_date = datetime.now().date() + timedelta(days=1)
            
            # Find the next available date
            while current_date.strftime('%Y-%m-%d') in used_dates:
                current_date += timedelta(days=1)
            
            return current_date
            
        except FileNotFoundError:
            return datetime.now().date() + timedelta(days=1)
    
    def generate_future_phrases(self):
        """Generate phrases for future dates when running low"""
        future_count = self.get_future_phrases_count()
        
        logging.info(f"Current future phrases: {future_count}")
        
        if future_count < self.min_days_ahead:
            needed = self.generate_count
            logging.info(f"Running low on phrases! Generating {needed} new phrases...")
            
            # Generate new phrases
            phrases = self.generator.generate_phrases(needed)
            
            if not phrases:
                logging.error("Failed to generate new phrases")
                return
            
            # Add phrases with future dates
            start_date = self.get_next_available_date()
            added_count = 0
            
            for i, phrase in enumerate(phrases):
                date = start_date + timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                
                if self.generator.add_phrase_to_file(phrase, date_str):
                    logging.info(f"Added: {date_str}, {phrase}")
                    added_count += 1
                else:
                    logging.warning(f"Failed to add: {phrase}")
            
            logging.info(f"Successfully added {added_count} phrases to {self.words_file}")
            logging.info(f"Now have {self.get_future_phrases_count()} future phrases")
        else:
            logging.info(f"Sufficient phrases available ({future_count} days ahead)")
    
    def daily_check(self):
        """Daily check function to run"""
        logging.info("Running daily phrase check...")
        self.generate_future_phrases()
    
    def start_scheduler(self, check_interval_hours=24):
        """Start the automated scheduler"""
        logging.info(f"Starting Auto Phrase Scheduler...")
        logging.info(f"Will check every {check_interval_hours} hours")
        logging.info(f"Minimum days ahead: {self.min_days_ahead}")
        logging.info(f"Generate count: {self.generate_count}")
        
        # Schedule daily check
        schedule.every(check_interval_hours).hours.do(self.daily_check)
        
        # Run initial check
        self.daily_check()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Automated phrase scheduler for Dialin game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 auto_phrase_scheduler.py                    # Start scheduler with defaults
  python3 auto_phrase_scheduler.py --check-now       # Run check immediately and exit
  python3 auto_phrase_scheduler.py --min-days 14     # Generate when less than 14 days ahead
  python3 auto_phrase_scheduler.py --generate 50     # Generate 50 phrases at a time
  python3 auto_phrase_scheduler.py --interval 12     # Check every 12 hours
        """
    )
    
    parser.add_argument(
        '--check-now',
        action='store_true',
        help='Run check immediately and exit (don\'t start scheduler)'
    )
    
    parser.add_argument(
        '--min-days',
        type=int,
        default=7,
        help='Minimum days ahead before generating new phrases (default: 7)'
    )
    
    parser.add_argument(
        '--generate',
        type=int,
        default=30,
        help='Number of phrases to generate when running low (default: 30)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=24,
        help='Check interval in hours (default: 24)'
    )
    
    parser.add_argument(
        '--words-file',
        type=str,
        default='words.txt',
        help='Path to words file (default: words.txt)'
    )
    
    args = parser.parse_args()
    
    scheduler = AutoPhraseScheduler(
        words_file=args.words_file,
        min_days_ahead=args.min_days,
        generate_count=args.generate
    )
    
    if args.check_now:
        logging.info("Running immediate check...")
        scheduler.daily_check()
        logging.info("Check complete. Exiting.")
    else:
        try:
            scheduler.start_scheduler(args.interval)
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user")
        except Exception as e:
            logging.error(f"Scheduler error: {e}")

if __name__ == "__main__":
    main() 